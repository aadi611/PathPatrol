# 🚀 PathPatrol - Start Here!

Welcome to **PathPatrol** - your pothole complaint portal!

## 📋 What You Need to Do

### Step 1: Create Virtual Environment
```powershell
python -m venv venv
```

### Step 2: Activate Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an error, run this first:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**CMD:**
```cmd
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the App
```powershell
streamlit run app.py
```

## ✨ Or Use The Run Scripts

**PowerShell:**
```powershell
.\run.ps1
```

**Command Prompt:**
```cmd
run.bat
```

These scripts will:
- Check if venv exists (create if not)
- Activate the virtual environment
- Install dependencies if needed
- Launch the application

## 🎯 What You'll Get

A fully functional pothole reporting system with:

✅ **Photo Upload** - Take or upload pothole photos  
✅ **Location Entry** - Add address and GPS coordinates  
✅ **Tagging System** - Categorize potholes (Severe, Urgent, etc.)  
✅ **Status Tracking** - Pending → In Progress → Resolved  
✅ **Statistics Dashboard** - View analytics  
✅ **Dual Themes** - Light (white/blue) and Dark (navy/blue)  
✅ **Responsive Design** - Works on all devices  

## 🌐 Access the App

Once running, open your browser to:
```
http://localhost:8501
```

The app should open automatically!

## 📚 Learn More

- **[SETUP.md](SETUP.md)** - Complete setup guide with troubleshooting
- **[QUICKSTART.md](QUICKSTART.md)** - Feature walkthrough and usage
- **[README.md](README.md)** - Full documentation and architecture

## 🎨 Application Features

### Submit Complaints
1. Click "Submit Complaint" in sidebar
2. Upload pothole photo
3. Enter location
4. Select tags
5. Submit!

### View Complaints
1. Click "View Complaints" in sidebar
2. Filter by tags or status
3. Update statuses
4. Delete if needed

### Statistics
1. Click "Statistics" in sidebar
2. View total complaints
3. See breakdown by status
4. Check recent activity

### Theme Toggle
- Use the theme button in sidebar
- Switch between light and dark modes
- Setting persists during session

## 🔧 Tech Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **SQLite** - Database
- **Pillow** - Image processing
- **Pandas** - Data manipulation

## 📁 Project Structure

```
govt_assist_road/
├── app.py              ← Main application
├── requirements.txt    ← Dependencies
├── run.ps1            ← PowerShell launcher
├── run.bat            ← CMD launcher
├── config/            ← Settings & themes
├── database/          ← SQLite + models
├── services/          ← Business logic
├── ui/                ← Components + styles
└── data/              ← Database & uploads
```

## ❓ Having Issues?

### Virtual Environment Won't Activate
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8501 Already in Use
```powershell
streamlit run app.py --server.port 8502
```

### Dependencies Won't Install
Make sure venv is activated (you should see `(venv)` in terminal)

### App Won't Start
Check Python version: `python --version` (need 3.8+)

## 🎉 You're All Set!

Run the app and start reporting potholes to make your roads safer!

---

**PathPatrol** - *Empowering citizens, improving infrastructure*
