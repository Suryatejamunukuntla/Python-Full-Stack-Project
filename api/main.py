from fastapi import FastAPI
from pydantic import BaseModel
from src.logic import create_note_logic, get_notes_logic, update_note_logic, delete_note_logic

app = FastAPI()

class Note(BaseModel):
    id: int | None = None
    title: str
    content: str
    user_id: str
    shared: bool = False

@app.post("/notes/")
def create_note(note: Note):
    return create_note_logic(note.dict())

@app.get("/notes/{user_id}")
def get_notes(user_id: str):
    return get_notes_logic(user_id)

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    return update_note_logic(note_id, note.dict())

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    return delete_note_logic(note_id)
