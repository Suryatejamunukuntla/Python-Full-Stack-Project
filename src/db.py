import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Optional, Dict, Any

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_note(user_id, title, content, tags=None, is_shared=False):
    payload = {
        "uid": user_id,
        "title": title,
        "note": content,
    }
    try:
        res = supabase.table("notes").insert(payload).execute()
        return res.data[0]  # the inserted row
    except Exception as e:
        raise RuntimeError(f"Supabase insert failed: {e}")



def get_note(note_id: str):
    try:
        res = supabase.table("notes").select("*").eq("note_id", note_id).limit(1).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise RuntimeError(f"Supabase select failed: {e}")


def get_notes_for_user(uid: str, include_shared: bool = True):
    try:
        if include_shared:
            res = supabase.table("notes").select("*").or_(
                f"user_id.eq.{uid}"
            ).order("updated_at", desc=True).execute()
        else:
            res = supabase.table("notes").select("*").eq("uid", uid).order("updated_at", desc=True).execute()
        return res.data
    except Exception as e:
        raise RuntimeError(f"Supabase select failed: {e}")


def update_note(note_id, title=None, content=None, tags=None, is_shared=None):
    payload = {}
    if title is not None: payload["title"] = title
    if content is not None: payload["content"] = content
    if tags is not None: payload["tags"] = tags
    if is_shared is not None: payload["is_shared"] = is_shared

    if not payload:
        note = get_note(note_id)
        if note is None:
            raise RuntimeError("Note not found")
        return note

    try:
        res = supabase.table("notes").update(payload).eq("id", note_id).execute()
        return res.data[0]
    except Exception as e:
        raise RuntimeError(f"Supabase update failed: {e}")


def delete_note(note_id):
    try:
        supabase.table("notes").delete().eq("id", note_id).execute()
        return True
    except Exception as e:
        raise RuntimeError(f"Supabase delete failed: {e}")

