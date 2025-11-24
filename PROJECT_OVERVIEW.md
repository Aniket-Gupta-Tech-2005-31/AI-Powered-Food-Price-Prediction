# 🥬 FoodPrice AI - Complete Project Overview

## Executive Summary

**FoodPrice AI** is a full-stack web application that helps users make smart grocery shopping decisions through:
- Real-time vegetable price tracking across multiple sources
- AI-powered price predictions using Prophet & ARIMA models
- Smart buy/wait recommendations
- Market insights and savings calculations

---

## 📁 Project Structure

```
project-root/
│
├── 🎨 frontend/
│   ├── index.html              # Main dashboard
│   ├── styles/
│   │   └── main.css            # All styling (modern, gradient UI)
│   ├── js/
│   │   └── app.js              # Frontend logic, API calls, DOM updates
│   ├── components/             # Reusable UI components
│   ├── pages/                  # Page templates
│   └── assets/images/          # Images and media
│
├── 🔧 backend/
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python dependencies
│   ├── populate_initial_data.py
│   ├── Dockerfile
│   │
│   ├── core/                   # Django project config
│   │   ├── settings.py         # All settings (CORS, Celery, DB, etc.)
│   │   ├── urls.py             # URL routing to APIs
│   │   ├── wsgi.py             # WSGI entry point
│   │   └── celery.py           # Celery configuration
│   │
│   ├── api/                    # Main API application
│   │   ├── models.py           # 5 models: City, Vegetable, PriceEntry, Prediction, UserFeedback
│   │   ├── views.py            # 8 API endpoints + custom views
│   │   ├── serializers.py      # DRF serializers for API responses
│   │   ├── urls.py             # API URL patterns
│   │   ├── tasks.py            # Celery tasks (fetch, train, predict)
│   │   ├── admin.py            # Django admin interface
│   │   ├── apps.py             # App configuration
│   │   └── tests.py            # Unit tests
│   │
│   ├── scraper/                # Data collection modules
│   │   ├── gov_api_fetch.py    # Government API (Agmarknet, OGD)
│   │   ├── online_store_scraper.py  # BigBasket, JioMart, Blinkit
│   │   ├── clean_data.py       # Data cleaning & validation
│   │   ├── save_to_db.py       # Store to database
│   │   └── __init__.py         # Module initialization
│   │
│   └── recommendation/         # Recommendation engine
│       ├── engine.py           # Main recommendation orchestrator
│       ├── rule_based.py       # Rule-based recommendations
│       ├── score_model.py      # Score-based weighted model
│       └── __init__.py
│
├── 🤖 ml/
│   ├── train_model.py          # Prophet & ARIMA training
│   ├── predict_price.py        # Prediction generation & storage
│   │
│   ├── dataset/
│   │   ├── raw_data.csv        # Raw price data
│   │   ├── cleaned_data.csv    # Preprocessed data
│   │   └── train_test_split/   # Split datasets
│   │
│   ├── models/                 # Trained model files
│   │   ├── prophet_*.pkl       # Prophet models
│   │   └── arima_*.pkl         # ARIMA models
│   │
│   └── utils/
│       ├── preprocess.py       # Data preprocessing pipeline
│       └── evaluate.py         # Model evaluation metrics
│
├── 📚 docs/
│   └── README.md               # Complete documentation
│
├── 🐳 Docker files
│   ├── docker-compose.yml      # Full stack container setup
│   └── backend/Dockerfile      # Backend container image
│
├── 🚀 Setup scripts
│   ├── setup.bat               # Windows setup
│   ├── setup.sh                # Linux/Mac setup
│   ├── QUICKSTART.md           # Quick start guide
│   └── PROJECT_OVERVIEW.md     # This file
│
└── Configuration
    ├── .env.example            # Environment variables template
    └── requirements.txt        # Python dependencies
```

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Structure
- **CSS3** - Modern styling (gradients, flexbox, grid)
- **Vanilla JavaScript** - No frameworks, lightweight
- **Fetch API** - HTTP requests to backend
- **Features**: Responsive design, real-time updates, smooth animations

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Celery** - Async task queue
- **Redis** - Message broker & caching
- **Gunicorn** - Production server
- **PostgreSQL** - Database (sqlite for dev)

### Machine Learning
- **Prophet** - Seasonal time series forecasting
- **ARIMA** - AutoRegressive Integrated Moving Average
- **Scikit-learn** - ML utilities
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy (production)
- **Git** - Version control

---

## 🗄️ Database Schema

