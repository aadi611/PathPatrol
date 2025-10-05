"""
Custom CSS styles for the application
"""
from config.settings import THEMES


def get_custom_css(theme: str = "light") -> str:
    """
    Generate custom CSS based on theme
    
    Args:
        theme: 'light' or 'dark'
    
    Returns:
        CSS string
    """
    colors = THEMES[theme]
    
    return f"""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Main app styling */
    .stApp {{
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    
    /* Header styles */
    .main-header {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }}
    
    .main-header h1 {{
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    
    .main-header p {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }}
    
    /* Card styles */
    .complaint-card {{
        background-color: {colors['surface']};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .complaint-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    
    /* Form styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {{
        background-color: {colors['surface']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {colors['primary']};
        box-shadow: 0 0 0 3px rgba(46, 134, 222, 0.1);
    }}
    
    /* Button styles */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46, 134, 222, 0.3);
    }}
    
    /* File uploader */
    .stFileUploader {{
        background-color: {colors['surface']};
        border: 2px dashed {colors['border']};
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }}
    
    .stFileUploader:hover {{
        border-color: {colors['primary']};
        background-color: {colors['background']};
    }}
    
    /* Multiselect */
    .stMultiSelect > div > div {{
        background-color: {colors['surface']};
        border-radius: 8px;
    }}
    
    /* Tags */
    .tag {{
        display: inline-block;
        background-color: {colors['primary']};
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: 500;
    }}
    
    /* Status badges */
    .status-pending {{
        background-color: #FFA502;
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }}
    
    .status-in_progress {{
        background-color: {colors['secondary']};
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }}
    
    .status-resolved {{
        background-color: #26DE81;
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }}
    
    /* Image container */
    .image-container {{
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    .image-container img {{
        width: 100%;
        height: auto;
        display: block;
    }}
    
    /* Statistics */
    .stat-card {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .stat-label {{
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }}
    
    /* Theme toggle */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {colors['surface']};
        border-right: 1px solid {colors['border']};
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 1.75rem;
        }}
        
        .complaint-card {{
            padding: 1rem;
        }}
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['border']};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['primary']};
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .complaint-card {{
        animation: fadeIn 0.3s ease-out;
    }}
    </style>
    """


def apply_theme(theme: str = "dark"):
    """Apply dark theme to Streamlit app"""
    import streamlit as st
    # Always use dark theme
    st.markdown(get_custom_css("dark"), unsafe_allow_html=True)
