from django.shortcuts import render

from bundesliga_app.bundesliga_api.forms import SearchForm
from bundesliga_app.bundesliga_api.helpers.OpenLigaAPI import API


api = API()


def home_view(request):

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
        'matchday_names': {}
    }

    api_response = api.get_all_matches()

    for match in api_response:
        matchday_name = match['group']['groupName']
        matchday_number = matchday_name.split('.')[0]
        context['matchday_names'][matchday_name] = {'matchday_name': matchday_name, 'number': matchday_number}

    return render(request, template_name='home.html', context=context)


def select_matchday_view(request, pk):

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

    if not next_matchday:

        table = api.get_table()
        champion = table[0]
        champions_league_participants = table[:4]
        europa_league_participant = table[4]
        europa_conference_participant = table[5]
        relegation_play_off = table[15]
        relegated_teams = table[16:]

        context = {
            'end_of_season': 'Season 2021/2022 has ended!',
            'champion': champion,
            'champions_league_participants': champions_league_participants,
            'europa_league_participant': europa_league_participant,
            'europa_conference_league': europa_conference_participant,
            'relegation_play_off': relegation_play_off,
            'relegated_teams': relegated_teams,
        }

    return render(request, template_name='matchday.html', context=context)


def search_by_team(request):

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
        end_of_season = True

        for match in match_data:
            if match['matchIsFinished']:
                result = f"{match['matchResults'][0]['pointsTeam1']} : {match['matchResults'][0]['pointsTeam2']}"
                match['result'] = result
            else:
                clean_date = match['matchDateTime'].replace('T', ' ')
                match['matchDateTime'] = clean_date
                end_of_season = False

        team_name = team_information['teamName']

        if not end_of_season:
            next_match = match_data.pop()
        else:
            next_match = None
        table = api.get_table()
        team_position = {}

        for position, team in enumerate(table, 1):

            if team['teamName'] != team_name:
                continue

            ratio = team['won'] / team['matches'] * 100
            team['ratio'] = f'{ratio:.2f}'
            team['position'] = position
            team_position = team

        context = {
            'team': team_information,
            'last_five_matches': match_data,
            'next_match': next_match,
            'team_position': team_position,
        }

        return render(request, template_name='search_by_team.html', context=context)


def handler404(request, *args, **kwargs):
    response = render(request, context={}, template_name='404.html')
    response.status_code = 404
    return response
