from django.shortcuts import render

from bundesliga_app.bundesliga_api.forms import SearchForm
from bundesliga_app.bundesliga_api.helpers.OpenLigaAPI import API


def home_view(request):
    api = API()

    api_response = api.get_table()

    for position, team in enumerate(api_response, 1):
        team['position'] = position
        played = team['matches']
        win = team['won']
        ratio = win / played * 100
        team['ratio'] = f'{ratio:.2f} %'

    search_form = SearchForm()
    context = {
        'table': api_response,
        'form': search_form,
    }

    return render(request, template_name='home.html', context=context)


def all_matchdays_view(request):
    api = API()

    context = {
        'matchday_names': {},
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

    next_matchday = api.get_matchday(next_matchday_number)

    for match in next_matchday:
        clean_date = match['matchDateTime'].replace('T', ' ')
        match['matchDateTime'] = clean_date

    context = {
        'matches': next_matchday,
    }

    return render(request, template_name='matchday.html', context=context)


def search_by_team(request):
    api = API()

    if request.method == 'POST':
        team_names = api.get_team_names()
        team = request.POST['team']

        result = [x for x in team_names if team.lower() in x['teamName'].lower()]

        if len(result) > 1 or len(result) == 0:
            context = {
                'error': f'There are {len(result)} results! Please, try again!'
            }
            return render(request, template_name='search_by_team.html', context=context)

        team_information = result[0]
        team_id = team_information['teamId']
        match_data = api.get_team_last_five_matches_and_next_match(team_id)

        for match in match_data:
            if match['matchIsFinished']:
                result = f"{match['matchResults'][0]['pointsTeam1']} : {match['matchResults'][0]['pointsTeam2']}"
                match['result'] = result
            else:
                clean_date = match['matchDateTime'].replace('T', ' ')
                match['matchDateTime'] = clean_date

        next_match = match_data.pop()
        context = {
            'team': team_information,
            'last_five_matches': match_data,
            'next_match': next_match,
        }
        # Add current position in the table
        return render(request, template_name='search_by_team.html', context=context)

