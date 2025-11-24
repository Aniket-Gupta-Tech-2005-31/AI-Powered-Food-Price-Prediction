import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

default_app_config = 'recommendation.apps.RecommendationConfig'
