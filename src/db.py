from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# CRUD Operations
# -------------------------------

def insert_note(note_data: dict):
    response = supabase.table("notes").insert(note_data).execute()
    return response

def get_notes_by_user(user_id: str):
    response = supabase.table("notes").select("*").eq("user_id", user_id).execute()
    return response

def update_note(note_id: int, note_data: dict):
    response = supabase.table("notes").update(note_data).eq("id", note_id).execute()
    return response

def delete_note(note_id: int):
    response = supabase.table("notes").delete().eq("id", note_id).execute()
    return response
