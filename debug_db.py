"""
Debug utility to check complaints in database
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database import DatabaseManager
from config.settings import DATABASE_PATH, UPLOAD_DIR

def check_database():
    """Check database contents"""
    print("=" * 60)
    print("PathPatrol Database Debug")
    print("=" * 60)
    
    print(f"\n📁 Database Location: {DATABASE_PATH}")
    print(f"📁 Upload Directory: {UPLOAD_DIR}")
    
    if not DATABASE_PATH.exists():
        print("\n❌ Database file does not exist!")
        return
    
    print("\n✅ Database file exists")
    
    db = DatabaseManager()
    
    # Get all complaints
    complaints = db.get_all_complaints(limit=100)
    
    print(f"\n📊 Total Complaints: {len(complaints)}")
    
    if not complaints:
        print("\n⚠️ No complaints found in database")
        return
    
    print("\n" + "=" * 60)
    print("Complaint Details:")
    print("=" * 60)
    
    for complaint in complaints:
        print(f"\n{'=' * 40}")
        print(f"ID: {complaint.id}")
        print(f"Location: {complaint.location}")
        print(f"GPS: {complaint.latitude}, {complaint.longitude}")
        print(f"Photo Path: {complaint.photo_path}")
        print(f"Status: {complaint.status}")
        print(f"Created: {complaint.created_at}")
        
        # Check if photo exists
        photo_paths = complaint.get_photo_paths()
        print(f"\nPhoto Paths ({len(photo_paths)}):")
        for idx, photo_path in enumerate(photo_paths, 1):
            # Try different path combinations
            from services import StorageService
            storage = StorageService()
            
            # Method 1: Using storage service
            path1 = storage.get_image_path(photo_path)
            
            # Method 2: Direct path
            from config.settings import DATABASE_DIR
            path2 = DATABASE_DIR / photo_path
            
            # Method 3: Just upload dir
            path3 = UPLOAD_DIR / Path(photo_path).name
            
            print(f"  {idx}. {photo_path}")
            print(f"     Method 1: {path1} - {'✅ EXISTS' if path1.exists() else '❌ NOT FOUND'}")
            print(f"     Method 2: {path2} - {'✅ EXISTS' if path2.exists() else '❌ NOT FOUND'}")
            print(f"     Method 3: {path3} - {'✅ EXISTS' if path3.exists() else '❌ NOT FOUND'}")
    
    # Check upload directory
    print("\n" + "=" * 60)
    print("Upload Directory Contents:")
    print("=" * 60)
    
    if UPLOAD_DIR.exists():
        files = list(UPLOAD_DIR.glob("*"))
        print(f"\nTotal files in upload directory: {len(files)}")
        for file in files:
            print(f"  - {file.name}")
    else:
        print("\n❌ Upload directory does not exist!")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_database()
