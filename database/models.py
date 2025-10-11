"""
Database models for the Pothole Complaint Portal
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Complaint:
    """Complaint data model"""
    id: Optional[int] = None
    photo_path: str = ""  # Can be multiple paths separated by semicolon
    location: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tags: str = ""  # Comma-separated tags
    description: str = ""
    created_at: Optional[datetime] = None
    status: str = "pending"  # pending, in_progress, resolved
    resolved_at: Optional[datetime] = None
    resolution_time_hours: Optional[float] = None
    user_id: Optional[int] = None  # User who created the complaint
    assigned_to: Optional[int] = None  # Admin/Moderator assigned to handle
    updated_by: Optional[int] = None  # Last user who updated the complaint
    
    def get_tags_list(self) -> List[str]:
        """Convert tags string to list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list: List[str]):
        """Convert tags list to string"""
        self.tags = ', '.join(tags_list)
    
    def get_photo_paths(self) -> List[str]:
        """Convert photo_path string to list of paths"""
        return [path.strip() for path in self.photo_path.split(';') if path.strip()]
    
    def set_photo_paths(self, paths_list: List[str]):
        """Convert photo paths list to string"""
        self.photo_path = ';'.join(paths_list)
    
   
