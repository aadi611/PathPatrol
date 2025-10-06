"""Fix GPS coordinates for existing complaints"""
import sqlite3
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
except ImportError:
    print("Installing required package...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Create geocoder
geolocator = Nominatim(user_agent="pathpatrol_fix", timeout=10)

# Database path
DB_PATH = Path(__file__).parent / "data" / "complaints.db"

def fix_complaints_without_gps():
    """Add GPS coordinates to complaints that don't have them"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get complaints without GPS
    cursor.execute("""
        SELECT id, location 
        FROM complaints 
        WHERE latitude IS NULL OR longitude IS NULL
    """)
    
    complaints = cursor.fetchall()
    
    if not complaints:
        print("✅ All complaints have GPS coordinates!")
        return
    
    print(f"Found {len(complaints)} complaint(s) without GPS coordinates\n")
    
    for complaint_id, location in complaints:
        print(f"Complaint #{complaint_id}: {location}")
        
        # Search for location using geopy
        try:
            geo_results = geolocator.geocode(location, exactly_one=False, limit=1)
            
            if geo_results:
                result = geo_results[0] if isinstance(geo_results, list) else geo_results
                lat = result.latitude
                lon = result.longitude
                full_name = result.address
                
                # Update database
                cursor.execute("""
                    UPDATE complaints 
                    SET latitude = ?, longitude = ?
                    WHERE id = ?
                """, (lat, lon, complaint_id))
                
                print(f"  ✅ Updated with GPS: {lat:.6f}, {lon:.6f}")
                print(f"  📍 Full location: {full_name}\n")
            else:
                print(f"  ⚠️ Could not find GPS for this location\n")
        except Exception as e:
            print(f"  ⚠️ Error: {e}\n")
    
    conn.commit()
    conn.close()
    print("✅ GPS fix complete!")

if __name__ == "__main__":
    fix_complaints_without_gps()
