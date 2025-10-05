"""
Complaint service for business logic
"""
from typing import List, Optional
from database import DatabaseManager, Complaint
from .storage_service import StorageService


class ComplaintService:
    """Handles complaint-related business logic"""
    
    def __init__(self):
        """Initialize complaint service"""
        self.db = DatabaseManager()
        self.storage = StorageService()
    
    def submit_complaint(
        self,
        uploaded_file,
        location: str,
        latitude: Optional[float],
        longitude: Optional[float],
        tags: List[str],
        description: str
    ) -> Optional[int]:
        """
        Submit a new complaint
        
        Returns:
            Complaint ID if successful, None otherwise
        """
        try:
            # Save image
            photo_path = self.storage.save_image(uploaded_file)
            if not photo_path:
                return None
            
            # Create complaint object
            complaint = Complaint(
                photo_path=photo_path,
                location=location,
                latitude=latitude,
                longitude=longitude,
                tags=', '.join(tags),
                description=description,
                status='pending'
            )
            
            # Save to database
            complaint_id = self.db.create_complaint(complaint)
            return complaint_id
            
        except Exception as e:
            print(f"Error submitting complaint: {e}")
            return None
    
    def get_all_complaints(self, limit: int = 100) -> List[Complaint]:
        """Get all complaints"""
        return self.db.get_all_complaints(limit=limit)
    
    def get_complaint(self, complaint_id: int) -> Optional[Complaint]:
        """Get a specific complaint"""
        return self.db.get_complaint(complaint_id)
    
    def filter_by_tag(self, tag: str) -> List[Complaint]:
        """Filter complaints by tag"""
        return self.db.get_complaints_by_tag(tag)
    
    def update_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        return self.db.update_status(complaint_id, status)
    
    def delete_complaint(self, complaint_id: int) -> bool:
        """Delete a complaint and its image"""
        complaint = self.db.get_complaint(complaint_id)
        if complaint:
            # Delete image
            self.storage.delete_image(complaint.photo_path)
            # Delete from database
            return self.db.delete_complaint(complaint_id)
        return False
    
    def get_statistics(self) -> dict:
        """Get complaint statistics"""
        return self.db.get_statistics()
    
    def get_image_path(self, relative_path: str):
        """Get absolute image path"""
        return self.storage.get_image_path(relative_path)
