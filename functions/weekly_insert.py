# import datetime
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

def event_weekly_insert(service, summary, location, start_date_time, end_date_time, timezone, day):
    day_dict = {
    "Monday": "MO",
    "Tuesday": "TU",
    "Wednesday": "WE",
    "Thursday": "TH",
    "Friday": "FR",
    "Saturday": "SA",
    "Sunday": "SU"
    }

    set_day = day_dict(day, "Invalid day")

    event = {
    'summary': summary, #'Google I/O 2015'
    'location': location, # '800 Howard St., San Francisco, CA 94103'
    # 'description': "",
    'start': {
        'dateTime': start_date_time, # '2015-05-28T09:00:00-07:00'
        'timeZone': timezone, # 'America/Los_Angeles'
    },
    'end': {
        'dateTime': end_date_time, # '2015-05-28T17:00:00-07:00'
        'timeZone': timezone, # 'America/Los_Angeles'
    },
    'recurrence': [
        f"RRULE:FREQ=WEEKLY;BYDAY={set_day}"

    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 15},
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))
