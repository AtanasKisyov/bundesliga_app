from django.shortcuts import render

from bundesliga_app.bundesliga_api.helpers.OpenLigaAPI import API


def all_matches_view(request):
    api = API()

    api_response = api.get_table()
    for position, team in enumerate(api_response, 1):
        team['position'] = position
    context = {
        'table': api_response
    }
    return render(request, template_name='home.html', context=context)


def all_matchdays_view(request):
    pass


def select_matchday_view(request):
    pass


def last_matchday_view(request):
    pass


def nex_matchday_view(request):
    pass
