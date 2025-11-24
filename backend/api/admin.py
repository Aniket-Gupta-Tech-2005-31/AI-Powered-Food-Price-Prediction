from django.contrib import admin
from .models import City, Vegetable, PriceEntry, Prediction, UserFeedback


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'created_at']
    search_fields = ['name', 'state']
    list_filter = ['state', 'created_at']


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    search_fields = ['name']
    list_filter = ['category', 'created_at']


@admin.register(PriceEntry)
class PriceEntryAdmin(admin.ModelAdmin):
    list_display = ['vegetable', 'city', 'price_per_kg', 'source', 'timestamp']
    search_fields = ['vegetable__name', 'city__name', 'source']
    list_filter = ['source', 'city', 'timestamp', 'quality_rating']
    date_hierarchy = 'timestamp'


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['vegetable', 'city', 'predicted_price', 'prediction_date', 'model_used', 'confidence']
    search_fields = ['vegetable__name', 'city__name']
    list_filter = ['model_used', 'prediction_date', 'created_at']
    date_hierarchy = 'prediction_date'


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_type', 'user_ip', 'vegetable', 'city', 'created_at']
    search_fields = ['user_ip', 'feedback_type']
    list_filter = ['feedback_type', 'created_at']
    date_hierarchy = 'created_at'
