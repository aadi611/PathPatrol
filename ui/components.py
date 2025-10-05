"""
UI components for the application
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from database.models import Complaint
from config.settings import DEFAULT_TAGS, APP_TITLE, APP_ICON
from io import BytesIO


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
    from utils.location_utils import location_service
    
    st.subheader("📝 Submit New Complaint")
    
    with st.form("complaint_form", clear_on_submit=True):
        # Photo upload - Multiple files
        uploaded_files = st.file_uploader(
            "Upload Pothole Photo(s) * (Multiple images allowed)",
            type=['jpg', 'jpeg', 'png', 'gif', 'webp'],
            accept_multiple_files=True,
            help="Upload clear photos of the pothole"
        )
        
        # Auto GPS extraction option
        auto_gps = st.checkbox("🔍 Auto-extract GPS from first photo", value=True)
        
        st.markdown("---")
        st.markdown("### 📍 Location Information")
        
        st.info("💡 **Tip:** Search for your location worldwide - cities, streets, landmarks!")
        
        # Location search with integrated dropdown
        col1, col2 = st.columns([3, 1])
        
        with col1:
            location_search = st.text_input(
                "🔍 Search Location *",
                placeholder="Start typing: 'New York', 'Tokyo', 'London', 'Paris'...",
                help="Type at least 3 characters to search",
                key="location_search"
            )
        
        with col2:
            if location_search and len(location_search) >= 3:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.spinner("🔍"):
                    pass
        
        # Search and display dropdown immediately below search box
        selected_location = None
        selected_coords = None
        
        if location_search and len(location_search) >= 3:
            with st.spinner("Searching locations..."):
                results = location_service.search_locations(location_search, limit=15)
            
            if results:
                # Create dropdown options with clean formatting
                location_options = {
                    "-- Select your location from the list below --": None
                }
                
                for result in results:
                    # Format the display nicely
                    display = result['display_name']
                    location_options[display] = result
                
                # Dropdown menu appears right below search
                selected_display = st.selectbox(
                    "Select from search results:",
                    options=list(location_options.keys()),
                    key="location_dropdown",
                    help="Choose the exact location from the dropdown"
                )
                
                # Process selection
                if selected_display != "-- Select your location from the list below --":
                    selected_result = location_options[selected_display]
                    if selected_result:
                        selected_location = selected_result['display_name']
                        selected_coords = (
                            selected_result['latitude'],
                            selected_result['longitude']
                        )
                        
                        # Display selected details in nice cards
                        st.success(f"✅ Location Selected!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("📍 Latitude", f"{selected_coords[0]:.6f}°")
                        with col2:
                            st.metric("📍 Longitude", f"{selected_coords[1]:.6f}°")
            else:
                st.warning("⚠️ No locations found. Try a different search or use manual entry below.")
        
        # Manual location entry (fallback)
        st.markdown("**Or enter location manually:**")
        manual_location = st.text_input(
            "Manual Location Entry",
            placeholder="e.g., Main Street near City Hall",
            help="Use this if search doesn't find your location"
        )
        
        # Manual coordinates override
        use_manual_coords = st.checkbox("Override with manual GPS coordinates")
        
        manual_latitude = None
        manual_longitude = None
        if use_manual_coords:
            coord_col1, coord_col2 = st.columns(2)
            with coord_col1:
                manual_latitude = st.number_input(
                    "Latitude",
                    min_value=-90.0,
                    max_value=90.0,
                    value=0.0,
                    format="%.6f"
                )
            with coord_col2:
                manual_longitude = st.number_input(
                    "Longitude",
                    min_value=-180.0,
                    max_value=180.0,
                    value=0.0,
                    format="%.6f"
                )
        
        st.markdown("---")
        
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
            if not uploaded_files:
                st.error("⚠️ Please upload at least one photo")
                return
            
            # Determine final location
            final_location = None
            if selected_location:
                final_location = selected_location
            elif manual_location:
                final_location = manual_location
            
            if not final_location:
                st.error("⚠️ Please select a location from search or enter manually")
                return
            
            # Determine final coordinates
            final_lat, final_lon = None, None
            
            # Priority: Manual coords > Selected coords > Auto-extracted GPS
            if use_manual_coords:
                final_lat, final_lon = manual_latitude, manual_longitude
            elif selected_coords:
                final_lat, final_lon = selected_coords
            elif auto_gps and uploaded_files:
                from services import ComplaintService
                service = ComplaintService()
                gps_coords = service.extract_gps_from_image(uploaded_files[0])
                if gps_coords:
                    final_lat, final_lon = gps_coords
                    st.success(f"📍 GPS extracted from photo: {final_lat:.6f}, {final_lon:.6f}")
            
            # Call the callback
            on_submit_callback(
                uploaded_files=uploaded_files,
                location=final_location,
                latitude=final_lat,
                longitude=final_lon,
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
    
    # Resolution time
    resolution_html = ""
    if complaint.resolved_at and complaint.resolution_time_hours:
        days = complaint.resolution_time_hours / 24
        resolution_html = f'<p><strong>⏱️ Resolution Time:</strong> {days:.1f} days</p>'
    
    st.markdown(f"""
        <div class="complaint-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0;">Complaint #{complaint.id}</h3>
                <span class="{status_class}">{complaint.status.replace('_', ' ').title()}</span>
            </div>
    """, unsafe_allow_html=True)
    
    # Show images if requested
    if show_image:
        try:
            from services import ComplaintService
            service = ComplaintService()
            photo_paths = complaint.get_photo_paths()
            
            # Display images in columns if multiple
            if len(photo_paths) > 1:
                cols = st.columns(min(len(photo_paths), 3))
                for idx, photo_path in enumerate(photo_paths[:6]):  # Max 6 images
                    image_path = service.get_image_path(photo_path)
                    if image_path.exists():
                        with cols[idx % 3]:
                            st.image(str(image_path), use_column_width=True)
            elif len(photo_paths) == 1:
                image_path = service.get_image_path(photo_paths[0])
                if image_path.exists():
                    st.image(str(image_path), use_column_width=True)
        except Exception as e:
            st.warning(f"Could not load images: {e}")
    
    st.markdown(f"""
            <div style="margin-top: 1rem;">
                <p><strong>📍 Location:</strong> {location_info}</p>
                <p><strong>📅 Reported:</strong> {date_str}</p>
                {f'<p><strong>🏷️ Tags:</strong> {tags_html}</p>' if tags_html else ''}
                {f'<p><strong>📝 Description:</strong> {complaint.description}</p>' if complaint.description else ''}
                {resolution_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_statistics(stats: dict):
    """
    Render statistics dashboard with charts
    
    Args:
        stats: Statistics dictionary
    """
    import plotly.graph_objects as go
    from utils.chart_utils import (
        create_status_pie_chart,
        create_tag_bar_chart,
        create_timeline_chart,
        create_resolution_time_chart
    )
    
    st.subheader("📊 Statistics Overview")
    
    # Top metrics
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts in two columns
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Status pie chart
        pie_chart = create_status_pie_chart(stats)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
        
        # Timeline chart
        timeline_chart = create_timeline_chart(stats)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)
    
    with chart_col2:
        # Tag bar chart
        tag_chart = create_tag_bar_chart(stats)
        if tag_chart:
            st.plotly_chart(tag_chart, use_container_width=True)
        
        # Resolution time gauge
        resolution_chart = create_resolution_time_chart(stats)
        if resolution_chart:
            st.plotly_chart(resolution_chart, use_container_width=True)
        else:
            st.info("⏱️ No resolved complaints yet to show average resolution time")


def render_theme_toggle():
    """Render theme toggle button in sidebar - Dark mode only"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Always use dark mode
    st.session_state.theme = 'dark'


def render_search_and_filters():
    """Render advanced search and filtering options"""
    st.subheader("🔍 Search & Filters")
    
    # Search bar
    search_term = st.text_input(
        "Search",
        placeholder="Search by location or description...",
        key="search_input"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date range filter
        use_date_filter = st.checkbox("Filter by date range")
        if use_date_filter:
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
            st.session_state.date_range = (start_date, end_date)
        else:
            st.session_state.date_range = None
    
    with col2:
        # Sort options
        sort_by = st.selectbox(
            "Sort by",
            options=["Newest First", "Oldest First", "Status"]
        )
        st.session_state.sort_by = sort_by
    
    return search_term


def render_export_button(service):
    """Render export to CSV/Excel button"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("📥 Export Data", use_container_width=True):
            try:
                df = service.export_to_dataframe()
                
                # Convert to Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Complaints')
                
                output.seek(0)
                
                st.download_button(
                    label="📥 Download Excel",
                    data=output,
                    file_name=f"pathpatrol_complaints_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                # Also provide CSV option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"pathpatrol_complaints_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Export failed: {e}")
