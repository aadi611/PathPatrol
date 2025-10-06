"""
User data models
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User model"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    full_name: str = ""
    role: str = "citizen"  # citizen, moderator, admin
    created_at: Optional[datetime] = None
    is_active: bool = True
    phone: Optional[str] = None
    address: Optional[str] = None
    
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == "admin"
    
    def is_moderator(self) -> bool:
        """Check if user is moderator"""
        return self.role == "moderator"
    
    def is_citizen(self) -> bool:
        """Check if user is citizen"""
        return self.role == "citizen"
    
    def can_edit_any_complaint(self) -> bool:
        """Check if user can edit any complaint"""
        return self.role in ["admin", "moderator"]
    
    def can_delete_complaint(self) -> bool:
        """Check if user can delete complaints"""
        return self.role == "admin"
    
    def can_access_admin_panel(self) -> bool:
        """Check if user can access admin panel"""
        return self.role in ["admin", "moderator"]
