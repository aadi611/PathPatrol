"""
Database manager for SQLite operations
"""
import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from .models import Complaint
from config.settings import DATABASE_PATH


class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialize database manager"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo_path TEXT NOT NULL,
                    location TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    tags TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    resolved_at TIMESTAMP,
                    resolution_time_hours REAL
                )
            """)
            
            # Migration: Add new columns if they don't exist
            try:
                cursor.execute("ALTER TABLE complaints ADD COLUMN resolved_at TIMESTAMP")
            except sqlite3.OperationalError:
                # Column already exists
                pass
            
            try:
                cursor.execute("ALTER TABLE complaints ADD COLUMN resolution_time_hours REAL")
            except sqlite3.OperationalError:
                # Column already exists
                pass
            
            conn.commit()
    
    def create_complaint(self, complaint: Complaint) -> int:
        """Insert a new complaint"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO complaints 
                (photo_path, location, latitude, longitude, tags, description, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                complaint.photo_path,
                complaint.location,
                complaint.latitude,
                complaint.longitude,
                complaint.tags,
                complaint.description,
                complaint.status
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_complaint(self, complaint_id: int) -> Optional[Complaint]:
        """Get a single complaint by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_complaint(row)
            return None
    
    def get_all_complaints(self, limit: int = 100, offset: int = 0) -> List[Complaint]:
        """Get all complaints with pagination"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            return [self._row_to_complaint(row) for row in rows]
    
    def get_complaints_by_tag(self, tag: str) -> List[Complaint]:
        """Get complaints by tag"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints 
                WHERE tags LIKE ?
                ORDER BY created_at DESC
            """, (f'%{tag}%',))
            
            rows = cursor.fetchall()
            return [self._row_to_complaint(row) for row in rows]
    
    def update_status(self, complaint_id: int, status: str) -> bool:
        """Update complaint status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # If marking as resolved, update resolved_at and calculate resolution time
            if status == 'resolved':
                cursor.execute("""
                    UPDATE complaints 
                    SET status = ?,
                        resolved_at = CURRENT_TIMESTAMP,
                        resolution_time_hours = (
                            (julianday(CURRENT_TIMESTAMP) - julianday(created_at)) * 24
                        )
                    WHERE id = ?
                """, (status, complaint_id))
            else:
                cursor.execute("""
                    UPDATE complaints 
                    SET status = ?
                    WHERE id = ?
                """, (status, complaint_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_complaint(self, complaint_id: int) -> bool:
        """Delete a complaint"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM complaints WHERE id = ?", (complaint_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_statistics(self) -> dict:
        """Get complaint statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total complaints
            cursor.execute("SELECT COUNT(*) as total FROM complaints")
            total = cursor.fetchone()['total']
            
            # By status
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM complaints 
                GROUP BY status
            """)
            by_status = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Average resolution time
            cursor.execute("""
                SELECT AVG(resolution_time_hours) as avg_resolution_time
                FROM complaints
                WHERE status = 'resolved' AND resolution_time_hours IS NOT NULL
            """)
            avg_resolution = cursor.fetchone()['avg_resolution_time']
            
            # By tag
            cursor.execute("SELECT tags FROM complaints WHERE tags != ''")
            all_tags = {}
            for row in cursor.fetchall():
                tags = [t.strip() for t in row['tags'].split(',') if t.strip()]
                for tag in tags:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
            
            # Complaints over time (last 30 days)
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM complaints
                WHERE created_at >= datetime('now', '-30 days')
                GROUP BY DATE(created_at)
                ORDER BY date
            """)
            timeline = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total': total,
                'by_status': by_status,
                'avg_resolution_hours': avg_resolution,
                'by_tag': all_tags,
                'timeline': timeline
            }
    
    def search_complaints(self, search_term: str) -> List[Complaint]:
        """Search complaints by location or description"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints 
                WHERE location LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            rows = cursor.fetchall()
            return [self._row_to_complaint(row) for row in rows]
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Complaint]:
        """Filter complaints by date range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints 
                WHERE DATE(created_at) BETWEEN ? AND ?
                ORDER BY created_at DESC
            """, (start_date, end_date))
            
            rows = cursor.fetchall()
            return [self._row_to_complaint(row) for row in rows]
    
    def _row_to_complaint(self, row: sqlite3.Row) -> Complaint:
        """Convert database row to Complaint object"""
        # Check if columns exist in the row
        try:
            resolved_at = row['resolved_at']
        except (KeyError, IndexError):
            resolved_at = None
        
        try:
            resolution_time_hours = row['resolution_time_hours']
        except (KeyError, IndexError):
            resolution_time_hours = None
        
        return Complaint(
            id=row['id'],
            photo_path=row['photo_path'],
            location=row['location'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            tags=row['tags'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            status=row['status'],
            resolved_at=datetime.fromisoformat(resolved_at) if resolved_at else None,
            resolution_time_hours=resolution_time_hours
        )
