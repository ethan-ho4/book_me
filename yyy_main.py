#for openai assistant
from openai import OpenAI
import json

#to get current time
import datetime
import pytz
import os.path

#send requests to google calendar api
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#function to get credentials to authenticate- if error, likely token expired, delete token.json to obtain new token
from authenticate import get_credentials

from yyy_decision_matrix_function import decision_matrix
from yyy_create_event import create_event
from yyy_return_event import return_event

# current_datetime= datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

def get_taiwan_datetime():
    utc_now = datetime.datetime.utcnow()
    taiwan_tz = pytz.timezone('Asia/Taipei')
    taiwan_now = utc_now.replace(tzinfo=pytz.utc).astimezone(taiwan_tz)
    return taiwan_now.isoformat()

current_datetime = get_taiwan_datetime()
print(current_datetime)

SCOPES = ['https://www.googleapis.com/auth/calendar']
service = build("calendar", "v3", credentials=get_credentials(SCOPES))

# user_message = "Put in my calendar that I have a meeting with Jessica from 2 to 4."
# user_message = "List the next 5 events in my calendar."

user_message = "interview with chen about tomorrow 4:00 PM"

messages = [{"role": "user", "content": f"Today is {current_datetime} taiwan time. {user_message}"}]

path = decision_matrix(messages) # create_event or return_event
print("this is the path to follow:", path)

if path == "create_event":
    response = create_event(service, messages)

elif path == "return_event":
    response = return_event(service, messages)

content = response.choices[0].message.content

print(content)



