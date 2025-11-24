# 📑 FoodPrice AI - Documentation Index

## 🎯 Quick Navigation

Use this page to find what you need quickly.

---

## 🚀 **I Want to GET STARTED** ⚡

### For First-Time Users
→ Read: **[QUICKSTART.md](./QUICKSTART.md)** (5 minutes)
- Fastest way to get running
- Step-by-step instructions
- Windows PowerShell commands
- Troubleshooting tips

### For Developers
→ Read: **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** (30 minutes)
- Architecture & design
- Technology stack
- API documentation
- ML pipeline explanation

### For Complete Understanding
→ Read: **[docs/README.md](./docs/README.md)** (45 minutes)
- Detailed setup guide
- Database schema
- API endpoints
- Deployment options

---

## 📚 **DOCUMENTATION FILES**

### Entry Points
| File | Time | Purpose |
|------|------|---------|
| [README.md](./README.md) | 5 min | **START HERE** - Overview & links |
| [QUICKSTART.md](./QUICKSTART.md) | 5 min | Quick setup guide |
| [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) | 30 min | Complete architecture |
| [COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md) | 10 min | What's included |
| [DELIVERY_CERTIFICATE.md](./DELIVERY_CERTIFICATE.md) | 15 min | Project checklist |
| [docs/README.md](./docs/README.md) | 45 min | Detailed guide |

---

## 🛠️ **I NEED TO SET UP THE PROJECT**

### Windows Users
1. Read: [QUICKSTART.md - Windows](./QUICKSTART.md)
2. Run: `.\setup.bat`
3. Or manually follow the steps

### Linux/Mac Users
1. Read: [QUICKSTART.md - Linux/Mac](./QUICKSTART.md)
2. Run: `bash setup.sh`
3. Or manually follow the steps

