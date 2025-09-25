# src/logic.py
import uuid

def generate_share_link() -> str:
    """Generate a unique UUID-based share link"""
    return str(uuid.uuid4())

def format_tags(tags_str: str) -> list:
    """
    Convert a comma-separated string into a list of clean tags.
    Ignores empty tags and trims whitespace.
    Example: "tag1, , tag2, " -> ["tag1", "tag2"]
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]
