import streamlit as st
import requests

# -----------------------
# Config
# -----------------------
API_URL = "http://localhost:8000"
  # FastAPI backend

# Hardcoded user ID for demo
USER_ID = "1a942b8b-07a7-410d-9d72-14980126ea4f"  # Replace with a valid UUID from users table

# -----------------------
# Helper Functions
# -----------------------

def get_notes():
    try:
        response = requests.get(f"{API_URL}/notes/{USER_ID}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching notes: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def create_note(title, content):
    data = {
        "title": title,
        "content": content,
        "user_id": USER_ID,
        "shared": False
    }
    try:
        response = requests.post(f"{API_URL}/notes/", json=data)
        if response.status_code == 200 or response.status_code == 201:
            st.success("Note added successfully!")
        else:
            st.error(f"Error adding note: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")

def delete_note(note_id):
    try:
        response = requests.delete(f"{API_URL}/notes/{note_id}")
        if response.status_code == 200:
            st.success("Note deleted successfully!")
        else:
            st.error(f"Error deleting note: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------
# Streamlit UI
# -----------------------

st.title("📒 Collaborative Notes App")

# Form to add a new note
st.subheader("Add a New Note")
with st.form("note_form"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    submitted = st.form_submit_button("Add Note")
    if submitted:
        if title.strip() == "" or content.strip() == "":
            st.warning("Title and Content cannot be empty")
        else:
            create_note(title, content)

st.markdown("---")

# Display existing notes
st.subheader("Your Notes")
notes = get_notes()
if notes:
    for note in notes:
        st.markdown(f"**{note['title']}**")
        st.markdown(f"{note['content']}")
        if st.button(f"Delete Note {note['id']}", key=f"delete_{note['id']}"):
            delete_note(note["id"])
else:
    st.info("No notes found. Add one above!")
