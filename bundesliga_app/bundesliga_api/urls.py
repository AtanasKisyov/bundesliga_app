from django.urls import path

from bundesliga_app.bundesliga_api.views import all_matches_view

urlpatterns = [
    path('', all_matches_view, name='home')
]