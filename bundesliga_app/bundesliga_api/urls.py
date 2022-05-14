from django.urls import path

from bundesliga_app.bundesliga_api.views import home_view, select_matchday_view, \
    last_matchday_view, next_matchday_view, search_by_team

urlpatterns = [
    path('', home_view, name='home'),
    path('matchday/<int:pk>', select_matchday_view, name='select_matchday'),
    path('last-matchday/', last_matchday_view, name='last_matchday'),
    path('next-matchday/', next_matchday_view, name='next_matchday'),
    path('search-by-team/', search_by_team, name='search_by_team'),
]

handler404 = 'bundesliga_app.bundesliga_api.views.handler404'
