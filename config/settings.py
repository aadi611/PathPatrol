"""
Configuration settings for the Pothole Complaint Portal
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "complaints.db"

# Upload settings
UPLOAD_DIR = DATABASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE_MB = 10

# Application settings
APP_TITLE = "Pothole Complaint Portal"
APP_ICON = "🚧"
PAGE_LAYOUT = "wide"

# Theme colors - Dark mode only
THEMES = {
    "dark": {
        "primary": "#1E3A8A",
        "secondary": "#3B82F6",
        "background": "#0F172A",
        "surface": "#1E293B",
        "text": "#F1F5F9",
        "text_secondary": "#94A3B8",
        "border": "#334155",
        "accent": "#60A5FA"
    }
}

# Tags
DEFAULT_TAGS = [
    "Severe", "Moderate", "Minor",
    "Highway", "Residential", "Commercial",
    "Urgent", "Maintenance", "Safety Hazard"
]

# Create necessary directories
def init_directories():
    """Create required directories if they don't exist"""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
