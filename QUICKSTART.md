# FoodPrice AI - Quick Start Guide

## One-Command Setup (Windows PowerShell)

Run this script to set up everything:

```powershell
# Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Quick Start - 5 Steps

### Step 1: Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Database Setup
```powershell
python manage.py migrate
python populate_initial_data.py
```

### Step 3: Start Backend
```powershell
python manage.py runserver
# Backend runs at: http://localhost:8000
```

### Step 4: Frontend (New PowerShell window)
```powershell
cd frontend
python -m http.server 8080
# Frontend runs at: http://localhost:8080
```

### Step 5: Start Redis & Celery (Optional, for background tasks)
```powershell
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A core worker -l info

# Terminal 3: Start Celery Beat
celery -A core beat -l info
```

## API Endpoints to Test

Open browser and visit:

- Dashboard: http://localhost:8080/index.html
- Cities API: http://localhost:8000/api/cities/
- Vegetables API: http://localhost:8000/api/vegetables/
- Current Prices: http://localhost:8000/api/current-prices/?city=Delhi
- Predictions: http://localhost:8000/api/prediction/?city=Delhi&item=Tomato&days=7
- Recommendations: http://localhost:8000/api/recommendation/?city=Delhi
- Insights: http://localhost:8000/api/insights/?city=Delhi&month=January

## Database Admin

```powershell
# Create superuser
python manage.py createsuperuser

# Access admin panel
# http://localhost:8000/admin/
```

## Troubleshooting

### Port Already in Use
```powershell
# Change Django port
python manage.py runserver 0.0.0.0:8001

# Change Frontend port
python -m http.server 8081
```

### Module Not Found
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Database Issues
```powershell
# Reset database
python manage.py migrate --run-syncdb
python manage.py migrate
```

## File Structure

```
project-root/
├── frontend/           # HTML/CSS/JS Dashboard
├── backend/            # Django REST API
├── ml/                 # ML Models (Prophet, ARIMA)
└── docs/               # Documentation
```

## Key Features

✅ Real-time price tracking
✅ AI-powered predictions
✅ Buy/Wait recommendations
✅ Price comparisons
✅ Market insights
✅ Savings calculator

## Documentation

See `docs/README.md` for detailed documentation.
