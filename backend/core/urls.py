from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

# ========== API ROUTER ==========
router = routers.DefaultRouter()
router.register(r'vegetables', views.VegetableViewSet, basename='vegetable')
router.register(r'cities', views.CityViewSet, basename='city')
router.register(r'price-entries', views.PriceEntryViewSet, basename='price-entry')
router.register(r'predictions', views.PredictionViewSet, basename='prediction')

# ========== URL PATTERNS ==========
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Custom endpoints
    path('api/current-prices/', views.CurrentPricesView.as_view(), name='current-prices'),
    path('api/comparison/', views.ComparisonView.as_view(), name='comparison'),
    path('api/prediction/', views.PredictionDetailView.as_view(), name='prediction-detail'),
    path('api/recommendation/', views.RecommendationView.as_view(), name='recommendation'),
    path('api/insights/', views.InsightsView.as_view(), name='insights'),
    path('api/fetch-now/', views.FetchNowView.as_view(), name='fetch-now'),
    path('api/submit-price/', views.SubmitPriceView.as_view(), name='submit-price'),
]
