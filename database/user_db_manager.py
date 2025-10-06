"""
User database operations
"""
import sqlite3
import bcrypt
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from database.user_models import User
from config.settings import DATABASE_PATH


class UserDatabaseManager:
    """Manages user database operations"""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialize user database manager"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Create users table if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT DEFAULT 'citizen',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    phone TEXT,
                    address TEXT
                )
            """)
            conn.commit()
            
            # Create default admin if no users exist
            cursor.execute("SELECT COUNT(*) as count FROM users")
            if cursor.fetchone()['count'] == 0:
                self.create_default_admin()
    
    def create_default_admin(self):
        """Create default admin user"""
        admin = User(
            username="admin",
            email="admin@pathpatrol.com",
            password_hash=self.hash_password("admin123"),
            full_name="System Administrator",
            role="admin",
            is_active=True
        )
        self.create_user(admin)
        print("✅ Default admin created: username='admin', password='admin123'")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def create_user(self, user: User) -> Optional[int]:
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, full_name, role, phone, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user.username, user.email, user.password_hash, user.full_name, 
                      user.role, user.phone, user.address))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_user_by_username(username)
        if user and user.is_active:
            if self.verify_password(password, user.password_hash):
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users (admin only)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            return [self._row_to_user(row) for row in cursor.fetchall()]
    
    def update_user_role(self, user_id: int, new_role: str) -> bool:
        """Update user role (admin only)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user (admin only)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deactivating user: {e}")
            return False
    
    def activate_user(self, user_id: int) -> bool:
        """Activate user (admin only)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET is_active = 1 WHERE id = ?", (user_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error activating user: {e}")
            return False
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        try:
            password_hash = self.hash_password(new_password)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                             (password_hash, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def _row_to_user(self, row) -> User:
        """Convert database row to User object"""
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            full_name=row['full_name'],
            role=row['role'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            is_active=bool(row['is_active']),
            phone=row['phone'],
            address=row['address']
        )
