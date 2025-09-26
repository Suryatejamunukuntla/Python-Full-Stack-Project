import streamlit as st #streamlit run frontend/app.py
import requests
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logic import format_tags
load_dotenv()
API_URL = "http://localhost:8000"

if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "share_link" not in st.session_state:
    st.session_state["share_link"] = ""
if "share_input_value" not in st.session_state:
    st.session_state["share_input_value"] = ""  
if "share_input_counter" not in st.session_state:
    st.session_state["share_input_counter"] = 0 

def switch_page(page_name: str):
    st.session_state["page"] = page_name

# ------------------------------
# Pages
# ------------------------------
def login_page():
    st.title("Login")
    email = st.text_input("Email").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        try:
            res = requests.post(f"{API_URL}/login",
                                json={"email": email, "password": password}, timeout=3)
            data = res.json()
        except requests.exceptions.RequestException:
            st.error("Cannot connect to backend. Make sure FastAPI is running.")
            return

        if res.status_code == 200 and data:
            st.session_state["user_id"] = data["user_id"]
            st.session_state["name"] = data.get("name", "")
            st.success(f"Welcome back, {st.session_state['name']}!")
            switch_page("notes")
        else:
            st.error(data.get("detail", "Invalid email or password"))

    st.write("Don't have an account?")
    if st.button("Go to Register"):
        switch_page("register")

def register_page():
    st.title("Register")
    name = st.text_input("Name").strip()
    email = st.text_input("Email").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Register"):
        if not name:
            st.error("Please enter your name")
            return
        try:
            res = requests.post(f"{API_URL}/register",
                                json={"name": name, "email": email, "password": password}, timeout=3)
            data = res.json()
        except requests.exceptions.RequestException:
            st.error("Cannot connect to backend. Make sure FastAPI is running.")
            return

        if res.status_code in [200, 201] and data:
            st.success("Registration successful! Please log in.")
            switch_page("login")
        else:
            st.error(data.get("detail", "Registration failed"))

    st.write("Already have an account?")
    if st.button("Go to Login"):
        switch_page("login")

