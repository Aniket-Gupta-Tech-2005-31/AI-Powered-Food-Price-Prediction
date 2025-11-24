# Generated migration for initial models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('state', models.CharField(max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('leafy', 'Leafy Vegetables'), ('root', 'Root Vegetables'), ('tomato', 'Tomatoes & Cucumbers'), ('legume', 'Pulses & Legumes'), ('other', 'Other')], max_length=20)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PriceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_kg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.CharField(choices=[('bigbasket', 'BigBasket'), ('jiomart', 'JioMart'), ('blinkit', 'Blinkit'), ('agmarknet', 'Agmarknet'), ('local', 'Local Market')], max_length=50)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('quality_rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Excellent')], default=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.city')),
                ('vegetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vegetable')),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['vegetable', 'city', 'timestamp'], name='api_price_vegetable_city_timestamp_idx')],
            },
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicted_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prediction_date', models.DateField()),
                ('model_used', models.CharField(choices=[('prophet', 'Prophet'), ('arima', 'ARIMA'), ('ensemble', 'Ensemble')], max_length=50)),
                ('confidence', models.FloatField(default=0.0)),
                ('lower_bound', models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)),
                ('upper_bound', models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.city')),
                ('vegetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vegetable')),
            ],
            options={
                'ordering': ['-prediction_date'],
                'indexes': [models.Index(fields=['vegetable', 'city', 'prediction_date'], name='api_prediction_vegetable_city_date_idx')],
            },
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.GenericIPAddressField()),
                ('feedback_type', models.CharField(choices=[('bug', 'Bug Report'), ('suggestion', 'Suggestion'), ('other', 'Other')], max_length=50)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.city')),
                ('vegetable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vegetable')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
