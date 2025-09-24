from fastapi import HTTPException
from .db import insert_note, get_notes_by_user, update_note, delete_note

def create_note_logic(note):
    response = insert_note(note)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

def get_notes_logic(user_id):
    response = get_notes_by_user(user_id)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

def update_note_logic(note_id, note):
    response = update_note(note_id, note)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

def delete_note_logic(note_id):
    response = delete_note(note_id)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Note deleted successfully"}
