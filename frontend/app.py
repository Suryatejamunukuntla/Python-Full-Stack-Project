import streamlit as st
import requests
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.logic import format_tags

load_dotenv()
API_URL = "http://localhost:8000"

# ------------------------------
# Session state initialisation
# ------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "share_link" not in st.session_state:
    st.session_state["share_link"] = ""


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
        res = requests.post(f"{API_URL}/login",
                            json={"email": email, "password": password})
        try:
            data = res.json()
        except Exception:
            st.error(res.text or "Login failed")
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

        res = requests.post(f"{API_URL}/register",
                            json={"name": name, "email": email, "password": password})
        try:
            data = res.json()
        except Exception:
            st.error(res.text or "Registration failed")
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
    st.title("My Notes")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in first.")
        switch_page("login")
        return

    # --- Create Note ---
    st.subheader("Create a new note")
    title = st.text_input("Title", key="new_title")
    content = st.text_area("Content", key="new_content")
    tags = st.text_input("Tags (comma separated)", key="new_tags")
    is_shared = st.checkbox("Share this note", key="new_shared")

    if st.button("Create Note"):
        payload = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "tags": format_tags(tags),
            "is_shared": is_shared
        }
        res = requests.post(f"{API_URL}/notes/", json=payload)
        if res.status_code == 200:
            st.success("Note created successfully!")
        else:
            st.error("Error creating note")

    # --- Display User Notes ---
    st.subheader("Your Notes")
    res = requests.get(f"{API_URL}/notes/", params={"user_id": user_id})
    if res.status_code == 200:
        notes = res.json()
        if notes:
            for note in notes:
                st.markdown(f"**{note['title']}**")
                st.write(note['content'])
                if note.get('is_shared'):
                    st.write(f"Share link: {note.get('share_link')}")
                st.write("---")
        else:
            st.write("No notes found.")
    else:
        st.error("Error fetching notes")

    # --- Shared Note Collaboration Section ---
    st.subheader("Access / Edit a Shared Note")
    share_input = st.text_input("Enter share link", st.session_state.get("share_link", ""), key="share_input")

    if st.button("Open Shared Note"):
        st.session_state["share_link"] = share_input.strip()
        if not share_input.strip():
            st.error("Please enter a share link")
        else:
            st.rerun()

    # If a share link is set, fetch the shared note via API
    if st.session_state.get("share_link"):
        share_link = st.session_state["share_link"]
        res = requests.get(f"{API_URL}/notes/share/{share_link}")
        if res.status_code == 200:
            shared_note = res.json()
            st.markdown(f"### Editing Shared Note: **{shared_note['title']}**")
            new_title = st.text_input("Edit Title", value=shared_note["title"], key="shared_title")
            new_content = st.text_area("Edit Content", value=shared_note["content"], key="shared_content")
            new_tags = st.text_input(
                "Edit Tags (comma separated)",
                value=",".join(shared_note.get("tags", [])),
                key="shared_tags"
            )

            if st.button("Save Changes to Shared Note"):
                payload = {
                    "title": new_title,
                    "content": new_content,
                    "tags": format_tags(new_tags)
                }
                update_res = requests.put(f"{API_URL}/notes/share/{share_link}", json=payload)
                if update_res.status_code == 200:
                    st.success("Shared note updated successfully!")
                else:
                    st.error("Error updating shared note")
        else:
            st.error("Invalid or inaccessible share link.")

    if st.button("Logout"):
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
