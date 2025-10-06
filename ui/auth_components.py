"""
Authentication UI components
"""
import streamlit as st
from database.user_db_manager import UserDatabaseManager
from database.user_models import User


def render_login_page():
    """Render login page"""
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1>🛣️ PathPatrol</h1>
            <p style="font-size: 1.2rem; color: #94A3B8;">Sign in to report and track potholes</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
            with col_btn2:
                signup_btn = st.form_submit_button("📝 Sign Up", use_container_width=True)
            
            if login_btn:
                if username and password:
                    user_db = UserDatabaseManager()
                    user = user_db.authenticate_user(username, password)
                    
                    if user:
                        # Store user in session
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.success(f"✅ Welcome back, {user.full_name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            if signup_btn:
                st.session_state.show_signup = True
                st.rerun()
        
        # Default admin info
        st.info("""
            **🔑 Default Admin Account**  
            Username: `admin`  
            Password: `admin123`
            
            *Please change this password after first login!*
        """)


def render_signup_page():
    """Render signup page"""
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1>🛣️ PathPatrol</h1>
            <p style="font-size: 1.2rem; color: #94A3B8;">Create your account</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📝 Sign Up")
        
        with st.form("signup_form"):
            username = st.text_input("Username *", placeholder="Choose a unique username")
            email = st.text_input("Email *", placeholder="your.email@example.com")
            full_name = st.text_input("Full Name *", placeholder="John Doe")
            password = st.text_input("Password *", type="password", placeholder="Minimum 6 characters")
            password_confirm = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
            phone = st.text_input("Phone", placeholder="+1 234 567 8900 (optional)")
            address = st.text_area("Address", placeholder="Your address (optional)")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                signup_btn = st.form_submit_button("✅ Create Account", use_container_width=True)
            with col_btn2:
                back_btn = st.form_submit_button("← Back to Login", use_container_width=True)
            
            if signup_btn:
                # Validation
                if not all([username, email, full_name, password, password_confirm]):
                    st.error("❌ Please fill all required fields")
                elif password != password_confirm:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    user_db = UserDatabaseManager()
                    
                    # Check if username exists
                    if user_db.get_user_by_username(username):
                        st.error("❌ Username already exists")
                    elif user_db.get_user_by_email(email):
                        st.error("❌ Email already registered")
                    else:
                        # Create new user
                        new_user = User(
                            username=username,
                            email=email,
                            password_hash=user_db.hash_password(password),
                            full_name=full_name,
                            role="citizen",
                            phone=phone,
                            address=address
                        )
                        
                        user_id = user_db.create_user(new_user)
                        if user_id:
                            st.success("✅ Account created successfully! Please login.")
                            st.balloons()
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error("❌ Error creating account. Please try again.")
            
            if back_btn:
                st.session_state.show_signup = False
                st.rerun()


def render_user_profile():
    """Render user profile in sidebar"""
    if 'user' in st.session_state and st.session_state.user:
        user = st.session_state.user
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Profile")
        
        # Role badge color
        role_colors = {
            "admin": "🔴",
            "moderator": "🟡",
            "citizen": "🟢"
        }
        
        role_emoji = role_colors.get(user.role, "⚪")
        
        st.sidebar.markdown(f"""
            <div style="padding: 1rem; background: #1E293B; border-radius: 0.5rem; margin-bottom: 1rem;">
                <p style="margin: 0; font-weight: bold; font-size: 1.1rem;">{user.full_name}</p>
                <p style="margin: 0.5rem 0 0 0; color: #94A3B8; font-size: 0.9rem;">@{user.username}</p>
                <p style="margin: 0.5rem 0 0 0;">
                    {role_emoji} <span style="text-transform: capitalize;">{user.role}</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            # Clear session
            st.session_state.user = None
            st.session_state.authenticated = False
            st.success("👋 Logged out successfully!")
            st.rerun()


def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if 'authenticated' not in st.session_state or not st.session_state.authenticated:
            render_login_page()
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_role(allowed_roles: list):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user' not in st.session_state or st.session_state.user.role not in allowed_roles:
                st.error("⛔ Access Denied: You don't have permission to access this page")
                st.info(f"Required role(s): {', '.join(allowed_roles)}")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_permission(user: User, action: str, complaint_user_id: int = None) -> bool:
    """Check if user has permission for an action"""
    if user.is_admin():
        return True  # Admin can do everything
    
    if action == "update_status" and user.is_moderator():
        return True
    
    if action == "edit_own" and complaint_user_id == user.id:
        return True
    
    if action == "delete" and user.is_admin():
        return True
    
    return False
