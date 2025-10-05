"""
PathPatrol - Pothole Complaint Portal
A modern web application for reporting potholes with photo upload and location tracking
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import APP_TITLE, APP_ICON, PAGE_LAYOUT, init_directories
from services import ComplaintService
from ui.styles import apply_theme
from ui.components import (
    render_header, 
    render_complaint_form, 
    render_complaint_card,
    render_statistics,
    render_theme_toggle,
    render_search_and_filters,
    render_export_button
)


# Initialize application
def init_app():
    """Initialize application settings and directories"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state="expanded"
    )
    
    # Initialize directories
    init_directories()
    
    # Initialize session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    if 'filter_tag' not in st.session_state:
        st.session_state.filter_tag = None
    
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    
    if 'date_range' not in st.session_state:
        st.session_state.date_range = None
    
    if 'sort_by' not in st.session_state:
        st.session_state.sort_by = "Newest First"


def handle_complaint_submission(uploaded_files, location, latitude, longitude, tags, description):
    """Handle complaint form submission"""
    service = ComplaintService()
    
    with st.spinner("Submitting your complaint..."):
        complaint_id = service.submit_complaint(
            uploaded_files=uploaded_files,
            location=location,
            latitude=latitude,
            longitude=longitude,
            tags=tags,
            description=description
        )
    
    if complaint_id:
        st.success(f"✅ Complaint submitted successfully! ID: #{complaint_id}")
        st.balloons()
    else:
        st.error("❌ Failed to submit complaint. Please try again.")


