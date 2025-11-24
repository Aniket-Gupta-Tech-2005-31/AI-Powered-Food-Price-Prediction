"""
FoodPrice AI - Smart Buying Advisor
A comprehensive guide to setup and run the project
"""

# ========== PROJECT SETUP GUIDE ==========

## 1. INSTALLATION

### Prerequisites
- Python 3.8+
- Node.js (optional, for frontend development)
- Redis Server
- PostgreSQL (optional, for production)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
```

### Frontend Setup

The frontend is a simple HTML/CSS/JavaScript application. No build step required.

```bash
# Navigate to frontend directory
cd frontend

# Option 1: Use Python's built-in server
python -m http.server 8080

# Option 2: Use Live Server extension in VS Code
# Install "Live Server" extension, then right-click index.html and select "Open with Live Server"
```

### Celery Setup (for background tasks)

```bash
# Install Redis (if not already installed)
# On Windows: Download from https://github.com/microsoftarchive/redis/releases
# On Linux: sudo apt-get install redis-server
# On Mac: brew install redis

# Start Redis server
redis-server

# In a new terminal, start Celery worker
celery -A core worker -l info

# In another terminal, start Celery Beat scheduler
celery -A core beat -l info
```

## 2. DATABASE SCHEMA

The application uses the following models:

### City Model
- id (PrimaryKey)
- name (CharField)
- state (CharField)
- latitude (FloatField, optional)
- longitude (FloatField, optional)

### Vegetable Model
- id (PrimaryKey)
- name (CharField)
- category (CharField) - leafy, root, tomato, legume, other
- image_url (URLField, optional)
- description (TextField, optional)

### PriceEntry Model
- id (PrimaryKey)
- vegetable_id (ForeignKey to Vegetable)
- city_id (ForeignKey to City)
- price_per_kg (DecimalField)
- source (CharField) - bigbasket, jiomart, blinkit, local_market, government, other
- location (CharField)
- timestamp (DateTimeField)
- quality_rating (IntegerField) - 1 to 5

### Prediction Model
- id (PrimaryKey)
- vegetable_id (ForeignKey to Vegetable)
- city_id (ForeignKey to City)
- predicted_price (DecimalField)
- prediction_date (DateField)
- model_used (CharField) - prophet, arima, lstm, ensemble
- confidence (FloatField)
- lower_bound (DecimalField, optional)
- upper_bound (DecimalField, optional)

## 3. API ENDPOINTS

### Get All Cities
GET /api/cities/

### Get All Vegetables
GET /api/vegetables/

### Get Current Prices
GET /api/current-prices/?city=Delhi

### Get Price Comparison
GET /api/comparison/?city=Delhi&item=Tomato

### Get Predictions
GET /api/prediction/?city=Delhi&item=Tomato&days=7

### Get Recommendations
GET /api/recommendation/?city=Delhi

### Get Insights
GET /api/insights/?city=Delhi&month=January

## 4. ML MODEL USAGE

### Training Models

```python
from ml.train_model import train_all_models

# Train models for a vegetable-city combination
models = train_all_models(vegetable_id=1, city_id=1)
```

### Generating Predictions

```python
from ml.predict_price import generate_predictions

# Generate predictions for next 30 days
predictions = generate_predictions(
    vegetable_id=1,
    city_id=1,
    days=30,
    use_ensemble=True
)
```

### Data Preprocessing

```python
from ml.utils.preprocess import DataPreprocessor
import pandas as pd

# Preprocess price data
preprocessor = DataPreprocessor()
df = pd.read_csv('price_data.csv')
df_processed = preprocessor.preprocess(df)
```

## 5. RECOMMENDATION ENGINE

### Using Score-Based Engine

```python
from backend.recommendation.score_model import score_engine
from datetime import datetime

# Generate recommendation
rec = score_engine.generate_recommendation(
    current_price=45.50,
    predicted_price=42.00,
    trend=-0.15,
    confidence=0.85,
    vegetable_name='Tomato',
    month=datetime.now().month
)

print(rec['action'])  # 'Wait' or 'Buy Now'
print(rec['reason'])  # Reason for recommendation
```

## 6. DATA COLLECTION

### From Government APIs

```python
from backend.scraper.gov_api_fetch import fetch_government_prices

prices = fetch_government_prices()
```

### From Online Stores

```python
from backend.scraper.online_store_scraper import fetch_online_store_prices

