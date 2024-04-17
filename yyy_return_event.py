
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

# return_event
def list_event(service, number_of_events):
    print("its at the list event block")
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("the date is:", now)

    events_result = (
        service.events()
        .list(
            calendarId=calendarID,# "primary"
            timeMin=now,
            maxResults=number_of_events, # 10
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return json.dumps({"events": events,})

    # Prints the start and name of the next 10 events
    events_list = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event.get("summary", "No title")  # Default to "No title" if summary is missing
        events_list.append({"time": start, "summary": summary})
    
    print(events_list)    
    return json.dumps({"events": events_list,})


def return_event(service, messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_event", # This name must match the function name, in this case the List_event that is called later
                "description": "what are my next events in my calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_events": {
                            "type": "integer",
                            "description": "how many events is being asked for, eg. 5, 10"
                        },

                    },
                    "required": ["number_of_events"],
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
            "list_event": list_event,
        } 
        messages.append(response_message) 
        
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(# things here go into the function above as parameters
                service=service,
                number_of_events=function_args.get("number_of_events"),
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
