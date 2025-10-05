# Pothole Complaint Portal

A modern, minimal web application for reporting potholes with photo upload, location tracking, and tagging capabilities.

## ✨ Features

- 📸 **Photo Upload**: Capture and upload pothole images
- 📍 **Location Tracking**: Manual address entry with optional GPS coordinates
- 🏷️ **Smart Tagging**: Categorize by severity, location type, and urgency
- 🌓 **Dual Themes**: Modern light and dark themes (white/blue & navy/blue)
- 💾 **Local Storage**: SQLite database with local file system
- � **Statistics Dashboard**: Real-time analytics and complaint tracking
- �📱 **Responsive Design**: Works seamlessly on all devices
- 🎨 **Modern UI**: Clean, symmetric, minimal interface

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit + Custom CSS/HTML |
| Backend | Modular Python Framework |
| Database | SQLite (Local Storage) |
| Image Processing | Pillow (PIL) |
| Data Handling | Pandas |

## Project Structure

```
govt_assist_road/
├── app.py                  # Main Streamlit application
├── config/
│   └── settings.py         # Configuration settings
├── database/
│   ├── __init__.py
│   ├── models.py          # Database models
│   └── db_manager.py      # Database operations
├── services/
│   ├── __init__.py
│   ├── complaint_service.py  # Business logic
│   └── storage_service.py    # File storage logic
├── ui/
│   ├── __init__.py
│   ├── styles.py          # CSS styling
│   └── components.py      # UI components
├── utils/
│   └── __init__.py
├── data/
│   ├── complaints.db      # SQLite database
│   └── uploads/           # Uploaded images
└── requirements.txt
```

## 🚀 Quick Start

### Option 1: PowerShell Script (Recommended)
```powershell
.\run.ps1
```

### Option 2: Batch File
```cmd
run.bat
```

### Option 3: Manual Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (CMD)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Feature guide and usage

## 🎯 Use Cases

- **Citizens**: Report potholes in your neighborhood
- **Municipal Teams**: Track and manage road repairs
- **Community Groups**: Organize road safety initiatives
- **Infrastructure Planning**: Data-driven maintenance decisions

## 🏗️ Architecture

**Modular Python Framework** with clean separation of concerns:

- **Config Layer**: Centralized settings and theme management
- **Database Layer**: SQLite with clean data models
- **Service Layer**: Business logic and file storage
- **UI Layer**: Reusable components with modern CSS
- **Utils Layer**: Shared utilities and helpers

**Scalable & Maintainable** - Easy to extend with new features

## 🎨 Themes

### Light Theme
- Clean white background
- Professional blue accents (#2E86DE, #54A0FF)
- High contrast for readability

### Dark Theme
- Navy background (#0F172A)
- Elegant blue highlights (#3B82F6, #60A5FA)
- Comfortable for extended use

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit + Custom CSS/HTML |
| Backend | Modular Python Framework |
| Database | SQLite (Local Storage) |
| Image Processing | Pillow (PIL) |
| Data Handling | Pandas |

## 📦 Requirements

- Python 3.8+
- streamlit==1.28.0
- Pillow==10.1.0
- pandas==2.1.1

## 🔧 Configuration

Customize the app by editing `config/settings.py`:

```python
# Theme colors
THEMES = {
    "light": {...},
    "dark": {...}
}

# Default tags
DEFAULT_TAGS = [
    "Severe", "Moderate", "Minor",
    "Highway", "Residential", "Commercial",
    "Urgent", "Maintenance", "Safety Hazard"
]

# Upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
```

## 📊 Database Schema

```sql
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_path TEXT NOT NULL,
    location TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    tags TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
)
```

## 🚀 Roadmap

- [ ] User authentication and profiles
- [ ] Email notifications for status updates
- [ ] Map view with geolocation clustering
- [ ] Export reports (PDF, Excel)
- [ ] Mobile app (React Native)
- [ ] Admin dashboard
- [ ] API for third-party integrations
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with ❤️ for safer roads and better communities.

---

**PathPatrol** - *Empowering citizens, improving infrastructure*
