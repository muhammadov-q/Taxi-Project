# Generated by Django 4.2.8 on 2024-01-07 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taxi_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxiPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField(default='00:00')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_seats', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True, max_length=500)),
                ('user', models.ForeignKey(default=taxi_app.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
