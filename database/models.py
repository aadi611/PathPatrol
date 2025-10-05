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
    photo_path: str = ""
    location: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tags: str = ""  # Comma-separated tags
    description: str = ""
    created_at: Optional[datetime] = None
    status: str = "pending"  # pending, in_progress, resolved
    
    def get_tags_list(self) -> List[str]:
        """Convert tags string to list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list: List[str]):
        """Convert tags list to string"""
        self.tags = ', '.join(tags_list)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'photo_path': self.photo_path,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'tags': self.tags,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }
