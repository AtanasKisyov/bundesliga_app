from django.urls import path

from bundesliga_app.bundesliga_api.views import home_view, all_matchdays_view, select_matchday_view, \
    last_matchday_view, next_matchday_view

urlpatterns = [
    path('', home_view, name='home'),
    path('matchdays/', all_matchdays_view, name='all_matchdays'),
    path('matchday/<int:pk>', select_matchday_view, name='select_matchday'),
    path('last-matchday/', last_matchday_view, name='last_matchday'),
    path('next-matchday/', next_matchday_view, name='next_matchday'),
]
