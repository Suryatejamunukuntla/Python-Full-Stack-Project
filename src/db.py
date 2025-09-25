# src/db.py
from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_note(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Insert a new note and return the inserted row"""
    res = supabase.table("notes").insert(data).execute()
    return res.data[0] if res.data else None


def get_user_notes(user_id: str) -> List[Dict[str, Any]]:
    """Get all notes for a given user"""
    res = supabase.table("notes").select("*").eq("user_id", user_id).execute()
    return res.data or []


def get_shared_note_by_link(link: str) -> Optional[Dict[str, Any]]:
    """Get a single shared note by its share_link"""
    res = supabase.table("notes").select("*").eq("share_link", link).single().execute()
    return res.data if res.data else None


def update_note(note_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a note by ID and return the updated row"""
    res = supabase.table("notes").update(data).eq("id", note_id).execute()
    return res.data[0] if res.data else None
