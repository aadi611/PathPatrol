"""
Map utilities for visualizing complaints
"""
import folium
from folium import plugins
from typing import List
from database.models import Complaint


def create_complaints_map(complaints: List[Complaint], center: tuple = None):
    """
    Create an interactive map with complaint markers
    
    Args:
        complaints: List of Complaint objects
        center: Tuple of (lat, lon) for map center
        
    Returns:
        Folium map object
    """
    # Filter complaints with valid coordinates
    valid_complaints = [c for c in complaints if c.latitude and c.longitude]
    
    if not valid_complaints:
        # Default center (can be customized)
        if center:
            map_center = center
        else:
            map_center = [0, 0]
        zoom_start = 2
    else:
        # Calculate center from complaints
        if center:
            map_center = center
        else:
            avg_lat = sum(c.latitude for c in valid_complaints) / len(valid_complaints)
            avg_lon = sum(c.longitude for c in valid_complaints) / len(valid_complaints)
            map_center = [avg_lat, avg_lon]
        zoom_start = 12
    
    # Create map
    m = folium.Map(
        location=map_center,
        zoom_start=zoom_start,
        tiles='CartoDB dark_matter'  # Dark theme map
    )
    
    # Color mapping for status
    status_colors = {
        'pending': 'red',
        'in_progress': 'blue',
        'resolved': 'green'
    }
    
    # Add markers
    for complaint in valid_complaints:
        color = status_colors.get(complaint.status, 'gray')
        
        # Create popup content
        popup_html = f"""
        <div style='width: 200px'>
            <h4>Complaint #{complaint.id}</h4>
            <p><b>Status:</b> {complaint.status.replace('_', ' ').title()}</p>
            <p><b>Location:</b> {complaint.location}</p>
            <p><b>Tags:</b> {complaint.tags}</p>
            {f'<p><b>Description:</b> {complaint.description[:100]}...</p>' if complaint.description else ''}
            <p><b>Reported:</b> {complaint.created_at.strftime('%Y-%m-%d') if complaint.created_at else 'N/A'}</p>
        </div>
        """
        
        folium.Marker(
            location=[complaint.latitude, complaint.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Complaint #{complaint.id} - {complaint.status.title()}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # Add marker cluster for better visualization
    if len(valid_complaints) > 20:
        marker_cluster = plugins.MarkerCluster().add_to(m)
        for complaint in valid_complaints:
            color = status_colors.get(complaint.status, 'gray')
            popup_html = f"""
            <div style='width: 200px'>
                <h4>Complaint #{complaint.id}</h4>
                <p><b>Status:</b> {complaint.status.replace('_', ' ').title()}</p>
                <p><b>Location:</b> {complaint.location}</p>
            </div>
            """
            folium.Marker(
                location=[complaint.latitude, complaint.longitude],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(marker_cluster)
    
    # Add fullscreen option
    plugins.Fullscreen().add_to(m)
    
    return m


def create_heatmap(complaints: List[Complaint]):
    """
    Create a heatmap of complaint density
    
    Args:
        complaints: List of Complaint objects
        
    Returns:
        Folium map object with heatmap
    """
    # Filter complaints with valid coordinates
    valid_complaints = [c for c in complaints if c.latitude and c.longitude]
    
    if not valid_complaints:
        return None
    
    # Calculate center
    avg_lat = sum(c.latitude for c in valid_complaints) / len(valid_complaints)
    avg_lon = sum(c.longitude for c in valid_complaints) / len(valid_complaints)
    
    # Create map
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=12,
        tiles='CartoDB dark_matter'
    )
    
    # Prepare data for heatmap
    heat_data = [[c.latitude, c.longitude] for c in valid_complaints]
    
    # Add heatmap
    plugins.HeatMap(
        heat_data,
        radius=15,
        blur=25,
        max_zoom=13,
        gradient={
            0.0: 'blue',
            0.5: 'yellow',
            0.7: 'orange',
            1.0: 'red'
        }
    ).add_to(m)
    
    return m
