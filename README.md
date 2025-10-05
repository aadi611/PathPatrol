# PathPatrol 🛣️

### *Smart Pothole Reporting with Interactive Geospatial Intelligence*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Transform your city's road maintenance with real-time, GPS-powered complaint visualization**

PathPatrol is a next-generation pothole complaint management system that revolutionizes how citizens report road issues and how authorities track them. Built with Python and Streamlit, it combines powerful geospatial mapping with an intuitive user experience.

---

## 🌟 **Exceptional USP: Interactive Map View**

### **See Every Complaint, Everywhere, Instantly**

PathPatrol's **Interactive Map View** sets it apart from traditional complaint systems:

<div align="center">

### 🗺️ **Dual-Layer Visualization System**

**Precision Markers** + **Density Heatmap** = **Complete Situational Awareness**

</div>

#### **Why Our Map View is Game-Changing:**

| Feature | Traditional Systems | PathPatrol Map View |
|---------|-------------------|---------------------|
| **Visual Intelligence** | ❌ Text lists only | ✅ Interactive markers + heatmap |
| **Geographic Context** | ❌ No spatial awareness | ✅ Instant hotspot identification |
| **Worldwide Coverage** | ❌ Limited to specific regions | ✅ Global OpenStreetMap integration |
| **Real-Time Updates** | ❌ Static reports | ✅ Dynamic map with live data |
| **Density Analysis** | ❌ Manual counting | ✅ Automated heatmap clustering |
| **Click-to-Details** | ❌ Separate navigation | ✅ Popup with full complaint info |

### **🎯 Map View Features:**

#### **1. Smart Marker System**
- 📍 **Color-Coded Status**: 
  - 🔴 Red = Pending (urgent action needed)
  - 🟡 Yellow = In Progress (being addressed)
  - 🟢 Green = Resolved (completed)
  - ⚫ Black = Rejected
- 📌 **Click for Details**: Each marker shows:
  - Complaint ID
  - Exact location name
  - GPS coordinates
  - Current status
  - Report date

#### **2. Heat Density Visualization**
- 🔥 **Problem Hotspots**: Instantly identify areas with multiple complaints
- 🎨 **Gradient Intensity**: Color scale from blue (few) to red (many)
- 📊 **Resource Allocation**: Plan maintenance teams based on density patterns
- 🔍 **Zoom-Adaptive**: Clusters adjust dynamically at different zoom levels

#### **3. Global Location Search**
- 🌍 **Worldwide Coverage**: From New York to Tokyo, Mumbai to London
- 🔍 **Smart Autocomplete**: Type-as-you-search with 15 location suggestions
- 📍 **Professional Dropdown**: Clean, user-friendly selection interface
- 🎯 **Auto-GPS Extraction**: Coordinates filled automatically from photos

#### **4. Map Analytics Dashboard**
- 📊 **Total Complaints**: Overall count at a glance
- 📍 **With GPS**: Number of geotagged reports
- ⚠️ **Without GPS**: Alerts for incomplete data
- 📈 **Coverage Metrics**: Track geolocation adoption rate

---

## ✨ **Complete Feature Set**

### **🚀 Core Capabilities**

#### **📸 Multi-Photo Upload**
- Upload up to **6 high-quality images** per complaint
- Automatic GPS extraction from EXIF data
- Supported formats: JPG, PNG, GIF, WebP
- Smart image optimization and storage

#### **🌐 Global Location Intelligence**
- **OpenStreetMap Integration**: Search any location worldwide
- **Autocomplete Dropdown**: Professional, fast location search
- **Manual Override**: Enter custom GPS coordinates
- **Auto-Geocoding**: Converts location names to coordinates

#### **📊 Advanced Analytics Dashboard**
- **Visual Charts**: Pie charts, bar graphs, timeline views
- **Status Distribution**: See complaint breakdown by status
- **Tag Analysis**: Most common issue categories
- **Trend Tracking**: Daily submission patterns
- **Performance Gauges**: Resolution time metrics

#### **🔍 Powerful Filtering & Search**
- **Full-Text Search**: Find complaints by keywords
- **Date Range Filter**: Custom time period selection
- **Tag Filtering**: Multiple category selection
- **Status Filtering**: Pending, resolved, in-progress, rejected
- **Smart Sorting**: By date, status, or location

#### **💾 Data Export**
- **Excel Export**: `.xlsx` format with full data
- **CSV Export**: Universal compatibility
- **One-Click Download**: Filtered or complete datasets
- **Batch Processing**: Handle large datasets efficiently

#### **🎨 Premium Dark Theme**
- **Eye-Friendly**: Professional dark blue/black palette
- **Consistent Design**: Unified across all pages
- **Modern UI**: Clean, minimalist interface
- **Accessibility**: High contrast for readability

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
- Python 3.11 or higher
- pip package manager
- Internet connection (for map tiles)

### **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/aadi611/PathPatrol.git
cd PathPatrol
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Launch the application:**

