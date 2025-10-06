"""
Test authentication system
Run this to verify database setup and user creation
"""
from database.user_db_manager import UserDatabaseManager
from database.user_models import User

def test_authentication_system():
    """Test the authentication system"""
    print("=" * 60)
    print("PathPatrol - Authentication System Test")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing user database...")
    user_db = UserDatabaseManager()
    print("   ✅ Database initialized")
    
    # Check if default admin exists
    print("\n2. Checking default admin account...")
    admin = user_db.get_user_by_username("admin")
    if admin:
        print(f"   ✅ Default admin exists")
        print(f"      Username: {admin.username}")
        print(f"      Email: {admin.email}")
        print(f"      Role: {admin.role}")
        print(f"      Active: {admin.is_active}")
    else:
        print("   ❌ Default admin not found")
        return
    
    # Test authentication
    print("\n3. Testing authentication...")
    auth_user = user_db.authenticate_user("admin", "admin123")
    if auth_user:
        print("   ✅ Authentication successful")
    else:
        print("   ❌ Authentication failed")
        return
    
    # Test role methods
    print("\n4. Testing role methods...")
    print(f"   is_admin(): {admin.is_admin()}")
    print(f"   is_moderator(): {admin.is_moderator()}")
    print(f"   is_citizen(): {admin.is_citizen()}")
    print(f"   can_edit_any_complaint(): {admin.can_edit_any_complaint()}")
    print(f"   can_delete_complaint(): {admin.can_delete_complaint()}")
    print(f"   can_access_admin_panel(): {admin.can_access_admin_panel()}")
    
    # Create a test citizen user
    print("\n5. Creating test citizen user...")
    test_citizen = User(
        username="test_citizen",
        email="citizen@test.com",
        password_hash=user_db.hash_password("password123"),
        full_name="Test Citizen",
        role="citizen",
        phone="+1234567890"
    )
    
    # Check if user already exists
    existing = user_db.get_user_by_username("test_citizen")
    if existing:
        print("   ℹ️  Test citizen already exists")
    else:
        citizen_id = user_db.create_user(test_citizen)
        if citizen_id:
            print(f"   ✅ Test citizen created (ID: {citizen_id})")
        else:
            print("   ❌ Failed to create test citizen")
    
    # Create a test moderator
    print("\n6. Creating test moderator...")
    test_moderator = User(
        username="test_moderator",
        email="moderator@test.com",
        password_hash=user_db.hash_password("password123"),
        full_name="Test Moderator",
        role="moderator"
    )
    
    existing_mod = user_db.get_user_by_username("test_moderator")
    if existing_mod:
        print("   ℹ️  Test moderator already exists")
    else:
        mod_id = user_db.create_user(test_moderator)
        if mod_id:
            print(f"   ✅ Test moderator created (ID: {mod_id})")
        else:
            print("   ❌ Failed to create test moderator")
    
    # List all users
    print("\n7. Listing all users...")
    all_users = user_db.get_all_users()
    print(f"   Total users: {len(all_users)}")
    for user in all_users:
        status = "✅ Active" if user.is_active else "❌ Inactive"
        print(f"   - {user.username} ({user.role}) - {status}")
    
    print("\n" + "=" * 60)
    print("✅ Authentication System Test Complete!")
    print("=" * 60)
    
    print("\n📋 Test Accounts Created:")
    print("   1. Admin:")
    print("      Username: admin")
    print("      Password: admin123")
    print("      Role: admin")
    print()
    print("   2. Test Citizen:")
    print("      Username: test_citizen")
    print("      Password: password123")
    print("      Role: citizen")
    print()
    print("   3. Test Moderator:")
    print("      Username: test_moderator")
    print("      Password: password123")
    print("      Role: moderator")
    print()
    print("🚀 Ready to test! Run: streamlit run app.py")
    print()

if __name__ == "__main__":
    test_authentication_system()
