# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.db import insert_note, get_user_notes, get_shared_note_by_link, update_note, delete_note
#uvicorn api.main:app --reload 
import uuid

app = FastAPI()

# ------------------------------
# Models
# ------------------------------
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class NoteIn(BaseModel):
    user_id: int
    title: str
    content: str
    tags: list
    is_shared: bool = False

class SharedNoteUpdate(BaseModel):
    title: str
    content: str
    tags: list

class UserNoteUpdate(BaseModel):  # <-- For editing user-created notes
    title: str
    content: str
    tags: list

# ------------------------------
# User functions
# ------------------------------
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(name: str, email: str, password: str):
    existing = supabase.table("users").select("*").eq("email", email).execute()
    if existing.data:
        return None
    res = supabase.table("users").insert({
        "name": name,
        "email": email,
        "password": password
    }).execute()
    return res.data[0] if res.data else None

def login_user(email: str, password: str):
    res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
    return res.data[0] if res.data else None

# ------------------------------
# Endpoints
# ------------------------------
@app.post("/register")
def register(user: RegisterIn):
    u = register_user(user.name, user.email, user.password)
    if not u:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"user_id": u["id"], "name": u["name"]}

@app.post("/login")
def login(user: LoginIn):
    u = login_user(user.email, user.password)
    if not u:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"user_id": u["id"], "name": u["name"]}

@app.post("/notes/")
def create_note(note: NoteIn):
    share_link = str(uuid.uuid4()) if note.is_shared else None
    note_data = {
        "user_id": note.user_id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "is_shared": note.is_shared,
        "share_link": share_link
    }
    n = insert_note(note_data)
    if not n:
        raise HTTPException(status_code=500, detail="Failed to create note")
    return {"note_id": n["id"], "share_link": share_link}

@app.get("/notes/")
def fetch_notes(user_id: int):
    notes = get_user_notes(user_id)
    return notes

@app.put("/notes/{note_id}")  # <-- New endpoint for editing user notes
def update_user_note(note_id: str, data: UserNoteUpdate):
    updated = update_note(note_id, data.dict())
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update note")
    return {"message": "Note updated successfully"}

@app.get("/notes/share/{share_link}")
def fetch_shared_note(share_link: str):
    note = get_shared_note_by_link(share_link)
    if not note:
        raise HTTPException(status_code=404, detail="Shared note not found")
    return note

@app.put("/notes/share/{share_link}")
def update_shared_note(share_link: str, data: SharedNoteUpdate):
    note = get_shared_note_by_link(share_link)
    if not note:
        raise HTTPException(status_code=404, detail="Shared note not found")
    updated = update_note(note["id"], data.dict())
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update note")
    return {"message": "Shared note updated successfully"}

@app.delete("/notes/{note_id}")
def remove_note(note_id: str, user_id: str):
    success = delete_note(note_id, user_id)   # <-- implement in src/db.py
    if not success:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return {"message": "Note deleted successfully"}
