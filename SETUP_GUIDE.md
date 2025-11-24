# 🥬 FoodPrice AI - Complete Step-by-Step Setup Guide

A complete guide to set up and run the **FoodPrice AI** project from scratch using PowerShell (Windows).

---

## 📋 Prerequisites

Before you start, make sure you have installed:

1. **Python 3.8+** — [Download](https://www.python.org/downloads/)
2. **A terminal** — Use PowerShell on Windows

**Check installation:**
```powershell
python --version
pip --version
```

---

## 🚀 Complete Setup (Copy & Paste)

### Step 1: Navigate to Project Directory

Open PowerShell and go to your project folder:

```powershell
cd "d:\Aniket Data\PROJECTS\WEB PROJECT\New folder (2)"
```

### Step 2: Create Virtual Environment

Create an isolated Python environment:

```powershell
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate
```

**You should see `(.venv)` in your terminal prompt.**

### Step 4: Install Backend Dependencies

```powershell
pip install -r backend/requirements.txt
```

**Wait for installation to complete (takes ~2-3 minutes).**

### Step 5: Navigate to Backend Folder

```powershell
cd backend
```

### Step 6: Set Up Database

```powershell
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying api.0001_initial... OK
```

### Step 7: (Optional) Create Admin User

```powershell
python manage.py createsuperuser
```

**Follow the prompts to create username, email, and password.**

### Step 8: Load Sample Data

Load test data so you can see the app in action:

```powershell
python populate_price_data.py
python populate_predictions.py
```

**Expected output:**
```
Created 50 sample price entries...
Created 20 predictions...
```

---

## ▶️ Running the Application

### Terminal 1: Start Backend Server

**Keep this terminal open while using the app.**

```powershell
cd backend
python manage.py runserver 8000
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Terminal 2: Start Frontend Server

**Open a NEW PowerShell window:**

```powershell
cd "d:\Aniket Data\PROJECTS\WEB PROJECT\New folder (2)\frontend"
python -m http.server 8001
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 8001 (http://0.0.0.0:8001/) ...
```

### Step 3: Open in Browser

Open your web browser and go to:

```
http://localhost:8001
```

**You should see the FoodPrice AI dashboard! 🎉**

---

## 📱 Using the Application

### Dashboard (Default Page)
1. Select a **City** from the top-left dropdown
2. Select a **Vegetable** from the "All Items" filter
3. Click **Refresh Data** to load prices
4. View current prices, recommendations, and savings

### Compare Prices
1. Go to **Compare Prices** tab
2. Select an item
3. (Optional) Set date range, state, sort
4. Click **Apply**
5. See comparison cards with best price highlighted

### Predictions
1. Go to **Predictions** tab
2. Select a vegetable
3. Choose timeframe (7, 14, or 30 days)
4. View the interactive line chart with AI predictions

### Insights
1. Go to **Insights** tab
2. Select a month
3. See average/min/max prices with bar charts
4. Check trend indicators (rising/falling/stable)

### Report Price
1. Click **Report Price** button in navbar
2. Fill in: Item, Price, City, Quality
3. (Optional) Add source
4. Click **Submit Price**
5. Modal closes and dashboard refreshes

---

## 🔌 Testing the API (Optional)

### Test Current Prices Endpoint

Open PowerShell and run:

```powershell
curl -X GET "http://localhost:8000/api/current-prices/?city=Delhi" -H "Content-Type: application/json"
```

### Test Submit Price Endpoint

```powershell
$body = @{
    vegetable_name = "Tomato"
    city_name = "Delhi"
    price_per_kg = 35.50
    source = "User"
    quality_rating = 4
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/submit-price/" `
  -H "Content-Type: application/json" `
  -d $body
```

---

## 🛑 Stopping the Application

To stop either server:

```powershell
# Press Ctrl+C in the terminal where the server is running
```

---

## 📊 Database Inspection (Optional)

To view the database directly:

```powershell
cd backend
python manage.py dbshell
```

**Useful SQL commands:**

```sql
-- View all prices
SELECT * FROM api_priceentry LIMIT 10;

-- View all vegetables
SELECT * FROM api_vegetable;

-- Count total prices
SELECT COUNT(*) FROM api_priceentry;

-- Exit
.exit
```

---

## 🔧 Common Issues & Solutions

### Issue 1: `ModuleNotFoundError: No module named 'django'`

**Solution:**
```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Issue 2: `django.core.exceptions.ImproperlyConfigured`

**Solution:**
```powershell
cd backend
python manage.py migrate
```

### Issue 3: Database not found

**Solution:**
```powershell
cd backend
python manage.py migrate
python populate_price_data.py
```

### Issue 4: Port 8000 or 8001 already in use

**Solution - Use different ports:**

```powershell
# Backend on port 8080
python manage.py runserver 8080

# Frontend on port 8002
python -m http.server 8002
# Then open http://localhost:8002
```

### Issue 5: "Connection refused" in frontend

**Make sure both servers are running:**
- Backend: `python manage.py runserver 8000`
- Frontend: `python -m http.server 8001`

### Issue 6: Charts not showing

**Hard refresh the browser:**
- **Windows**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`

### Issue 7: Modal (Report Price) won't close

**Solution:**
```powershell
# Hard refresh browser
Ctrl + Shift + R
```

---

## 📚 What's Next?

After the app is running:

1. **Explore the dashboard** - Click through different pages
2. **Submit a price** - Click "Report Price" and add data
3. **Check predictions** - Go to Predictions and see AI forecasts
4. **Read the code** - Check `frontend/js/app.js` and `backend/api/views.py`
5. **Customize** - Modify colors, add features, integrate real data

---

## 📖 Additional Guides

For more detailed information, check these files:

- **Quick overview**: Read this file (SETUP_GUIDE.md)
- **Project structure**: See `README.md`
- **API documentation**: Open `http://localhost:8000/api/` in browser
- **Django admin**: Go to `http://localhost:8000/admin/` (login with superuser)

---

## 🎯 Project Features

✅ **Dashboard** - View current prices and recommendations
✅ **Comparisons** - Compare prices across cities and sources
✅ **Predictions** - AI-powered 30-day price forecasts
✅ **Insights** - Market trends and analytics
✅ **Submit Prices** - Crowd-source price data
✅ **Charts** - Interactive visualizations
✅ **Filters** - By city, vegetable, date range
✅ **Mobile-friendly** - Responsive design

---

## 🔌 API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/api/cities/` | List all cities |
| GET | `/api/vegetables/` | List all items |
| GET | `/api/current-prices/?city=Delhi` | Current prices |
| GET | `/api/comparison/?item=Tomato&city=Delhi` | Compare prices |
| GET | `/api/prediction/?city=Delhi&item=Tomato&days=7` | Price forecast |
| GET | `/api/recommendation/?city=Delhi` | Buy/Wait advice |
| GET | `/api/insights/?city=Delhi&month=January` | Market trends |
| POST | `/api/submit-price/` | Add custom price |

---

## 💡 Tips & Tricks

### Tip 1: Quick Reset

Clear sample data and start fresh:

```powershell
cd backend
python manage.py flush
python populate_price_data.py
```

### Tip 2: Check Backend Logs

Keep backend terminal open to see API requests and errors.

### Tip 3: Use Browser DevTools

- **Network tab** - See API requests
- **Console tab** - Check for JS errors
- **Elements tab** - Inspect HTML/CSS

### Tip 4: Test with curl

```powershell
# Get all vegetables
curl http://localhost:8000/api/vegetables/

# Get current prices for Delhi
curl http://localhost:8000/api/current-prices/?city=Delhi
```

---

## 🚀 Deployment (Production)

When you're ready to deploy:

1. Set `DEBUG=False` in `backend/core/settings.py`
2. Set a strong `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Use a real web server (Gunicorn, Nginx)
5. Enable HTTPS
6. Set environment variables

See `README.md` for more info.

---

## 📞 Help & Support

**If something goes wrong:**

1. Check the **Troubleshooting** section above
2. Make sure **both servers are running** (backend + frontend)
3. **Hard refresh** the browser (`Ctrl+Shift+R`)
4. Check **browser console** for errors
5. Check **backend terminal** for errors
6. Look at **database** with `python manage.py dbshell`

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated (see `(.venv)` in terminal)
- [ ] Backend server running at `http://localhost:8000`
- [ ] Frontend server running at `http://localhost:8001`
- [ ] Can open `http://localhost:8001` in browser
- [ ] Dashboard shows prices and recommendations
- [ ] Can select city and vegetable
- [ ] Can click "Report Price" and submit a price
- [ ] Charts display on Predictions and Insights pages
- [ ] Can navigate between Dashboard, Compare, Predictions, Insights

---

## 🎉 Success!

If all checks pass, you have successfully set up **FoodPrice AI**! 

**Next steps:**
1. Explore the application
2. Read the code to understand how it works
3. Customize it for your needs
4. Deploy to production when ready

---

## 📄 File Locations

| Component | Location | Type |
|-----------|----------|------|
| Frontend | `frontend/` | HTML/CSS/JS |
| Backend | `backend/` | Django app |
| Database | `backend/db.sqlite3` | SQLite |
| ML Models | `ml/` | Python |
| Config | `.env` | Environment |

---

## 🔐 Environment Variables

Optional settings in `backend/.env`:

```
DEBUG=True
SECRET_KEY=your-secret-key
FETCH_API_KEY=your-api-key
CELERY_BROKER_URL=redis://localhost:6379
DATABASE_URL=sqlite:///db.sqlite3
```

---

## 📞 Quick Links

| Resource | Link |
|----------|------|
| Frontend | http://localhost:8001 |
| Backend API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |
| Project Root | `d:\Aniket Data\PROJECTS\WEB PROJECT\New folder (2)` |

---

**Happy Price Tracking! 🥬📊**

*Last updated: November 2024*