def render_sidebar():
    """Render sidebar with filters and options"""
    with st.sidebar:
        # Navigation
        st.title("📋 Navigation")
        page = st.radio(
            "Go to",
            ["Submit Complaint", "View Complaints", "Map View", "Statistics"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Filters (only show on View Complaints page)
        if page == "View Complaints":
            st.title("🔍 Filters")
            
            # Tag filter
            from config.settings import DEFAULT_TAGS
            filter_tag = st.selectbox(
                "Filter by tag",
                options=["All"] + DEFAULT_TAGS
            )
            st.session_state.filter_tag = None if filter_tag == "All" else filter_tag
            
            # Status filter
            status_filter = st.selectbox(
                "Filter by status",
                options=["All", "Pending", "In Progress", "Resolved"]
            )
            st.session_state.status_filter = None if status_filter == "All" else status_filter.lower().replace(' ', '_')
        
        st.divider()
        
        # About
        st.markdown("""
        ### About PathPatrol
        Report potholes and help improve our roads.
        
        **Features:**
        - 📸 Multiple photo upload
        - 📍 Auto GPS extraction
        - 🗺️ Interactive maps
        - 🔍 Advanced filtering
        - 📊 Analytics & charts
        - 📥 Export to Excel/CSV
        """)
        
        return page


def render_submit_page():
    """Render the submit complaint page"""
    render_complaint_form(handle_complaint_submission)


def render_view_page():
    """Render the view complaints page"""
    st.subheader("📋 All Complaints")
    
    service = ComplaintService()
    
    # Export button
    render_export_button(service)
    
    # Search and filters
    search_term = render_search_and_filters()
    
    # Get complaints based on filters
    complaints = []
    
    if search_term:
        complaints = service.search_complaints(search_term)
    elif st.session_state.date_range:
        start_date, end_date = st.session_state.date_range
        complaints = service.filter_by_date_range(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
    elif st.session_state.filter_tag:
        complaints = service.filter_by_tag(st.session_state.filter_tag)
    else:
        complaints = service.get_all_complaints(limit=50)
    
    # Apply status filter if set
    if hasattr(st.session_state, 'status_filter') and st.session_state.status_filter:
        complaints = [c for c in complaints if c.status == st.session_state.status_filter]
    
    # Sort complaints
    if st.session_state.sort_by == "Newest First":
        complaints.sort(key=lambda x: x.created_at if x.created_at else datetime.min, reverse=True)
    elif st.session_state.sort_by == "Oldest First":
        complaints.sort(key=lambda x: x.created_at if x.created_at else datetime.min)
    elif st.session_state.sort_by == "Status":
        complaints.sort(key=lambda x: x.status)
    
    if not complaints:
        st.info("No complaints found. Be the first to report a pothole!")
    else:
        st.write(f"Showing {len(complaints)} complaint(s)")
        
        # Display complaints in a grid
        for complaint in complaints:
            render_complaint_card(complaint, show_image=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            
            with col1:
                if complaint.status != 'resolved':
                    new_status = 'in_progress' if complaint.status == 'pending' else 'resolved'
                    if st.button(f"Mark as {new_status.replace('_', ' ').title()}", key=f"status_{complaint.id}"):
                        if service.update_status(complaint.id, new_status):
                            st.success(f"Status updated to {new_status.replace('_', ' ')}")
                            st.rerun()
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{complaint.id}"):
                    if service.delete_complaint(complaint.id):
                        st.success("Complaint deleted")
                        st.rerun()
                    else:
                        st.error("Failed to delete complaint")
            
            st.divider()


def render_stats_page():
    """Render the statistics page"""
    service = ComplaintService()
    stats = service.get_statistics()
    
    render_statistics(stats)
    
    st.divider()
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    complaints = service.get_all_complaints(limit=5)
    
    if complaints:
        for complaint in complaints:
            render_complaint_card(complaint, show_image=False)
    else:
        st.info("No complaints yet")


def render_map_page():
    """Render the interactive map page"""
    from streamlit_folium import st_folium
    from utils.map_utils import create_complaints_map, create_heatmap
    
    st.subheader("🗺️ Complaint Map")
    
    service = ComplaintService()
    
    # Get all complaints
    all_complaints = service.get_all_complaints(limit=1000)
    
    if not all_complaints:
        st.info("📋 No complaints found yet. Submit your first complaint to see it on the map!")
        return
    
    # Filter complaints with coordinates
    complaints_with_coords = [c for c in all_complaints if c.latitude and c.longitude]
    
    # Show statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Complaints", len(all_complaints))
    with col2:
        st.metric("With GPS", len(complaints_with_coords))
    with col3:
        st.metric("Without GPS", len(all_complaints) - len(complaints_with_coords))
    
    if not complaints_with_coords:
        st.warning("⚠️ No complaints with GPS coordinates found yet!")
        st.info("""
        **How to add GPS coordinates:**
        
        1. 🔍 **Use Location Search** (Recommended!)
           - Type location in search box
           - Select from dropdown
           - GPS auto-fills
        
        2. 📸 **Upload Photos with GPS**
           - Take photos with smartphone
           - Ensure location services enabled
           - GPS extracted automatically
        
        3. ✏️ **Enter Manually**
           - Check "Override with manual GPS coordinates"
           - Enter latitude and longitude
        """)
        return
    
    st.success(f"📍 Showing {len(complaints_with_coords)} complaints with GPS coordinates on map")
    
    # Map type selector
    map_type = st.radio(
        "Map Type",
        ["Markers", "Heatmap"],
        horizontal=True
    )
    
    # Create and display map
    if map_type == "Markers":
        m = create_complaints_map(complaints_with_coords)
    else:
        m = create_heatmap(complaints_with_coords)
    
    if m:
        st_folium(m, width=1200, height=600)
    
    # Show legend
    st.markdown("""
    <div style='background: #1E293B; padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
        <strong>Legend:</strong><br>
        🔴 Red - Pending | 🔵 Blue - In Progress | 🟢 Green - Resolved
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    # Initialize
    init_app()
    
    # Apply theme
    apply_theme(st.session_state.theme)
    
    # Render header
    render_header()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if page == "Submit Complaint":
        render_submit_page()
    elif page == "View Complaints":
        render_view_page()
    elif page == "Map View":
        render_map_page()
    elif page == "Statistics":
        render_stats_page()


if __name__ == "__main__":
    main()