def notes_page():
    st.header("📝 My Notes")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("⚠️ Please log in first.")
        switch_page("login")
        return

    # --- Create Note ---
    st.subheader("➕ Create a New Note")
    title = st.text_input("📝 Title", key="new_title")
    content = st.text_area("✏️ Content", key="new_content")
    tags = st.text_input("🏷 Tags (comma separated)", key="new_tags")
    is_shared = st.checkbox("🔗 Share this note", key="new_shared")

    if st.button("Create Note", key="create_note_btn"):
        payload = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "tags": format_tags(tags),
            "is_shared": is_shared
        }
        try:
            res = requests.post(f"{API_URL}/notes/", json=payload, timeout=3)
        except requests.exceptions.RequestException:
            st.error("❌ Cannot connect to backend. Make sure FastAPI is running.")
            return

        if res.status_code == 200:
            st.success("✅ Note created successfully!")
            st.rerun()
        else:
            st.error("❌ Error creating note")

    # --- Display User Notes ---
    st.subheader("📚 Your Notes")
    try:
        res = requests.get(f"{API_URL}/notes/", params={"user_id": user_id}, timeout=3)
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to backend.")
        return

    if res.status_code == 200:
        notes = res.json()
        if not notes:
            st.info("ℹ️ No notes found. Create one above.")
        else:
            for note in notes:
                with st.expander(f"📝 {note['title']}"):
                    st.write(note['content'])
                    st.write("🏷 Tags:", ", ".join(note.get("tags", [])))
                    if note.get('is_shared'):
                        st.write(f"🔗 Share link: {note.get('share_link')}")

                    # --- Edit toggle button ---
                    edit_key = f"edit_enabled_{note['id']}"
                    if edit_key not in st.session_state:
                        st.session_state[edit_key] = False

                    if st.button("✏️ Edit Note", key=f"edit_btn_{note['id']}"):
                        st.session_state[edit_key] = True

                    if st.session_state[edit_key]:
                        edit_title = st.text_input("📝 Edit Title", value=note['title'], key=f"edit_title_{note['id']}")
                        edit_content = st.text_area("✏️ Edit Content", value=note['content'], key=f"edit_content_{note['id']}")
                        edit_tags = st.text_input(
                            "🏷 Edit Tags (comma separated)",
                            value=",".join(note.get("tags", [])),
                            key=f"edit_tags_{note['id']}"
                        )
                        if st.button("💾 Save Changes", key=f"save_{note['id']}"):
                            payload = {
                                "title": edit_title,
                                "content": edit_content,
                                "tags": format_tags(edit_tags)
                            }
                            try:
                                update_res = requests.put(f"{API_URL}/notes/{note['id']}", json=payload, timeout=3)
                            except requests.exceptions.RequestException:
                                st.error("❌ Cannot connect to backend.")
                                return

                            if update_res.status_code == 200:
                                st.success("✅ Note updated successfully!")
                                st.session_state[edit_key] = False
                                st.rerun()
                            else:
                                st.error(f"❌ Error updating note: {update_res.status_code}")

                    # --- Delete Note ---
                    if st.button("🗑 Delete Note", key=f"delete_{note['id']}"):
                        try:
                            del_res = requests.delete(
                                f"{API_URL}/notes/{note['id']}",
                                params={"user_id": user_id},
                                timeout=3
                            )
                        except requests.exceptions.RequestException:
                            st.error("❌ Cannot connect to backend.")
                            return
                        if del_res.status_code == 200:
                            st.success("✅ Note deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete note")
                st.write("---")
    else:
        st.error("❌ Error fetching notes")

    # --- Shared Note Section ---
    st.subheader("🔗 Access / Edit a Shared Note")
    share_input_key = f"share_input_widget_{st.session_state['share_input_counter']}"
    share_input = st.text_input(
        "🔗 Enter share link",
        value=st.session_state.get("share_input_value", ""),
        key=share_input_key
    )

    if st.button("📂 Open Shared Note", key="open_shared_btn"):
        st.session_state["share_link"] = share_input.strip()
        st.session_state["share_input_value"] = share_input.strip()
        if not share_input.strip():
            st.error("⚠️ Please enter a share link")
        else:
            st.rerun()

    if st.session_state.get("share_link"):
        share_link = st.session_state["share_link"]
        try:
            res = requests.get(f"{API_URL}/notes/share/{share_link}", timeout=3)
        except requests.exceptions.RequestException:
            st.error("❌ Cannot connect to backend.")
            return
        if res.status_code == 200:
            shared_note = res.json()
            st.text_input("📝 Edit Title", value=shared_note["title"], key="shared_title")
            st.text_area("✏️ Edit Content", value=shared_note["content"], key="shared_content")
            st.text_input(
                "🏷 Edit Tags (comma separated)",
                value=",".join(shared_note.get("tags", [])),
                key="shared_tags"
            )
            if st.button("💾 Save Changes to Shared Note", key="save_shared_btn"):
                payload = {
                    "title": st.session_state["shared_title"],
                    "content": st.session_state["shared_content"],
                    "tags": format_tags(st.session_state["shared_tags"])
                }
                try:
                    update_res = requests.put(f"{API_URL}/notes/share/{share_link}", json=payload, timeout=3)
                except requests.exceptions.RequestException:
                    st.error("❌ Cannot connect to backend.")
                    return
                if update_res.status_code == 200:
                    st.success("✅ Shared note updated successfully!")
                    st.session_state["share_link"] = ""
                    st.session_state["share_input_value"] = ""
                    st.session_state["share_input_counter"] += 1
                    st.rerun()
                else:
                    st.error("❌ Error updating shared note")

    if st.button("🚪 Logout", key="logout_btn"):
        st.session_state.clear()
        switch_page("login")





# ------------------------------
# Router
# ------------------------------
page = st.session_state["page"]
if page == "login":
    login_page()
elif page == "register":
    register_page()
elif page == "notes":
    notes_page()
