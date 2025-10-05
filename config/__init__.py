"""
Configuration package initialization
"""
from .settings import *

__all__ = [
    'BASE_DIR', 'DATABASE_PATH', 'UPLOAD_DIR', 
    'APP_TITLE', 'APP_ICON', 'THEMES', 'DEFAULT_TAGS',
    'init_directories'
]
