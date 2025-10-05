"""
UI components for the application
"""
import streamlit as st
from datetime import datetime
from database.models import Complaint
from config.settings import DEFAULT_TAGS, APP_TITLE, APP_ICON


def render_header():
    """Render application header"""
    st.markdown(f"""
        <div class="main-header">
            <h1>{APP_ICON} {APP_TITLE}</h1>
            <p>Report potholes and help improve our roads</p>
        </div>
    """, unsafe_allow_html=True)


def render_complaint_form(on_submit_callback):
    """
    Render complaint submission form
    
    Args:
        on_submit_callback: Function to call on form submission
    """
    st.subheader("📝 Submit New Complaint")
    
    with st.form("complaint_form", clear_on_submit=True):
        # Photo upload
        uploaded_file = st.file_uploader(
            "Upload Pothole Photo *",
            type=['jpg', 'jpeg', 'png', 'gif', 'webp'],
            help="Upload a clear photo of the pothole"
        )
        
        # Location
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input(
                "Location/Address *",
                placeholder="e.g., Main Street near City Hall"
            )
        
        with col2:
            # Optional coordinates
            use_coords = st.checkbox("Add GPS coordinates")
        
        latitude = None
        longitude = None
        if use_coords:
            coord_col1, coord_col2 = st.columns(2)
            with coord_col1:
                latitude = st.number_input(
                    "Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=0.0,
                    format="%.6f"
                )
            with coord_col2:
                longitude = st.number_input(
                    "Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=0.0,
                    format="%.6f"
                )
        
        # Tags
        tags = st.multiselect(
            "Tags",
            options=DEFAULT_TAGS,
            help="Select relevant tags for this complaint"
        )
        
        # Description
        description = st.text_area(
            "Description",
            placeholder="Provide additional details about the pothole...",
            height=100
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)
        
        if submitted:
            # Validation
            if not uploaded_file:
                st.error("⚠️ Please upload a photo")
                return
            
            if not location:
                st.error("⚠️ Please enter a location")
                return
            
            # Call the callback
            on_submit_callback(
                uploaded_file=uploaded_file,
                location=location,
                latitude=latitude if use_coords else None,
                longitude=longitude if use_coords else None,
                tags=tags,
                description=description
            )


def render_complaint_card(complaint: Complaint, show_image: bool = True):
    """
    Render a single complaint card
    
    Args:
        complaint: Complaint object
        show_image: Whether to show the image
    """
    status_class = f"status-{complaint.status}"
    
    # Format date
    if complaint.created_at:
        date_str = complaint.created_at.strftime("%B %d, %Y at %I:%M %p")
    else:
        date_str = "Unknown date"
    
    # Build tags HTML
    tags_html = ""
    if complaint.tags:
        tags_list = complaint.get_tags_list()
        for tag in tags_list:
            tags_html += f'<span class="tag">{tag}</span>'
    
    # Build location info
    location_info = complaint.location
    if complaint.latitude and complaint.longitude:
        location_info += f" ({complaint.latitude:.4f}, {complaint.longitude:.4f})"
    
    st.markdown(f"""
        <div class="complaint-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0;">Complaint #{complaint.id}</h3>
                <span class="{status_class}">{complaint.status.replace('_', ' ').title()}</span>
            </div>
    """, unsafe_allow_html=True)
    
    # Show image if requested
    if show_image:
        try:
            from services import ComplaintService
            service = ComplaintService()
            image_path = service.get_image_path(complaint.photo_path)
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load image: {e}")
    
    st.markdown(f"""
            <div style="margin-top: 1rem;">
                <p><strong>📍 Location:</strong> {location_info}</p>
                <p><strong>📅 Reported:</strong> {date_str}</p>
                {f'<p><strong>🏷️ Tags:</strong> {tags_html}</p>' if tags_html else ''}
                {f'<p><strong>📝 Description:</strong> {complaint.description}</p>' if complaint.description else ''}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_statistics(stats: dict):
    """
    Render statistics dashboard
    
    Args:
        stats: Statistics dictionary
    """
    st.subheader("📊 Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Total Complaints</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pending = stats['by_status'].get('pending', 0)
        st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #FFA502 0%, #FF6348 100%);">
                <div class="stat-number">{pending}</div>
                <div class="stat-label">Pending</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        in_progress = stats['by_status'].get('in_progress', 0)
        st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #54A0FF 0%, #2E86DE 100%);">
                <div class="stat-number">{in_progress}</div>
                <div class="stat-label">In Progress</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        resolved = stats['by_status'].get('resolved', 0)
        st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #26DE81 0%, #20BF6B 100%);">
                <div class="stat-number">{resolved}</div>
                <div class="stat-label">Resolved</div>
            </div>
        """, unsafe_allow_html=True)


def render_theme_toggle():
    """Render theme toggle button in sidebar"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
    theme_label = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
    
    if st.sidebar.button(f"{theme_icon} {theme_label}", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()
