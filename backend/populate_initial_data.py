"""
Django management command to populate initial data
Run with: python manage.py shell < populate_initial_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import City, Vegetable

# ========== CITIES DATA ==========
cities_data = [
    {'name': 'Delhi', 'state': 'Delhi'},
    {'name': 'Mumbai', 'state': 'Maharashtra'},
    {'name': 'Bangalore', 'state': 'Karnataka'},
    {'name': 'Hyderabad', 'state': 'Telangana'},
    {'name': 'Pune', 'state': 'Maharashtra'},
    {'name': 'Chennai', 'state': 'Tamil Nadu'},
    {'name': 'Kolkata', 'state': 'West Bengal'},
    {'name': 'Ahmedabad', 'state': 'Gujarat'},
    {'name': 'Jaipur', 'state': 'Rajasthan'},
    {'name': 'Lucknow', 'state': 'Uttar Pradesh'},
]

# ========== VEGETABLES DATA ==========
vegetables_data = [
    {'name': 'Tomato', 'category': 'tomato'},
    {'name': 'Onion', 'category': 'root'},
    {'name': 'Potato', 'category': 'root'},
    {'name': 'Spinach', 'category': 'leafy'},
    {'name': 'Carrot', 'category': 'root'},
    {'name': 'Cucumber', 'category': 'tomato'},
    {'name': 'Capsicum', 'category': 'tomato'},
    {'name': 'Broccoli', 'category': 'leafy'},
    {'name': 'Cauliflower', 'category': 'leafy'},
    {'name': 'Cabbage', 'category': 'leafy'},
    {'name': 'Bell Pepper', 'category': 'tomato'},
    {'name': 'Green Beans', 'category': 'legume'},
    {'name': 'Peas', 'category': 'legume'},
    {'name': 'Radish', 'category': 'root'},
    {'name': 'Beetroot', 'category': 'root'},
]

# ========== POPULATE DATA ==========
def populate_cities():
    print("Populating cities...")
    for city_data in cities_data:
        city, created = City.objects.get_or_create(**city_data)
        status = "Created" if created else "Already exists"
        print(f"  {status}: {city.name}")

def populate_vegetables():
    print("\nPopulating vegetables...")
    for veg_data in vegetables_data:
        vegetable, created = Vegetable.objects.get_or_create(**veg_data)
        status = "Created" if created else "Already exists"
        print(f"  {status}: {vegetable.name}")

if __name__ == '__main__':
    populate_cities()
    populate_vegetables()
    print("\nData population completed!")
