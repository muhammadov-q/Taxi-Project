from django.http import HttpResponse
from django.shortcuts import render

from .forms import *
from .models import TaxiPost


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


def post_trip(request):
    if request.method == 'POST':
        form = TaxiPostForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            post = form.save(commit=False)
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
    return render(request, 'taxi_app/user.html')


def driver(request):
    return render(request, 'taxi_app/driver.html')
