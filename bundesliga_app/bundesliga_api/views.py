from django.shortcuts import render

from bundesliga_app.bundesliga_api.helpers.OpenLigaAPI import API


def home_view(request):
    api = API()

    api_response = api.get_table()
    for position, team in enumerate(api_response, 1):
        team['position'] = position
    context = {
        'table': api_response
    }
    return render(request, template_name='home.html', context=context)


def all_matchdays_view(request):
    api = API()
    context = {
        'matchday_names': {}
    }
    api_response = api.get_all_matches()

    for match in api_response:
        matchday_name = match['group']['groupName']
        matchday_number = matchday_name.split('.')[0]
        context['matchday_names'][matchday_name] = {'matchday_name': matchday_name, 'number': matchday_number}

    return render(request, template_name='all_matches.html', context=context)


def select_matchday_view(request, pk):
    api = API()

    api_response = api.get_matchday(pk)

    for match in api_response:
        if match['matchIsFinished']:
            result = f"{match['matchResults'][0]['pointsTeam1']} : {match['matchResults'][0]['pointsTeam2']}"
            match['result'] = result

    context = {
        'matches': api_response,
    }

    return render(request, template_name='matchday.html', context=context)


def last_matchday_view(request):
    api = API()

    api_response = api.get_all_matches()
    last_matchday_number = 0

    for match in api_response:

        if match['matchIsFinished']:
            last_matchday_number = match['group']['groupOrderID']

    last_matchday = api.get_matchday(last_matchday_number)

    for match in last_matchday:
        result = f"{match['matchResults'][0]['pointsTeam1']} : {match['matchResults'][0]['pointsTeam2']}"
        match['result'] = result
        match['matchDateTime'] = match['matchDateTime'].replace('T', ' ')
    context = {
        'matches': last_matchday,
    }
    return render(request, template_name='matchday.html', context=context)


def next_matchday_view(request):
    api = API()

    api_response = api.get_all_matches()
    next_matchday_number = 0

    for match in api_response:

        if not match['matchIsFinished']:
            next_matchday_number = match['group']['groupOrderID']
            clean_date = match['matchDateTime'].replace('T', ' ')
            match['matchDateTime'] = clean_date

    next_matchday = api.get_matchday(next_matchday_number)

    for match in next_matchday:
        clean_date = match['matchDateTime'].replace('T', ' ')
        match['matchDateTime'] = clean_date

    context = {
        'matches': next_matchday,
    }

    return render(request, template_name='matchday.html', context=context)
