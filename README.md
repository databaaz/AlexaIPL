# Alexa IPL

## Introduction

This is an alexa skill which gives you answers about all the previous IPL matches till Season10 (2017), based on your queries.

## How does it work?

### Workflow
You can test out this skill using an Amazon Echo device or at [Echosim](https://echosim.io) (Web Browser) or at [Reverb](https://reverb.ai/) (Android/iOS). The workflow is as follows:
- You invoke the skill saying "Alexa, start IPL Search."
- Alexa will speak a welcome message and wait for your query.
- Currently we have 3 types of queries that can be invoked  
    **1. Match Summary:**  
    		*sample invocation* - `Summarize the match on April 9, 2017`  
    **2. Man of the Match:**  
    		*sample invocation* - `Who was awarded the man of the match on April 9, 2017`  
    **3. Match Result:**  
    		*sample invocation* - `Who won the match between Kolkata and Mumbai that took place on April 9, 2017`  
    **4. Season Winners:**  
    		*sample invocation* - `Who was the winner of IPL Season 2014`  
-If you want to exit the skill, you can do so by saying `exit` or `goodbye` or `close IPL search`  
**_Note:_** We will iteratively add more intents to the skills, which will be introduced in later releases.  

### Internal Implementation

This skill is written in Python using Flask and the python library [Flask-Ask](https://github.com/johnwheeler/flask-ask). The Implementation is as follows:
- When you make a particular type of query, an appropriate intent from the skill set is invoked and then the relevant method mapped to that intent is called from the Flask script, which fetches the results from the matches database.
A response string is generated using fetched data, which is spoken out by Alexa.  
- If Alexa is not able to recognise the spoken words or if there exists no results based on the parameters passed, Alexa will humbly respond and ask you to try again.


## How to get it up and running?
### Deployment
This skill can be deployed on any server that supports HTTPS over SSL. 
For our testing purpose we are using services of Hasura. Hasura automatically generates SSL certificates for you.
Just run the following commands to deploy your skill.

(Make sure you have [hasura-cli](https://docs.hasura.io/0.15/manual/install-hasura-cli.html))

```
$ hasura quickstart khan185/alexa-ipl-skill
$ cd alexa-ipl-skill
$ git add . && git commit -m "Initial Commit"
$ git push hasura master
```

### Database Setup  

The `matches` table is already created for you. We need to import data into this table using a csv file.
The matches csv data has been fetched from [Kaggle](https://www.kaggle.com/manasgarg/ipl/data)  
1. Download the matches.csv file.  
2. Import the csv data in your table. For help, [check this](https://stackoverflow.com/questions/47380173/how-do-i-import-a-csv-file-into-my-hasura-postgresql-database)  
3. There is another table with the name `ipl_finals` having two columns 'season' and 'match_id', where 'match_id' is a foreign key linked to 'id' column in `matches` table. Refer that table and insert data for all the 10 seasons accordingly.  


### How to add the skill to your Amazon account?

To link it with your Amazon Echo Device, go to your [Amazon developer console](https://developer.amazon.com/edw/home.html#/skills).

1. Create a new skill. Call it `IPL Ask` (or any name you'd like to give). Give the invocation name as `ipl ask`. Click next.  

2. Go to Skill Builder > Code Editor, and copy the following JSON object
```
{
  "languageModel": {
    "types": [
      {
        "name": "IPL_TEAM",
        "values": [
          {
            "id": null,
            "name": {
              "value": "Gujarat Lions",
              "synonyms": [
                "Gujrat",
                "Gujarat",
                "GL"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Kolkata Knight Riders",
              "synonyms": [
                "Kolkata",
                "KKR",
                "Knight Riders"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Mumbai Indians",
              "synonyms": [
                "MI",
                "Mumbai"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Royal Challengers Bangalore",
              "synonyms": [
                "Bangalore",
                "Bengaluru",
                "RCB"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Kings Eleven Punjab",
              "synonyms": [
                "Punjab",
                "KXIP"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Delhi Daredevils",
              "synonyms": [
                "Delhi",
                "Daredevils",
                "DD"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Sunrisers Hyderabad",
              "synonyms": [
                "sunrisers",
                "Hyderabad",
                "SRH"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Chennai Super Kings",
              "synonyms": [
                "Chennai",
                "CSK"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Rajasthan Royals",
              "synonyms": [
                "RR",
                "Rajasthan"
              ]
            }
          },
          {
            "id": null,
            "name": {
              "value": "Rising Pune Supergiants",
              "synonyms": [
                "RPS",
                "Pune"
              ]
            }
          }
        ]
      }
    ],
    "intents": [
      {
        "name": "AMAZON.CancelIntent",
        "samples": []
      },
      {
        "name": "AMAZON.HelpIntent",
        "samples": []
      },
      {
        "name": "AMAZON.StopIntent",
        "samples": []
      },
      {
        "name": "Exit",
        "samples": [
          "Bye",
          "Quit",
          "Exit",
          "Close IPL Search",
          "Close",
          "Shutdown",
          "Goodbye"
        ],
        "slots": []
      },
      {
        "name": "IPLFinal",
        "samples": [
          "Who won the final match of season {season}",
          "who won the IPL in the year {season}",
          "tell me about the final match of season {season}",
          "who won IPL season {season}",
          "who was the winner of IPL season {season}",
          "who won the final match of IPL {season}",
          "who won the IPL trophy in season {season}"
        ],
        "slots": [
          {
            "name": "season",
            "type": "AMAZON.NUMBER",
            "samples": [
              "{season}"
            ]
          }
        ]
      },
      {
        "name": "MatchResult",
        "samples": [
          "Did {teamA} win the match against {teamB} on {date_of_match}",
          "Tell me the result of the match between {teamA} and {teamB} on {date_of_match}",
          "Tell me about the winner of the match between {teamA} and {teamB} the date of the match is {date_of_match}",
          "give me the match result between {teamA} and {teamB} that took place on {date_of_match}",
          "Who won the match between {teamA} and {teamB} on {date_of_match}",
          "Who was the winner in the match of {teamA} versus {teamB} that took place on {date_of_match}"
        ],
        "slots": [
          {
            "name": "teamA",
            "type": "IPL_TEAM"
          },
          {
            "name": "teamB",
            "type": "IPL_TEAM"
          },
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      },
      {
        "name": "MatchSummary",
        "samples": [
          "Please give summary of the match that took place on {date_of_match}",
          "Give highlights of the match that took place on {date_of_match}",
          "Summarize the match played on {date_of_match}",
          "Give details of that match that was played on {date_of_match}",
          "Tell me more about the match played on {date_of_match}"
        ],
        "slots": [
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      },
      {
        "name": "MOMatch",
        "samples": [
          "Who was the player of the match on {date_of_match}",
          "Who was awarded the man of the match that took place on {date_of_match}",
          "Who was the best player of the match that took place on {date_of_match}",
          "Who was the man of the match for the match that took place on {date_of_match}",
          "Which player showed best performance in the match that took place on {date_of_match}"
        ],
        "slots": [
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      }
    ],
    "invocationName": "ipl search"
  },
  "prompts": [
    {
      "id": "Confirm.Intent-Exit",
      "variations": [
        {
          "type": "PlainText",
          "value": "Are you sure you want to exit IPL search ?"
        }
      ]
    },
    {
      "id": "Elicit.Intent-IPLFinal.IntentSlot-season",
      "variations": [
        {
          "type": "PlainText",
          "value": "Please mention the season of IPL you're querying about"
        }
      ]
    }
  ],
  "dialog": {
    "intents": [
      {
        "name": "Exit",
        "confirmationRequired": true,
        "prompts": {
          "confirmation": "Confirm.Intent-Exit"
        },
        "slots": []
      },
      {
        "name": "IPLFinal",
        "confirmationRequired": false,
        "prompts": {},
        "slots": [
          {
            "name": "season",
            "type": "AMAZON.NUMBER",
            "elicitationRequired": true,
            "confirmationRequired": false,
            "prompts": {
              "elicitation": "Elicit.Intent-IPLFinal.IntentSlot-season"
            }
          }
        ]
      }
    ]
  }
}
```  
This JSON object represents the entire Language Model of the skill, defining intentes and their utterances, custom slots, etc.  
3. Click on Apply Changes and press the `Build Model` button.  


4. Under Configuration Section, For the service endpoint, check the `HTTPS` radio button.

	Put the default URL as `https://bot.<cluster-name>.hasura-app.io/ipl`. (Run `$ hasura cluster status` from root directory to know your cluster name).

	Click next.

5. About SSL certificates, Hasura services have auto generated `LetsEncrypt` Grade A SSL certificates. This means, you have to check the radio button that says `My development endpoint has a certificate from a trusted certificate authority`

	Click next.

6. Your skill is live on the ECHO device associated with your account. Test it by saying **Alexa**, `start IPL Ask`. And Alexa will become your Harsha Bhogle :)

## How to use it as a boilerplate?

The source code lies in the `microservices/bot/app/src` directory. This is a simple application, so the entire code lies in `server.py`.  
You might want to go through the Flask-ask docs (a very quick read).    