**Windows PowerShell:**
```powershell
.\run.ps1
```

**Windows CMD:**
```cmd
run.bat
```

**Manual Start:**
```bash
streamlit run app.py
```

5. **Open browser:**
```
http://localhost:8501
```

---

## 📱 **User Guide**

### **Submitting a Complaint**

1. **Navigate to "📝 Submit Complaint"**
2. **Upload Photos**: 
   - Click "Browse files" or drag-and-drop
   - Select up to 6 images
   - ✅ GPS auto-extracted if enabled
3. **Search Location**:
   - Type city/street/landmark (e.g., "Times Square New York")
   - Select from dropdown (15 results)
   - GPS coordinates auto-fill
4. **Add Details**:
   - Select relevant tags (safety hazard, large, deep, etc.)
   - Add optional description
5. **Submit**: Click "🚀 Submit Complaint"

### **Viewing the Map** 🗺️

1. **Go to "🗺️ Map View"**
2. **Explore**:
   - 🖱️ Zoom in/out with mouse wheel
   - 📍 Click markers for complaint details
   - 🔥 View heatmap for problem areas
   - 🎨 See color-coded status markers
3. **Check Statistics**:
   - 📊 Total complaints with GPS
   - ⚠️ Identify data gaps
   - 📈 Track coverage metrics
4. **Plan Action**:
   - 🔴 Red hotspots = priority areas
   - 🟢 Green markers = completed work
   - 🟡 Yellow = work in progress

### **Analyzing Data**

1. **Visit "📊 Statistics"**
2. **View Charts**:
   - Status distribution (pie chart)
   - Tag frequency (bar chart)
   - Daily trends (timeline)
   - Resolution efficiency (gauge)
3. **Export Data**:
   - Click "Export to Excel" or "Export to CSV"
   - Use for reports or further analysis

---

## 🏗️ **Technology Stack**

### **Backend**
- **Python 3.11+**: Core programming language
- **SQLite3**: Lightweight, serverless database
- **Pillow (PIL)**: Image processing and EXIF extraction

### **Frontend**
- **Streamlit 1.28+**: Web application framework
- **Custom CSS**: Dark theme styling

### **Geospatial** 🗺️
- **Folium 0.14+**: Interactive Leaflet.js maps
- **streamlit-folium**: Streamlit-Folium integration
- **geopy 2.4+**: Geocoding and location search
- **OpenStreetMap Nominatim**: Global geocoding API

### **Data & Visualization**
- **Plotly 5.17+**: Interactive charts and graphs
- **pandas 2.1+**: Data manipulation and export
- **openpyxl 3.1+**: Excel file generation

---

## 📂 **Project Architecture**

```
pathpatrol/
│
├── 📄 app.py                      # Main application entry point
│
├── ⚙️ config/
│   ├── __init__.py
│   └── settings.py                # App configuration, themes, defaults
│
├── 🗄️ database/
│   ├── __init__.py
│   ├── models.py                  # Complaint data model
│   └── db_manager.py              # SQLite operations & queries
│
├── 🔧 services/
│   ├── __init__.py
│   ├── complaint_service.py       # Business logic layer
│   └── storage_service.py         # File upload & GPS extraction
│
├── 🎨 ui/
│   ├── __init__.py
│   ├── components.py              # Reusable UI components
│   └── styles.py                  # CSS styling
│
├── 🛠️ utils/
│   ├── __init__.py
│   ├── map_utils.py               # 🗺️ Folium map generation (KEY USP!)
│   ├── chart_utils.py             # Plotly chart creation
│   └── location_utils.py          # Geocoding service
│
├── 💾 data/
│   ├── complaints.db              # SQLite database
│   └── uploads/                   # Uploaded images
│
├── 📋 requirements.txt            # Python dependencies
├── 📖 README.md                   # This file
└── 🚀 run.ps1 / run.bat          # Quick launch scripts
```

### **Design Principles**