### Docker Users
1. Read: [PROJECT_OVERVIEW.md - Docker](./PROJECT_OVERVIEW.md#9-final-output-examples)
2. Run: `docker-compose up`

### Environment Setup
- Copy `.env.example` to `.env`
- Update variables if needed
- Default settings work for development

---

## 💻 **I WANT TO UNDERSTAND THE ARCHITECTURE**

### Project Structure
→ See: [PROJECT_OVERVIEW.md - Folder Structure](./PROJECT_OVERVIEW.md#5-folder-structure)

### Technology Stack
→ See: [PROJECT_OVERVIEW.md - Tech Stack](./PROJECT_OVERVIEW.md#technology-stack)

### Database Schema
→ See: [PROJECT_OVERVIEW.md - Database](./PROJECT_OVERVIEW.md#6-database-schema)

### API Endpoints
→ See: [PROJECT_OVERVIEW.md - API Endpoints](./PROJECT_OVERVIEW.md#7-backend-working-logic)

### ML Pipeline
→ See: [PROJECT_OVERVIEW.md - ML Pipeline](./PROJECT_OVERVIEW.md#8-ml-folder-working)

### Recommendation Engine
→ See: [PROJECT_OVERVIEW.md - Recommendations](./PROJECT_OVERVIEW.md#7-backend-working-logic)

---

## 🔌 **I WANT TO USE THE API**

### All Endpoints
→ See: [docs/README.md - API Endpoints](./docs/README.md#2-api-endpoints)

### Example Calls
```
GET /api/cities/
GET /api/vegetables/
GET /api/current-prices/?city=Delhi
GET /api/comparison/?city=Delhi&item=Tomato
GET /api/prediction/?city=Delhi&item=Tomato&days=7
GET /api/recommendation/?city=Delhi
GET /api/insights/?city=Delhi&month=January
```

### Testing APIs
→ See: [docs/README.md - Testing](./docs/README.md#10-testing)

---

## 🤖 **I WANT TO UNDERSTAND THE ML**

### How Predictions Work
→ See: [PROJECT_OVERVIEW.md - ML Pipeline](./PROJECT_OVERVIEW.md#8-ml-folder-working)

### Training Models
→ See: [docs/README.md - ML Usage](./docs/README.md#4-ml-model-usage)

### Data Preprocessing
→ See: [docs/README.md - ML Preprocessing](./docs/README.md#4-ml-model-usage)

### Making Predictions
→ See: [docs/README.md - Making Predictions](./docs/README.md#4-ml-model-usage)

---

## 💡 **I WANT TO UNDERSTAND RECOMMENDATIONS**

### Recommendation Logic
→ See: [PROJECT_OVERVIEW.md - Recommendations](./PROJECT_OVERVIEW.md#7-recommendation-engine-logic)

### How Score is Calculated
→ See: [PROJECT_OVERVIEW.md - Score Model](./PROJECT_OVERVIEW.md#7-recommendation-engine-logic)

### Using the Engine
→ See: [docs/README.md - Recommendation Engine](./docs/README.md#7-recommendation-engine)

---

## 📊 **I WANT TO UNDERSTAND DATA COLLECTION**

### Scraper Modules
→ See: [docs/README.md - Data Collection](./docs/README.md#7-scheduled-automation)

### Government APIs
→ See: [docs/README.md - Gov APIs](./docs/README.md#1-data-fetch-workflow)

### Online Store Scrapers
→ See: [docs/README.md - Online Stores](./docs/README.md#1-data-fetch-workflow)

---

## ⏰ **I WANT TO UNDERSTAND SCHEDULED TASKS**

### Celery Setup
→ See: [docs/README.md - Celery Setup](./docs/README.md#1-installation)

### Scheduled Tasks
→ See: [docs/README.md - Scheduled Automation](./docs/README.md#10-scheduled-automation)

### Beat Configuration
→ See: [PROJECT_OVERVIEW.md - Scheduled Tasks](./PROJECT_OVERVIEW.md#scheduled-tasks)

---

## 🐳 **I WANT TO USE DOCKER**

### Docker Compose
→ See: [docker-compose.yml](./docker-compose.yml)

### Dockerfile
→ See: [backend/Dockerfile](./backend/Dockerfile)

### Docker Guide
→ See: [docs/README.md - Docker](./docs/README.md#9-production-deployment)

---

## 🚀 **I WANT TO DEPLOY**

### Local Deployment
→ See: [QUICKSTART.md](./QUICKSTART.md)

### Docker Deployment
→ See: [PROJECT_OVERVIEW.md - Docker](./PROJECT_OVERVIEW.md#option-2-docker-compose)

### Cloud Deployment
→ See: [docs/README.md - Production Deployment](./docs/README.md#9-production-deployment)

### Environment Setup
→ See: [backend/.env.example](./backend/.env.example)

---

## 🧪 **I WANT TO TEST**

### Running Tests
→ See: [docs/README.md - Testing](./docs/README.md#10-testing)

### API Testing
→ See: [docs/README.md - Testing APIs](./docs/README.md#10-testing)

### Test Location
→ See: [backend/api/tests.py](./backend/api/tests.py)

---

## 🔐 **I WANT SECURITY INFORMATION**

### Security Features
→ See: [PROJECT_OVERVIEW.md - Security](./PROJECT_OVERVIEW.md#-security-features)

### CORS Configuration
→ See: [backend/core/settings.py](./backend/core/settings.py)

### Environment Variables
→ See: [backend/.env.example](./backend/.env.example)

---

## 📱 **I WANT TO CUSTOMIZE**

### Adding New Endpoints
→ See: [backend/api/views.py](./backend/api/views.py)

### Adding New Models
→ See: [backend/api/models.py](./backend/api/models.py)

### Customizing UI
→ See: [frontend/styles/main.css](./frontend/styles/main.css)

### Extending Frontend
→ See: [frontend/js/app.js](./frontend/js/app.js)

---

## 🐛 **I'M HAVING PROBLEMS**

### Troubleshooting Guide
→ See: [docs/README.md - Troubleshooting](./docs/README.md#8-troubleshooting)

### Common Issues
1. **Port already in use** → See QUICKSTART.md
2. **Redis connection error** → See docs/README.md
3. **Database errors** → See docs/README.md
4. **Model loading error** → See docs/README.md

---

## 📞 **QUICK REFERENCE**

### File Locations
- Frontend: `frontend/`
- Backend API: `backend/api/`
- ML Models: `ml/`
- Scrapers: `backend/scraper/`
- Recommendations: `backend/recommendation/`
- Configuration: `backend/core/`
- Database: `backend/db.sqlite3`

### Key Files
- Settings: `backend/core/settings.py`
- Models: `backend/api/models.py`
- Views: `backend/api/views.py`
- Frontend: `frontend/index.html`
- Styles: `frontend/styles/main.css`
- Logic: `frontend/js/app.js`

### URLs
- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

---

## 🎓 **LEARNING PATH**

### Beginner
1. Read: [README.md](./README.md)
2. Read: [QUICKSTART.md](./QUICKSTART.md)
3. Run: Setup script
4. Explore: Dashboard
5. Read: [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)

### Intermediate
1. Review: Architecture
2. Explore: API endpoints
3. Study: Database schema
4. Test: API calls
5. Customize: UI/Logic

### Advanced
1. Review: ML pipeline
2. Study: ML code
3. Train: Models
4. Deploy: Docker
5. Extend: Features

---

## 📊 **PROJECT STATISTICS**

- **Total Files**: 34+
- **Lines of Code**: 6,700+
- **Documentation**: 1,500+ lines
- **API Endpoints**: 8+
- **Database Models**: 5
- **Celery Tasks**: 3
- **Setup Time**: 5-10 minutes
- **Estimated Learning Time**: 2-4 hours

---

## ✨ **KEY HIGHLIGHTS**

✅ Complete full-stack application
✅ Production-ready code
✅ Comprehensive documentation
✅ Multiple setup options
✅ Docker containerization
✅ ML integration
✅ Automated tasks
✅ Beautiful UI
✅ Scalable architecture
✅ Enterprise-grade

---

## 🎉 **GET STARTED NOW**

### In 5 Minutes
1. [Read QUICKSTART.md](./QUICKSTART.md)
2. Run setup script
3. Open http://localhost:8080

### In 30 Minutes
1. [Read PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
2. Understand architecture
3. Explore codebase

### In 1 Hour
1. Complete setup
2. Test API endpoints
3. Customize UI

### In 2 Hours
1. Complete setup
2. Explore all features
3. Study architecture
4. Plan customizations

---

## 📞 **NEED HELP?**

### For Setup Issues
→ Check [QUICKSTART.md](./QUICKSTART.md)

### For Architecture Questions
→ Check [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)

### For Detailed Information
→ Check [docs/README.md](./docs/README.md)

### For Feature Overview
→ Check [COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md)

### For Complete Checklist
→ Check [DELIVERY_CERTIFICATE.md](./DELIVERY_CERTIFICATE.md)

---

## 🚀 **LET'S BEGIN!**

Choose your starting point:

- **I'm in a hurry** → [QUICKSTART.md](./QUICKSTART.md) ⚡
- **I want to learn** → [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) 📚
- **I need details** → [docs/README.md](./docs/README.md) 🔍
- **I want everything** → Start with [README.md](./README.md) 🎯

---

**Happy Coding!** 🥬🤖

*FoodPrice AI - Making smart shopping decisions through AI predictions*