### City Model
```python
- id: Primary Key
- name: String (unique)
- state: String
- latitude: Float (nullable)
- longitude: Float (nullable)
- timestamps: Auto
```

### Vegetable Model
```python
- id: Primary Key
- name: String (unique)
- category: Choices [leafy, root, tomato, legume, other]
- image_url: URL (nullable)
- description: Text (nullable)
- timestamps: Auto
```

### PriceEntry Model
```python
- id: Primary Key
- vegetable_id: ForeignKey(Vegetable)
- city_id: ForeignKey(City)
- price_per_kg: Decimal(8,2)
- source: Choices [bigbasket, jiomart, blinkit, local_market, government, other]
- location: String
- timestamp: DateTime
- quality_rating: Integer(1-5)
- Indexed on: [vegetable, city, timestamp]
```

### Prediction Model
```python
- id: Primary Key
- vegetable_id: ForeignKey(Vegetable)
- city_id: ForeignKey(City)
- predicted_price: Decimal(8,2)
- prediction_date: Date
- model_used: Choices [prophet, arima, lstm, ensemble]
- confidence: Float(0.0-1.0)
- lower_bound: Decimal(8,2) (confidence interval)
- upper_bound: Decimal(8,2) (confidence interval)
- created_at: DateTime
- Indexed on: [vegetable, city, prediction_date]
```

### UserFeedback Model
```python
- id: Primary Key
- user_ip: IPAddress
- feedback_type: Choices [recommendation_useful, price_accurate, etc.]
- vegetable_id: ForeignKey (nullable)
- city_id: ForeignKey (nullable)
- comment: Text
- created_at: DateTime
```

---

## 🔌 API Endpoints

### All endpoints return JSON

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cities/` | List all cities |
| GET | `/api/vegetables/` | List all vegetables |
| GET | `/api/price-entries/` | List all price entries with filters |
| GET | `/api/predictions/` | List predictions with filters |
| GET | `/api/current-prices/?city=Delhi` | Get latest prices for city |
| GET | `/api/comparison/?city=Delhi&item=Tomato` | Compare prices across sources |
| GET | `/api/prediction/?city=Delhi&item=Tomato&days=7` | Get price predictions |
| GET | `/api/recommendation/?city=Delhi` | Get buy/wait recommendations |
| GET | `/api/insights/?city=Delhi&month=January` | Get market insights |

---

## 🤖 ML Pipeline

### 1. Data Collection
```
Government APIs → Online Scrapers → Data Cleaning → Database
```

### 2. Model Training
```
Historical Prices → Preprocessing → Prophet Training + ARIMA Training
                                  ↓
                            Models Saved (PKL)
```

### 3. Prediction Generation
```
Saved Models → Generate Forecasts → Ensemble Combine → Store in DB
```

### 4. Recommendation
```
Current Price + Predicted Price + Trend + Seasonality → Score Calculation → Action
```

---

## 📊 Recommendation Engine Logic

### Score-Based Recommendation
```
Score = (Price_Change × 0.4) + (Trend × 0.25) + (Seasonality × 0.15) × Confidence_Boost

