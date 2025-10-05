# 🚧 PathPatrol - Setup Guide

A modern pothole complaint portal built with Python and Streamlit.

## 🚀 Quick Start

### 1. Create Virtual Environment

```powershell
# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the Application

```powershell
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
govt_assist_road/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py        # App settings and theme colors
├── database/              # Database layer
│   ├── __init__.py
│   ├── db_manager.py     # SQLite operations
│   └── models.py         # Data models
├── services/              # Business logic
│   ├── __init__.py
│   ├── complaint_service.py
│   └── storage_service.py
├── ui/                    # User interface
│   ├── __init__.py
│   ├── components.py     # UI components
│   └── styles.py         # CSS themes
├── utils/                 # Utilities
│   └── __init__.py
└── data/                  # Data storage
    ├── uploads/          # Photo storage
    └── complaints.db     # SQLite database
```

## ✨ Features

- 📸 **Photo Upload**: Click and upload pothole photos
- 📍 **Location Tracking**: Add location and GPS coordinates
- 🏷️ **Tag System**: Categorize with tags (Severe, Highway, Urgent, etc.)
- 📊 **Statistics Dashboard**: View complaint analytics
- 🌓 **Dark/Light Themes**: Modern blue-based themes
- 💾 **Local Storage**: SQLite database with file storage
- 📱 **Responsive Design**: Works on all devices

## 🎨 Themes

The application includes two beautiful themes:

### Light Theme
- White background with blue accents
- Clean and professional look

### Dark Theme  
- Dark navy background with blue highlights
- Easy on the eyes for night use

Toggle themes using the sidebar button.

## 🔧 Configuration

Edit `config/settings.py` to customize:

- Database path
- Upload directory
- File size limits
- Allowed file types
- Default tags
- Theme colors

## 📝 Usage

### Submit a Complaint

1. Click "Submit Complaint" in sidebar
2. Upload a pothole photo
3. Enter location/address
4. Optionally add GPS coordinates
5. Select relevant tags
6. Add description
7. Click "Submit Complaint"

### View Complaints

1. Click "View Complaints" in sidebar
2. Filter by tags or status
3. Update status or delete complaints

### View Statistics

1. Click "Statistics" in sidebar
2. See total, pending, in progress, and resolved complaints
3. View recent activity

## 🛠️ Development

### Modular Architecture

- **Config**: Centralized settings
- **Database**: Clean data layer with models
- **Services**: Business logic separation
- **UI**: Reusable components
- **Utils**: Shared utilities

### Adding New Features

1. Add data models in `database/models.py`
2. Add database operations in `database/db_manager.py`
3. Add business logic in `services/`
4. Add UI components in `ui/components.py`
5. Update styles in `ui/styles.py`

## 📦 Dependencies

- **streamlit**: Web framework
- **Pillow**: Image processing
- **pandas**: Data manipulation (optional)

## 🐛 Troubleshooting

### Port Already in Use
```powershell
streamlit run app.py --server.port 8502
```

### Database Issues
Delete `data/complaints.db` and restart the app.

### Virtual Environment Issues
Make sure venv is activated (you should see `(venv)` in your terminal).

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve!

---

**Made with ❤️ using Python and Streamlit**
