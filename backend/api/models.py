from django.db import models
from django.utils import timezone

# ========== CITY MODEL ==========
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state}"


# ========== VEGETABLE MODEL ==========
class Vegetable(models.Model):
    CATEGORY_CHOICES = [
        ('leafy', 'Leafy Vegetables'),
        ('root', 'Root Vegetables'),
        ('tomato', 'Tomatoes & Cucumbers'),
        ('legume', 'Pulses & Legumes'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ========== PRICE ENTRY MODEL ==========
class PriceEntry(models.Model):
    SOURCE_CHOICES = [
        ('bigbasket', 'BigBasket'),
        ('jiomart', 'JioMart'),
        ('blinkit', 'Blinkit'),
        ('local_market', 'Local Market'),
        ('government', 'Government'),
        ('other', 'Other'),
    ]

    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, related_name='price_entries')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='price_entries')
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    quality_rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['vegetable', 'city', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.vegetable.name} - {self.city.name} (₹{self.price_per_kg})"


# ========== PREDICTION MODEL ==========
class Prediction(models.Model):
    MODEL_CHOICES = [
        ('prophet', 'Prophet'),
        ('arima', 'ARIMA'),
        ('lstm', 'LSTM'),
        ('ensemble', 'Ensemble'),
    ]

    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, related_name='predictions')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='predictions')
    predicted_price = models.DecimalField(max_digits=8, decimal_places=2)
    prediction_date = models.DateField()
    model_used = models.CharField(max_length=20, choices=MODEL_CHOICES)
    confidence = models.FloatField(default=0.0)  # 0.0 to 1.0
    created_at = models.DateTimeField(auto_now_add=True)
    lower_bound = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    upper_bound = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['prediction_date']
        indexes = [
            models.Index(fields=['vegetable', 'city', 'prediction_date']),
        ]

    def __str__(self):
        return f"{self.vegetable.name} - {self.city.name} ({self.prediction_date})"


# ========== USER INTERACTION MODEL ==========
class UserFeedback(models.Model):
    FEEDBACK_TYPE = [
        ('recommendation_useful', 'Recommendation was useful'),
        ('recommendation_not_useful', 'Recommendation was not useful'),
        ('price_accurate', 'Price was accurate'),
        ('price_inaccurate', 'Price was inaccurate'),
    ]

    user_ip = models.GenericIPAddressField()
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.feedback_type} - {self.user_ip}"