prices = fetch_online_store_prices()
```

### Data Cleaning

```python
from backend.scraper.clean_data import clean_price_data

cleaned = clean_price_data(raw_prices)
```

## 7. SCHEDULED TASKS

The application uses Celery Beat to schedule daily tasks:

### Daily Tasks (Automated)
- **00:00** - Fetch price data from all sources
- **01:00** - Train ML models
- **02:00** - Generate predictions for next 30 days

### Manual Task Execution

```bash
# Run fetch task manually
python manage.py shell
from api.tasks import fetch_and_store_prices
result = fetch_and_store_prices.delay()
```

## 8. TROUBLESHOOTING

### CORS Issues
If frontend can't connect to backend:
1. Check CORS_ALLOWED_ORIGINS in settings.py
2. Ensure frontend URL is whitelisted

### Redis Connection Error
1. Verify Redis is running: `redis-cli ping`
2. Check REDIS_URL in .env

### Database Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Model Loading Error
Ensure Prophet and ARIMA models are trained before predictions:
```bash
python manage.py shell
from ml.train_model import train_all_models
train_all_models(1, 1)
```

## 9. PRODUCTION DEPLOYMENT

### Using Gunicorn

```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Environment Variables for Production

```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/foodprice
REDIS_URL=redis://redis-server:6379/0
```

## 10. TESTING

### Run Tests

```bash
python manage.py test api

# With coverage
coverage run --source='.' manage.py test api
coverage report
```

## 11. MONITORING

### View Logs

```bash
# Django logs
tail -f logs/django.log

# Celery logs
celery -A core events
```

## 12. FEATURES IMPLEMENTED

✅ Real-time price collection from multiple sources
✅ ML-based price predictions (Prophet + ARIMA)
✅ Smart buy/wait recommendations
✅ Price comparison across platforms
✅ Market insights and trends
✅ Savings calculator
✅ Modern responsive UI
✅ REST API endpoints
✅ Automated daily tasks with Celery
✅ Comprehensive error handling
✅ Logging and monitoring

## 13. FILE STRUCTURE

```
project-root/
├── frontend/
│   ├── index.html           # Main dashboard
│   ├── styles/
│   │   └── main.css         # All styling
│   ├── js/
│   │   └── app.js           # Frontend logic
│   ├── components/          # Reusable components
│   ├── pages/               # Page templates
│   └── assets/
│       └── images/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── core/
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # URL routing
│   │   ├── wsgi.py          # WSGI config
│   │   └── celery.py        # Celery config
│   │
│   ├── api/
│   │   ├── models.py        # Database models
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # DRF serializers
│   │   ├── urls.py          # API URLs
│   │   └── tasks.py         # Celery tasks
│   │
│   ├── scraper/
│   │   ├── gov_api_fetch.py
│   │   ├── online_store_scraper.py
│   │   ├── clean_data.py
│   │   └── save_to_db.py
│   │
│   └── recommendation/
│       ├── engine.py
│       ├── rule_based.py
│       └── score_model.py
│
├── ml/
│   ├── train_model.py
│   ├── predict_price.py
│   ├── dataset/
│   │   ├── raw_data.csv
│   │   ├── cleaned_data.csv
│   │   └── train_test_split/
│   ├── models/               # Trained models
│   │   ├── prophet_*.pkl
│   │   └── arima_*.pkl
│   └── utils/
│       ├── preprocess.py
│       └── evaluate.py
│
└── docs/
    └── README.md
```

## 14. NEXT STEPS

1. ✅ Project structure created
2. ✅ Frontend UI with HTML/CSS/JS
3. ✅ Django backend with APIs
4. ✅ Database models
5. ✅ Scraper modules
6. ✅ ML models (Prophet, ARIMA)
7. ✅ Recommendation engine
8. ⏳ Deploy to cloud (AWS, Azure, or Heroku)
9. ⏳ Add real data from APIs
10. ⏳ Setup monitoring and alerts

## 15. SUPPORT & DOCUMENTATION

For detailed information about each component:
- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- Prophet: https://facebook.github.io/prophet/
- Celery: https://docs.celeryproject.io/
- Pandas: https://pandas.pydata.org/docs/

---

**Project**: AI-Powered Food Price Prediction & Smart Buying Advisor
**Version**: 1.0.0
**Last Updated**: November 2024
