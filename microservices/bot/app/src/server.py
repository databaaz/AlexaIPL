from src import app
from flask import Flask, request, redirect, make_response, render_template
from flask_ask import Ask, statement, question, session
import requests
import json



ask = Ask(app, "/ipl")





url = "https://data.likelihood60.hasura-app.io/v1/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 238662f0f1e1e5d9f3117b7ee899ce8c1b0157c1f0ee1d70"
}
query_match_result = '''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "winner"
        ],
        "where": {{
            "team1": {{
                "$eq": "{}"
            }},
            "team2": {{
                "$eq": "{}"
            }},
            "date":{{
                "$eq": "{}"
            }}
        }}
    }}
}}'''

query_mom = '''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "team1",
            "team2",
            "player_of_match"
        ],
        "where": {{
            "date": {{
                "$eq": "{}"
            }}
        }}
    }}
}}'''
query_summary='''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "team1",
            "team2",
            "venue",
            "city",
            "toss_winner",
            "toss_decision",
            "winner",
            "win_by_runs",
            "win_by_wickets",
            "player_of_match"
        ],
        "where": {{
            "date": {{
                "$eq": "{}"
            }}
        }}
    }}
}}
'''


teams_mapping = {'rcb':'Royal Challengers Bangalore', 'bangalore':'Royal Challengers Bangalore', 'royal challengers bangalore': 'Royal Challengers Bangalore',
'mi':'Mumbai Indians', 'mumbai':'Mumbai Indians', 'mumbai indians': 'Mumbai Indians',
'hyderabad':'Sunrisers Hyderabad', 'srh':'Sunrisers Hyderabad','sunrisers hyderabad':'Sunrisers Hyderabad', 'sunrisers':'Sunrisers Hyderabad',
'csk':'Chennai Super Kings','chennai':'Chennai Super Kings', 'chennai super kings':'Chennai Super Kings',
'kxip':'Kings XI Punjab', 'punjab':'Kings XI Punjab','kings eleven punjab':'Kings XI Punjab',
'rps':'Rising Pune Supergiant', 'pune':'Rising Pune Supergiant','rising pune supergiant':'Rising Pune Supergiant',
'gujrat':'Gujarat Lions','gujarat':'Gujarat Lions','gl':'Gujarat Lions', 'gujarat lions':'Gujarat Lions',
'kkr':'Kolkata Knight Riders', 'kolkata':'Kolkata Knight Riders', 'knight riders':'Kolkata Knight Riders','kolkata knight riders':'Kolkata Knight Riders',
'rajasthan':'Rajasthan Royals', 'rr':'Rajasthan Royals','rajasthan royals':'Rajasthan Royals',
'delhi':'Delhi Daredevils', 'daredevils':'Delhi Daredevils', 'dd':'Delhi Daredevils','delhi daredevils':'Delhi Daredevils'
}

@app.route('/')
def homepage():
    return "Alexa skill is running."

@ask.launch
def welcome():
	welcome_msg = render_template('welcome')
	return question(welcome_msg)

@ask.intent("MatchResult")
def match_result(teamA,teamB,date_of_match):
	try:
		teamA=teamA.lower()
		teamB=teamB.lower()
		teamA = teams_mapping[teamA]
		teamB = teams_mapping[teamB]
	except:
		teamA=None
		teamB=None	
	requestPayload = query_match_result.format(teamA,teamB,date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result) == 0:
		teamA,teamB = teamB,teamA
		requestPayload = query_match_result.format(teamA,teamB,date_of_match)
		resp = requests.request("POST", url, data=(requestPayload), headers=headers)
		result = json.loads(resp.content)
		if len(result) == 0:
			return statement('Sorry I could not find any result for your query. Please try again')
	else:
		winner = result[0]['winner']
		return statement('You have queried about the match between {} and team {} that took place on {}. The winner of the match was {}'.format(teamA,teamB,date_of_match, winner))
	
    
@ask.intent("MOMatch")
def mom(date_of_match):
	requestPayload = query_mom.format(date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result)>0:
		response = 'A total of {} matches took place on {}.\n'.format(len(result),date_of_match)
		for i in range(len(result)):
			response += 'Match {}: {} versus {}. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["player_of_match"])
	else:
		response = 'Sorry, Your query did not return any result. Please try again.'
	return statement(response)	

@ask.intent("MatchSummary")	
def summarize_match(date_of_match):
	requestPayload = query_summary.format(date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result)>0:
		response = 'A total of {} matches took place on {}.\n'.format(len(result),date_of_match)
		for i in range(len(result)):
			if result[i]["win_by_runs"]>0:
				response += 'Match {}: {} versus {}. The match was played at {},{}. {} won the toss and elected to {} first. {} won the match by {} runs. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["venue"],result[i]["city"],result[i]["toss_winner"],result[i]["toss_decision"],result[i]["winner"],result[i]["win_by_runs"],result[i]["player_of_match"])
			else:
				response += 'Match {}: {} versus {}. The match was played at {},{}. {} won the toss and elected to {} first. {} won the match by {} wickets. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["venue"],result[i]["city"],result[i]["toss_winner"],result[i]["toss_decision"],result[i]["winner"],result[i]["win_by_wickets"],result[i]["player_of_match"])
					
	else:
		response = 'Sorry, Your query did not return any result. Please try again.'
	return statement(response)
	



