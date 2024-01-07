from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import *
from .forms import CustomAuthenticationForm, RegistrationForm
from .models import TaxiPost


@login_required
def driver_dashboard(request):
    user = request.user
    return render(request, 'taxi_app/driver/driver_dashboard.html', {'user': user})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or homepage
            return redirect('driver_dashboard')  # Update 'home' with the name of your homepage URL
    else:
        form = CustomAuthenticationForm(request)

    return render(request, 'taxi_app/driver/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            # Check if a user with the given phone number already exists
            if User.objects.filter(username=phone_number).exists():
                form.add_error('phone_number', 'This phone number is already registered.')
                return render(request, 'taxi_app/driver/register.html', {'form': form})

            user = form.save(commit=False)
            user.username = phone_number
            user.save()
            login(request, user)
            # Redirect to a success page or homepage
            return redirect('login')  # Update 'home' with the name of your homepage URL
    else:
        form = RegistrationForm()

    return render(request, 'taxi_app/driver/register.html', {'form': form})


def search_index(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']
            date = form.cleaned_data['date']

            # Perform a database query to find matching TaxiPosts
            matching_posts = TaxiPost.objects.filter(
                from_location=from_location,
                to_location=to_location,
                date__exact=date,
            ).order_by('date', 'time')

            return render(request, 'taxi_app/search_results.html', {'form': form, 'matching_posts': matching_posts})

    # If form is not valid or it's not a GET request, render the form
    return render(request, 'taxi_app/index.html', {'form': SearchForm()})


def search_results(request):
    if request.method == 'GET':
        from_location = request.GET.get('from_location', '')
        to_location = request.GET.get('to_location', '')

        # Query the database for posts that match the user's input
        matching_posts = TaxiPost.objects.filter(
            from_location__icontains=from_location,
            to_location__icontains=to_location,
        )

        context = {
            'matching_posts': matching_posts,
            'search_params': {
                'from_location': from_location,
                'to_location': to_location,
            },
        }

        return render(request, 'taxi_app/search_results.html', context)

    return HttpResponse("Invalid request method.")


@login_required
def post_trip(request):
    if request.method == 'POST':
        form = TaxiPostForm(request.POST)
        if form.is_valid():
            # Associate the post with the current user
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return render(request, 'taxi_app/post_trip.html', {'form': form, 'post_result': 'Post successful!'})
        else:
            # Form is not valid, print errors for debugging
            print(form.errors)
    else:
        form = TaxiPostForm()

    # Return the form with errors to the user
    return render(request, 'taxi_app/post_trip.html', {'form': form})


def user(request):
    return render(request, 'taxi_app/user/user.html')


def driver(request):
    return render(request, 'taxi_app/driver/main.html')
