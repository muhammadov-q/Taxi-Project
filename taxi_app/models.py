from django.db import models
from django.contrib.auth import get_user_model


def get_default_user():
    return get_user_model().objects.get_or_create(username='default_user')[0]


class TaxiPost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=get_default_user)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(default='00:00')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    comments = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.from_location} to {self.to_location} - {self.date}"
