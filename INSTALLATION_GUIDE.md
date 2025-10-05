# PathPatrol - Installation & Setup Guide

## 🚀 Quick Start

### Step 1: Install New Dependencies

```powershell
# Make sure you're in the project directory
cd c:\Projects\govt_assist_road

# Activate virtual environment (if you created one)
.\.venv\Scripts\Activate.ps1

# Install all requirements
pip install -r requirements.txt
```

### Step 2: Run the Application

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📦 Dependencies Breakdown

### Core Framework:
- `streamlit==1.28.0` - Web framework

### Image Processing:
- `Pillow==10.1.0` - Image manipulation & EXIF reading

### Data Handling:
- `pandas==2.1.1` - Data export to Excel/CSV
- `openpyxl==3.1.2` - Excel file writing

### Visualizations:
- `plotly==5.17.0` - Interactive charts
- `folium==0.14.0` - Map generation
- `streamlit-folium==0.15.0` - Folium integration with Streamlit

### Database:
- SQLite3 (built-in Python) - Local database

---

## 🎨 Application Features

### 1. Submit Complaints
- Upload 1-6 photos
- Auto GPS extraction from photos
- Manual GPS override
- Tags and descriptions
- Real-time validation

### 2. View Complaints
- Advanced search
- Date range filtering
- Tag filtering
- Status filtering
- Sort options
- Export to Excel/CSV

### 3. Map View (NEW!)
- Interactive marker map
- Heatmap visualization
- Click markers for details
- Dark theme optimized

### 4. Statistics (ENHANCED!)
- Status pie chart
- Tag bar chart
- Timeline chart (30 days)
- Resolution time gauge
- Top metrics cards

---

## 🗂️ Project Structure

```
govt_assist_road/
│
├── app.py                          # Main application
├── requirements.txt                # Dependencies
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration
│
├── database/
│   ├── __init__.py
│   ├── models.py                   # Data models
│   └── db_manager.py               # Database operations
│
├── services/
│   ├── __init__.py
│   ├── complaint_service.py        # Business logic
│   └── storage_service.py          # File & GPS handling
│
├── ui/
│   ├── __init__.py
│   ├── components.py               # UI components
│   └── styles.py                   # Dark theme CSS
│
├── utils/
│   ├── __init__.py
│   ├── map_utils.py                # Map generation
│   └── chart_utils.py              # Chart creation
│
└── data/
    ├── complaints.db               # SQLite database (auto-created)
    └── uploads/                    # Uploaded photos (auto-created)
```

---

## 🎯 Usage Guide

### Creating Your First Complaint:

1. Click "Submit Complaint" in sidebar
2. Upload photo(s) - try a smartphone photo with GPS
3. Enter location
4. GPS will auto-extract if available
5. Add tags (Severe, Highway, etc.)
6. Add description
7. Click "Submit Complaint"

### Viewing Complaints:

1. Click "View Complaints"
2. Use search or filters
3. Click action buttons to update status
4. Export data if needed

### Exploring Maps:

1. Click "Map View"
2. Toggle between Markers/Heatmap
3. Click markers to see details

### Analyzing Data:

1. Click "Statistics"
2. View interactive charts
3. See recent activity

---

## 🔧 Configuration

### Theme Colors (Dark Mode):
Located in `config/settings.py`:
- Primary: #1E3A8A (Dark Blue)
- Secondary: #3B82F6 (Blue)
- Background: #0F172A (Dark Navy)
- Surface: #1E293B (Dark Slate)

### Tags:
Default tags in `config/settings.py`:
- Severity: Severe, Moderate, Minor
- Location Type: Highway, Residential, Commercial
- Priority: Urgent, Maintenance, Safety Hazard

### File Upload:
- Max file size: 10 MB
- Allowed formats: JPG, JPEG, PNG, GIF, WEBP
- Max images per complaint: 6 (displayed)

---

## 📊 Database Schema

### Complaints Table:
```sql
id                      INTEGER PRIMARY KEY
photo_path             TEXT (semicolon-separated for multiple)
location               TEXT
latitude               REAL
longitude              REAL
tags                   TEXT (comma-separated)
description            TEXT
created_at             TIMESTAMP
status                 TEXT (pending/in_progress/resolved)
resolved_at            TIMESTAMP
resolution_time_hours  REAL
```

---

## 🎨 Dark Theme Details

- **Background**: Deep navy (#0F172A)
- **Cards**: Dark slate (#1E293B)
- **Primary**: Blue (#3B82F6)
- **Text**: Light (#F1F5F9)
- **Borders**: Subtle gray (#334155)

All components optimized for dark theme:
- Maps use dark tiles
- Charts use dark backgrounds
- Status badges have vibrant colors
- Smooth transitions and shadows

---

## 🚀 Performance Tips

1. **Images**: Auto-optimized to 1920x1080 max
2. **Database**: Indexed for fast queries
3. **Maps**: Marker clustering for >20 complaints
4. **Loading**: Background processing with spinners

---

## 🐛 Common Issues

**Issue**: Maps not showing
- **Solution**: Install `folium` and `streamlit-folium`

**Issue**: GPS extraction fails
- **Solution**: Ensure photo has EXIF data

**Issue**: Export button not working
- **Solution**: Install `openpyxl`

**Issue**: Charts not rendering
- **Solution**: Install `plotly`

---

## 📱 Mobile Responsiveness

The app is responsive and works on:
- Desktop (optimal)
- Tablets
- Mobile phones
- Different screen sizes

---

## 🔐 Security Notes

- SQLite database stored locally
- No external API calls (except maps tiles)
- Photo files stored in local `data/uploads/`
- No user authentication (can be added)

---

## 🎓 Learning Resources

**Streamlit**: https://docs.streamlit.io
**Folium**: https://python-visualization.github.io/folium/
**Plotly**: https://plotly.com/python/

---

## ✨ What's Next?

Consider adding:
- User authentication
- Email notifications (infrastructure ready)
- Admin dashboard
- API endpoints
- Mobile app
- AI pothole detection
- Government integration

---

**You're all set! Happy pothole reporting! 🛣️**
