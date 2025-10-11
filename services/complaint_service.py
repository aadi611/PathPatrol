"""
Complaint service for business logic
"""
from typing import List, Optional
from database import DatabaseManager, Complaint
from .storage_service import StorageService
from .email_service import EmailService
import os

    class ComplaintService:
    """Handles complaint-related business logic"""

    def __init__(self):
        """Initialize complaint service"""
        self.db = DatabaseManager()
        self.storage = StorageService()
        # Initialize email service if notifications are enabled
        self.email_enabled = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'false').lower() == 'true'
        if self.email_enabled:
            self.email_service = EmailService()
        else:
            self.email_service = None
    
    def submit_complaint(
        self,
        uploaded_files,  # Can be single file or list
        location: str,
        latitude: Optional[float],
        longitude: Optional[float],
        tags: List[str],
        description: str,
        user_id: Optional[int] = None
    ) -> Optional[int]:
        """
        Submit a new complaint
        
        Returns:
            Complaint ID if successful, None otherwise
        """
        try:
            # Handle single or multiple files
            if not isinstance(uploaded_files, list):
                uploaded_files = [uploaded_files]
            
            # Save all images
            photo_paths = []
            for uploaded_file in uploaded_files:
                photo_path = self.storage.save_image(uploaded_file)
                if photo_path:
                    photo_paths.append(photo_path)
            
            if not photo_paths:
                return None
            
            # Create complaint object
            complaint = Complaint(
                photo_path=';'.join(photo_paths),  # Store multiple paths separated by semicolon
                location=location,
                latitude=latitude,
                longitude=longitude,
                tags=', '.join(tags),
                description=description,
                status='pending',
                user_id=user_id
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
    
    def get_complaints_by_user(self, user_id: int) -> List[Complaint]:
        """Get all complaints by a specific user"""
        return self.db.get_complaints_by_user(user_id)
    
    def filter_by_tag(self, tag: str) -> List[Complaint]:
        """Filter complaints by tag"""
        return self.db.get_complaints_by_tag(tag)
    
    def update_status(self, complaint_id: int, status: str, user_email: Optional[str] = None) -> bool:
        """
        Update complaint status and send notification email
        
        Args:
            complaint_id: ID of the complaint
            status: New status
            user_email: Email of the user who filed the complaint (optional)
            
        Returns:
            True if successful
        """
        success = self.db.update_status(complaint_id, status)
        
        # Send email notification if enabled and email provided
        if success and self.email_service and user_email:
            complaint = self.get_complaint(complaint_id)
            if complaint:
                self.email_service.send_complaint_status_update(
                    user_email=user_email,
                    complaint_id=complaint_id,
                    old_status=complaint.status,
                    new_status=status,
                    location=complaint.location
                )
        
        return success
    
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
    
    def search_complaints(self, search_term: str) -> List[Complaint]:
        """Search complaints"""
        return self.db.search_complaints(search_term)
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Complaint]:
        """Filter by date range"""
        return self.db.filter_by_date_range(start_date, end_date)
    
    def export_to_dataframe(self):
        """Export all complaints to pandas DataFrame"""
        import pandas as pd
        complaints = self.get_all_complaints(limit=10000)
        
        data = []
        for c in complaints:
            data.append({
                'ID': c.id,
                'Location': c.location,
                'Latitude': c.latitude,
                'Longitude': c.longitude,
                'Tags': c.tags,
                'Description': c.description,
                'Status': c.status,
                'Created At': c.created_at,
                'Resolved At': c.resolved_at,
                'Resolution Time (hours)': c.resolution_time_hours
            })
        
        return pd.DataFrame(data)
    
    def extract_gps_from_image(self, uploaded_file):
        """Extract GPS coordinates from image"""
        return self.storage.extract_gps_from_image(uploaded_file)
