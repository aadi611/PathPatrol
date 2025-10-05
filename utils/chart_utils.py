"""
Chart utilities for data visualization
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List


def create_status_pie_chart(stats: Dict):
    """Create pie chart for complaint status distribution"""
    if not stats.get('by_status'):
        return None
    
    labels = [status.replace('_', ' ').title() for status in stats['by_status'].keys()]
    values = list(stats['by_status'].values())
    
    colors = {
        'Pending': '#FFA502',
        'In Progress': '#3B82F6',
        'Resolved': '#26DE81'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=[colors.get(label, '#888888') for label in labels]),
        textinfo='label+percent',
        textfont=dict(size=14, color='white')
    )])
    
    fig.update_layout(
        title="Complaints by Status",
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        font=dict(color='#F1F5F9'),
        showlegend=True,
        legend=dict(
            font=dict(color='#F1F5F9')
        )
    )
    
    return fig


def create_tag_bar_chart(stats: Dict):
    """Create bar chart for tag distribution"""
    if not stats.get('by_tag'):
        return None
    
    tags = list(stats['by_tag'].keys())
    counts = list(stats['by_tag'].values())
    
    # Sort by count
    sorted_data = sorted(zip(tags, counts), key=lambda x: x[1], reverse=True)
    tags, counts = zip(*sorted_data) if sorted_data else ([], [])
    
    fig = go.Figure(data=[go.Bar(
        x=list(tags),
        y=list(counts),
        marker=dict(
            color=list(counts),
            colorscale='Blues',
            showscale=False
        ),
        text=list(counts),
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Complaints by Tag",
        xaxis_title="Tag",
        yaxis_title="Count",
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        font=dict(color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', color='#F1F5F9'),
        yaxis=dict(gridcolor='#334155', color='#F1F5F9')
    )
    
    return fig


def create_timeline_chart(stats: Dict):
    """Create timeline chart for complaints over time"""
    if not stats.get('timeline'):
        return None
    
    timeline_data = stats['timeline']
    
    dates = [item['date'] for item in timeline_data]
    counts = [item['count'] for item in timeline_data]
    
    fig = go.Figure(data=[go.Scatter(
        x=dates,
        y=counts,
        mode='lines+markers',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8, color='#60A5FA'),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.2)'
    )])
    
    fig.update_layout(
        title="Complaints Over Time (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Number of Complaints",
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        font=dict(color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155', color='#F1F5F9'),
        yaxis=dict(gridcolor='#334155', color='#F1F5F9')
    )
    
    return fig


def create_resolution_time_chart(stats: Dict):
    """Create chart showing average resolution time"""
    avg_hours = stats.get('avg_resolution_hours')
    
    if avg_hours is None or avg_hours == 0:
        return None
    
    # Convert to days for better readability
    avg_days = avg_hours / 24
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_days,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Avg Resolution Time (Days)", 'font': {'color': '#F1F5F9'}},
        number={'font': {'color': '#F1F5F9'}},
        gauge={
            'axis': {'range': [None, 30], 'tickcolor': '#F1F5F9'},
            'bar': {'color': "#3B82F6"},
            'steps': [
                {'range': [0, 7], 'color': "#26DE81"},
                {'range': [7, 14], 'color': "#FFA502"},
                {'range': [14, 30], 'color': "#FF6348"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 14
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        font=dict(color='#F1F5F9'),
        height=300
    )
    
    return fig


def create_dashboard_charts(stats: Dict):
    """Create comprehensive dashboard with multiple charts"""
    if not stats:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Status Distribution", "Tag Distribution", 
                       "Timeline", "Resolution Metrics"),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "indicator"}]]
    )
    
    # Add status pie chart
    if stats.get('by_status'):
        labels = [s.replace('_', ' ').title() for s in stats['by_status'].keys()]
        values = list(stats['by_status'].values())
        fig.add_trace(
            go.Pie(labels=labels, values=values, hole=0.3),
            row=1, col=1
        )
    
    # Add tag bar chart
    if stats.get('by_tag'):
        tags = list(stats['by_tag'].keys())[:10]  # Top 10
        counts = list(stats['by_tag'].values())[:10]
        fig.add_trace(
            go.Bar(x=tags, y=counts),
            row=1, col=2
        )
    
    # Add timeline
    if stats.get('timeline'):
        dates = [item['date'] for item in stats['timeline']]
        counts = [item['count'] for item in stats['timeline']]
        fig.add_trace(
            go.Scatter(x=dates, y=counts, mode='lines+markers'),
            row=2, col=1
        )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        paper_bgcolor='#1E293B',
        plot_bgcolor='#1E293B',
        font=dict(color='#F1F5F9')
    )
    
    return fig
