#for openai assistant
from openai import OpenAI
import json

#to get current time
import datetime
import os.path

#send requests to google calendar api
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#function to get credentials to authenticate- if error, likely token expired, delete token.json to obtain new token
from authenticate import get_credentials

client = OpenAI()

calendarID = "primary"

#create events
def schedule_event(service, start_time, end_time, event_description, timezone):
    event = {
    'summary': event_description, #'Google I/O 2015'
    'start': {
        'dateTime': start_time, # '2015-05-28T09:00:00-07:00'
        'timeZone': timezone, # 'America/Los_Angeles'
    },
    'end': {
        'dateTime': end_time, # '2015-05-28T17:00:00-07:00'
        'timeZone': timezone, # 'America/Los_Angeles'
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 15},
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    event_link = event.get('htmlLink')
    print('Event created:', event_link)
    return json.dumps({"start_time": start_time, "end_time": end_time, "event_link": event_link,})


def create_event(service, messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "schedule_event",
                "description": "schedule an event in my calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "string",
                            "description": "The start time of the event, in ISO 8601 format"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time of the event in ISO 8601 format"
                        },
                        "event_description":{
                            "type": "string",
                            "description": "A brief description of the event, e.g. Dinner with Lisa"
                        },
                        "timezone":{
                            "type": "string",
                            "description": "any city in the timezone, e.g. America/Los_Angeles"
                        },

                    },
                    "required": ["start_time", "end_time", "timezone"],
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message

    #response from first agent
    # print("This should be the locations:", response_message)
    tool_calls = response_message.tool_calls

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        available_functions = {
            "schedule_event": schedule_event,
        } 
        messages.append(response_message) 


        
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                service=service,
                start_time=function_args.get("start_time"),
                end_time=function_args.get("end_time"),
                event_description=function_args.get("event_description"),
                timezone=function_args.get("timezone"),
            )

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
        ) 
        return second_response
