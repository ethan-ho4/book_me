import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from authenticate import get_credentials
from functions.insert import event_insert
from functions.weekly_insert import event_weekly_insert
from functions.list import event_list

from mistral.mistral_client import mistral

MISTRAL_SERVER_URL = "http://127.0.0.1:5000/v1/chat/completions"

SCOPES = ['https://www.googleapis.com/auth/calendar']
service = build("calendar", "v3", credentials=get_credentials(SCOPES))

now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
print("the date is:", now)

calendarID = "primary"
num_of_results = 10

summary = 'Google I/O 2015'
location = '800 Howard St., San Francisco, CA 94103'
start_date_time = '2015-05-28T09:00:00-07:00'
end_date_time = '2015-05-28T17:00:00-07:00'
timezone = 'America/Los_Angeles'

# event_weekly_insert(service,summary, location, start_date_time, end_date_time, timezone)
# event_insert(service,summary, location, start_date_time, end_date_time, timezone)
# event_list(service, calendarID, num_of_results)

# command = "create an event from april 5, 2pm to 5 pm, in toronto, and call it meeting with jane"

# identify_path_prompt = 'Analyze the following task instruction:', command, 'Compare this task with the two options below to determine which one it most closely resembles: (a) Create an event in the calendar. (b) Retrieve the next 10 events from the calendar. Evaluate the essence and intent of the instruction, considering the actions described and their objectives. Your response should consist solely of the letter (either (a) or (b)) corresponding to the option that best matches the task instruction, ensuring clarity and precision in identifying the intended action for the most accurate outcome.'


# path_mistral = mistral(MISTRAL_SERVER_URL, identify_path_prompt)
# print("Response:", path_mistral)

# if path_mistral == "(b)":
#     identify_values_prompt = 'Todays current date time is:', now, 'From this sentence:', command, 'identify these values from the sentence and return it as an array. Return start time and end time in the same format as current date time title, location, start time, end time'
#     value_mistral = mistral(MISTRAL_SERVER_URL, identify_values_prompt)
#     print("value mistral:", value_mistral)