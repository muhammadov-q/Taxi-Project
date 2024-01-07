from django.urls import path

from .views import *

urlpatterns = [
    path('', search_index, name='search_index'),
    path('user/', user, name='user'),
    path('driver/', driver, name='driver'),
    path('post_trip/', post_trip, name='post_trip'),
    path('search_results/', search_results, name='search_results'),
    path('search/', search_index, name='search_index'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('driver/dashboard/', driver_dashboard, name='driver_dashboard'),
]