- **Modular Architecture**: Clear separation of concerns
- **Service Layer**: Business logic isolated from UI
- **Reusable Components**: DRY (Don't Repeat Yourself)
- **Scalable Storage**: File-based with path references
- **Type Hinting**: Better code documentation and IDE support

---

## 🎯 **Use Cases**

### **For Citizens** 👥
- 🏘️ Report dangerous potholes in neighborhoods
- 📱 Submit with smartphone GPS photos
- 🔍 Track complaint status and resolution
- 📊 See community-wide road conditions

### **For Municipal Authorities** 🏛️
- 🗺️ **Visual dispatch planning** via map hotspots
- 📈 Data-driven resource allocation
- 📊 Performance tracking and reporting
- 🎯 Priority identification through density analysis
- 💰 Budget justification with geographical data

### **For Urban Planners** 🏗️
- 📍 Identify chronic problem areas
- 📉 Analyze maintenance patterns over time
- 💼 Budget allocation with visual evidence
- 🎨 Long-term infrastructure planning using heatmaps

### **For Emergency Services** 🚨
- ⚠️ Identify dangerous road sections
- 🗺️ Route planning to avoid hazardous areas
- 📊 Safety risk assessment by location

---

## 🔧 **Configuration**

### **Database Location**
```python
# config/settings.py
DATABASE_DIR = Path(__file__).parent.parent / "data"
```

### **Upload Settings**
```python
# Maximum file size: 10MB
# Supported formats: JPG, PNG, GIF, WebP
# Max images per complaint: 6
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
```

### **Map Configuration** 🗺️
```python
# Default map center: [20.5937, 78.9629] (India)
# Zoom levels: 1-18 (1=world, 18=street level)
# Tile provider: OpenStreetMap
# Heatmap: Gradient blue→yellow→red
```

### **Theme Settings**
```python
# Dark Theme (default)
PRIMARY_COLOR = "#3B82F6"      # Blue
BACKGROUND_COLOR = "#0F172A"   # Dark navy
TEXT_COLOR = "#F8FAFC"         # Light gray
```

---

## 🚧 **Troubleshooting**

### **Map not showing complaints?**
✅ Ensure complaints have GPS coordinates:
```bash
python fix_gps.py  # Auto-geocode existing complaints
```

### **Images not displaying?**
✅ Check file paths in database:
```bash
python debug_db.py  # Diagnose path issues
```

### **Location search not working?**
✅ Check internet connection (requires OpenStreetMap API)

---

## 🤝 **Contributing**

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to branch**: `git push origin feature/AmazingFeature`
5. **Open Pull Request**

### **Development Guidelines**
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Test map features thoroughly
- Update documentation as needed
- Test with various GPS coordinates

---

## 📊 **Database Schema**

```sql
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_path TEXT NOT NULL,              -- Semicolon-separated paths
    location TEXT NOT NULL,
    latitude REAL,                         -- 🗺️ For map markers
    longitude REAL,                        -- 🗺️ For map markers
    tags TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',         -- pending/in_progress/resolved/rejected
    resolved_at TIMESTAMP,
    resolution_time_hours REAL
);
```

---

## 🗺️ **Map View Technical Details**

### **Marker System**
```python
# Color coding logic
STATUS_COLORS = {
    'pending': 'red',          # 🔴 Urgent attention
    'in_progress': 'orange',   # 🟡 Being worked on
    'resolved': 'green',       # 🟢 Completed
    'rejected': 'black'        # ⚫ Dismissed
}
```

### **Heatmap Algorithm**
- **Radius**: 15 pixels at zoom level
- **Blur**: 20 pixels for smooth gradients
- **Min Opacity**: 0.4
- **Gradient**: `{0.4: 'blue', 0.65: 'yellow', 1.0: 'red'}`

### **Performance**
- Handles 1000+ complaints efficiently
- Lazy loading for large datasets
- Client-side clustering for markers
- Cached geocoding results

---

## 🛣️ **Roadmap**

### **Phase 1: Core Features** ✅ COMPLETE
- [x] Multi-photo upload
- [x] GPS extraction from photos
- [x] Global location search
- [x] Interactive map with markers
- [x] Heatmap visualization
- [x] Analytics dashboard
- [x] Data export

### **Phase 2: Enhanced Mapping** 🚧 IN PROGRESS
- [ ] Cluster markers for better performance
- [ ] Route planning around potholes
- [ ] Area-based filtering on map
- [ ] Time-lapse map animation

### **Phase 3: Advanced Features** 📋 PLANNED
- [ ] User authentication
- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] API for third-party integrations
- [ ] Real-time updates (WebSocket)

### **Phase 4: AI Integration** 🔮 FUTURE
- [ ] AI pothole severity detection
- [ ] Predictive maintenance suggestions
- [ ] Automatic duplicate detection
- [ ] Smart priority scoring

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **OpenStreetMap Contributors**: Global mapping data and tile servers
- **Streamlit Team**: Amazing web framework for rapid development
- **Folium Developers**: Leaflet.js Python wrapper for beautiful maps
- **Plotly**: Interactive visualization library
- **geopy**: Geocoding made simple

---

## 📞 **Support & Contact**

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/aadi611/PathPatrol/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/aadi611/PathPatrol/discussions)
- 📧 **Email**: support@pathpatrol.app
- 📱 **Twitter**: @PathPatrolApp

---

## 📈 **Stats**

![GitHub stars](https://img.shields.io/github/stars/aadi611/PathPatrol?style=social)
![GitHub forks](https://img.shields.io/github/forks/aadi611/PathPatrol?style=social)
![GitHub issues](https://img.shields.io/github/issues/aadi611/PathPatrol)
![GitHub pull requests](https://img.shields.io/github/issues-pr/aadi611/PathPatrol)

---

<div align="center">

### 🌟 **Star this repository if PathPatrol helps your community!** 🌟

**Built with ❤️ for better roads and safer communities**

### 🗺️ *"Mapping Problems, Paving Solutions"* 🗺️

[⬆ Back to Top](#pathpatrol-)

</div>
