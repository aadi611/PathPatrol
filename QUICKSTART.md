# Quick Start Guide

## Installation Steps

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**
   - The app will automatically open in your browser
   - Default URL: http://localhost:8501

## Features Overview

### Submit Complaint Page
- Upload pothole photo (JPG, PNG, GIF, WebP)
- Enter location/address
- Optional GPS coordinates
- Add tags for categorization
- Add description

### View Complaints Page
- Browse all submitted complaints
- Filter by tags
- Filter by status (Pending, In Progress, Resolved)
- Update complaint status
- Delete complaints

### Statistics Page
- Total complaints count
- Breakdown by status
- Recent activity

## Theme Toggle
- Switch between Light and Dark themes
- Located in the sidebar
- Persists during session

## Project Architecture

### Modular Structure
```
Backend Layer:
├── database/          # Data persistence
│   ├── models.py     # Data models
│   └── db_manager.py # Database operations

├── services/         # Business logic
│   ├── complaint_service.py
│   └── storage_service.py

Frontend Layer:
├── ui/              # User interface
│   ├── styles.py   # CSS styling
│   └── components.py # UI components

Configuration:
└── config/
    └── settings.py  # App settings
```

### Design Principles
- **Separation of Concerns**: Each module has a single responsibility
- **Scalability**: Easy to add new features
- **Maintainability**: Clean, documented code
- **Modularity**: Components can be reused

## Customization

### Change Colors
Edit `config/settings.py` -> `THEMES` dictionary

### Add More Tags
Edit `config/settings.py` -> `DEFAULT_TAGS` list

### Modify Database Schema
Edit `database/models.py` and `database/db_manager.py`

## Database Location
- SQLite database: `data/complaints.db`
- Uploaded images: `data/uploads/`

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Clear Cache
```bash
streamlit cache clear
```

### Reset Database
Delete `data/complaints.db` file (will be recreated on next run)

## Production Deployment

For production use, consider:
1. Use PostgreSQL instead of SQLite
2. Implement user authentication
3. Add API rate limiting
4. Use cloud storage for images (S3, Azure Blob)
5. Add input validation and sanitization
6. Implement logging and monitoring
