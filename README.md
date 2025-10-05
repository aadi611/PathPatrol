# Pothole Complaint Portal

A modern, minimal web application for reporting potholes with photo upload, location tracking, and tagging capabilities.

## Features

- 📸 Photo upload with camera support
- 📍 Location tracking (manual entry)
- 🏷️ Tag-based categorization
- 🌓 Light/Dark theme toggle
- 💾 Local SQLite database
- 📱 Responsive design
- 🎨 Modern UI with blue color scheme

## Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Modular Python architecture
- **Database**: SQLite (local storage)
- **Image Storage**: Local file system

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

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your browser
2. Toggle between Light/Dark theme
3. Upload a pothole photo
4. Enter location details
5. Add relevant tags
6. Submit the complaint
7. View all complaints in the gallery

## License

MIT License