If Score > 0.15 → "Wait" (prices dropping)
If Score < -0.15 → "Buy Now" (prices rising)
Else → "Buy Now" (stable)
```

### Factors Considered
- **Price Change**: Expected % change in price
- **Trend**: Historical trend direction (-1 to +1)
- **Seasonality**: Seasonal price patterns
- **Confidence**: Model prediction confidence
- **Potential Savings**: Calculated savings from waiting

---

## ⏰ Scheduled Tasks (Celery Beat)

| Time | Task | Frequency |
|------|------|-----------|
| 00:00 | Fetch price data from all sources | Daily |
| 01:00 | Train ML models | Daily |
| 02:00 | Generate predictions (30 days) | Daily |

---

## 🚀 Deployment Options

### Option 1: Local Development
```bash
python manage.py runserver  # Django
python -m http.server 8080  # Frontend
redis-server                # Redis
celery -A core worker       # Celery
```

### Option 2: Docker Compose
```bash
docker-compose up
# All services start automatically
```

### Option 3: Cloud Deployment
- **AWS**: EC2 + RDS + ElastiCache
- **Azure**: App Service + Database + Redis
- **Heroku**: Simple push deployment
- **DigitalOcean**: Droplets + Managed Database

---

## 📈 Key Features Implemented

✅ **Real-Time Price Tracking**
- Multiple data sources
- Automatic updates every day
- Quality ratings

✅ **ML-Based Predictions**
- Prophet (seasonal forecasting)
- ARIMA (short-term forecasting)
- Ensemble method (combines both)
- Confidence intervals

✅ **Smart Recommendations**
- Buy Now vs Wait decisions
- Potential savings calculation
- Confidence levels
- Seasonal adjustments

✅ **Market Intelligence**
- Price trends analysis
- Seasonal patterns
- Multi-month insights
- Comparative analytics

✅ **User Experience**
- Modern responsive UI
- Real-time data updates
- Interactive charts
- Savings calculator
- City & item selectors

✅ **Scalability**
- Modular architecture
- Microservices ready
- Async task processing
- Redis caching
- Database indexing

---

## 🔐 Security Features

- CORS configuration for cross-origin requests
- Environment variables for sensitive data
- Input validation & sanitization
- SQL injection prevention (ORM)
- Rate limiting ready
- HTTPS ready (production)
- Admin authentication

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   USER INTERFACE                        │
│            (HTML/CSS/JavaScript Frontend)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────┐
        │   Django REST API          │
        │  (localhost:8000/api)      │
        └────────┬────────┬──────────┘
                 │        │
         ┌───────┴─────┬──┴────────┐
         ↓             ↓           ↓
    ┌─────────┐  ┌─────────┐  ┌──────────┐
    │ Database│  │ Scraper │  │ ML Model │
    │(SQLite) │  │ Module  │  │ (Prophet)│
    └─────────┘  └────┬────┘  └──────────┘
                      │
         ┌────────────┬┴────────────┐
         ↓            ↓             ↓
    Government  Online Stores  Local Data
```

---

## 🎯 Use Cases

### For Individual Users
- Check best prices before shopping
- Get alerts when prices drop
- Save money with smart recommendations
- Track price trends

### For Students & Families
- Budget planning for groceries
- Weekly shopping optimization
- Seasonal buying patterns
- Multi-city price comparison

### For Small Retailers
- Understand market pricing
- Competitive analysis
- Seasonal forecasting
- Supplier negotiation

---

## 📝 Setup Instructions

### Quick Start (5 minutes)

#### Windows PowerShell
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then in new terminal:
```powershell
cd frontend
python -m http.server 8080
```

#### Linux/Mac
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then in new terminal:
```bash
cd frontend
python -m http.server 8080
```

### Detailed Setup
See `QUICKSTART.md` and `docs/README.md`

---

## 🧪 Testing

### Backend Tests
```bash
python manage.py test api

# With coverage
coverage run --source='.' manage.py test api
coverage report
```

### API Testing
```bash
# Using curl
curl http://localhost:8000/api/cities/

# Using Postman
Import `api-collection.json` (create this)
```

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/your-feature`
5. Create Pull Request

---

## 📞 Support

- **Issues**: Use GitHub Issues
- **Questions**: Create Discussions
- **Bugs**: Submit detailed bug reports
- **Features**: Request in Issues

---

## 📄 License

This project is open source and available under MIT License.

---

## 🎉 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | ✅ Complete | Responsive dashboard ready |
| Backend API | ✅ Complete | All endpoints implemented |
| Database | ✅ Complete | Schema & models ready |
| ML Models | ✅ Complete | Prophet & ARIMA integrated |
| Scraper | ✅ Complete | Multi-source data collection |
| Recommendations | ✅ Complete | Score-based engine |
| Celery Tasks | ✅ Complete | Scheduled automation |
| Docker | ✅ Complete | Full container setup |
| Documentation | ✅ Complete | Comprehensive guides |

---

## 🚀 Next Phase Roadmap

- [ ] Mobile app (React Native/Flutter)
- [ ] User authentication & profiles
- [ ] Email notifications
- [ ] Price history charts (interactive)
- [ ] Budget planning tools
- [ ] Nutritional information
- [ ] Recipe suggestions
- [ ] Community ratings & reviews
- [ ] Machine learning model improvements
- [ ] Real-time price alerts
- [ ] Multi-language support
- [ ] Social sharing features

---

## 📚 Resources

### Documentation
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Prophet Docs](https://facebook.github.io/prophet/)
- [Celery Docs](https://docs.celeryproject.io/)

### Tutorials
- Django REST Framework Tutorial
- Celery Getting Started
- Prophet Quick Start
- Docker Compose Guide

---

## 👨‍💻 Author

Created with ❤️ for helping users save money on groceries through AI-powered predictions.

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: Production Ready
