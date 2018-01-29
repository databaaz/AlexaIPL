from flask import Flask, request, redirect, make_response, render_template
from flask_ask import Ask, statement, question, session
import requests
import json


app = Flask(__name__)
ask = Ask(app, "/")


'''@ask.launch
def welcome():
	welcome_msg = render_template('welcome')
    return question(welcome_msg)

'''
url = "https://data.adulteration65.hasura-app.io/v1/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer a3780941cd52641e5f0b0ba821929addc347e82cd9bd17b4"
}
query = '''{
    "type": "select",
    "args": {
        "table": "matches",
        "columns": [
            "winner"
        ],
        "where": {
            "team1": {
                "$eq": {}
            },
            "team2": {
                "$eq": {}
            },
            "date":{
                "$eq": {}
            }
            

        }
    }
}'''






teams_mapping = {'RCB':'Royal Challengers Bangalore', 'Bangalore':'Royal Challengers Bangalore', 'Royal Challengers Bangalore': 'Royal Challengers Bangalore',
'MI':'Mumbai Indians', 'Mumbai':'Mumbai Indians', 'Mumbai Indians': 'Mumbai Indians', 'Hyderabad':'Sunrisers Hyderabad', 'SRH':'Sunrisers Hyderabad',
'Sunrisers Hyderabad':'Sunrisers Hyderabad', 'CSK':'Chennai Super Kings','Chennai':'Chennai Super Kings', 'Chennai Super Kings':'Chennai Super Kings',
'KXIP':'Kings XI Punjab', 'Punjab':'Kings XI Punjab','Kings Eleven Punjab':'Kings XI Punjab', 'RPS':'Rising Pune Supergiant', 'Pune':'Rising Pune Supergiant',

}
@ask.intent("MatchResult")
def match_result(teamA,teamB,date_of_match):
	welcome_msg = render_template('welcome')
	requestPayload = json.loads(query.format(teamA,teamB,date))
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	#print(resp.content)
	#return statement('You have queried about the match {} versus {} that took place on {}'.format(teamA,teamB,date_of_match))
    
@ask.intent("MOMatch")
def mom(date_of_match):
	return statement("Man of the match for every match is MS Dhoni. He is the legend.")
	



'''
@app.route('/')
def hello():
	return "Hello World - Shahbaz"

@app.route('/authors')
def authors():
	author_list = requests.get('https://jsonplaceholder.typicode.com/users').json()
	author_data = dict()
	for i in author_list:
		author_data[i['id']]=i['name']
	posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
	post_count=dict()
	for i in posts:
		u_id = i['userId']
		post_count[u_id] = post_count.get(u_id,0) + 1
	resp = ''
	for u_id in author_data:
		resp += (' '.join([str(author_data[u_id]),str(post_count[u_id])])+'<br>')
	return resp

@app.route('/setcookie')
def setCookie():
	#redirect_to_index = redirect('/')
	resp = app.make_response('Cookies Set !')
	resp.set_cookie('name', value='Shahbaz')
	resp.set_cookie('age', value='21')
	return resp
@app.route('/getcookie')
def getCookie():
	name = request.cookies.get('name')
	age = request.cookies.get('age')
	return 'name: '+ name + '<br>' + 'age: '+age

@app.route('/robots.txt')
def deny_robot():
	return r"""<pre>
          .-''''''-.
        .' _      _ '.
       /   O      O   \
      :                :
      |                |
      :       __       :
       \  .-"`  `"-.  /
        '.          .'
          '-......-'
     YOU SHOULDN'T BE HERE</pre>"""

@app.route('/image')    
def send_image():
	return app.send_static_file('sad_bot.jpg')
@app.route('/html')
def send_html():
	return render_template('home.html')

@app.route('/input')	
def send():
	return render_template('form.html')

@app.route('/send-name',  methods = ['POST'])	
def get_name():
	name = request.form['user_name']
	print(name)
	return 'Welcome '+name



    
    '''