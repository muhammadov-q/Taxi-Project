from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import TaxiPost


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'type': 'tel'}))


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'type': 'tel'}))
    car_type = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'car_type', 'password1', 'password2']


CITIES_CHOICES = [
    ("Tashkent", "Tashkent"),
    ("Andijan", "Andijan"),
    ("Bukhara", "Bukhara"),
    ("Jizzakh", "Jizzakh"),
    ("Kashkadarya", "Kashkadarya"),
    ("Navoi", "Navoi"),
    ("Namangan", "Namangan"),
    ("Samarkand", "Samarkand"),
    ("Sirdarya", "Sirdarya"),
    ("Surkhandarya", "Surkhandarya"),
    ("Fergana", "Fergana"),
    ("Khorezm", "Khorezm"),
]


class TaxiPostForm(forms.ModelForm):
    class Meta:
        model = TaxiPost
        fields = ['from_location', 'to_location', 'date', 'time', 'price', 'available_seats', 'comments']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    from_location = forms.ChoiceField(choices=CITIES_CHOICES, label="From:")
    to_location = forms.ChoiceField(choices=CITIES_CHOICES, label="To:")
    price = forms.DecimalField(label="Price:")
    available_seats = forms.IntegerField(label="Available Seats:")
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your comment here'}),
                               label="Comment", required=False)


class SearchForm(forms.Form):
    from_location = forms.TypedChoiceField(choices=CITIES_CHOICES, label="From:")
    to_location = forms.TypedChoiceField(choices=CITIES_CHOICES, label="To:")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date:")
