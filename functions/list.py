import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def event_list(service, calendarID, num_of_results):
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  print("Getting the upcoming 10 events")
  print(now)
  events_result = (
      service.events()
      .list(
          calendarId=calendarID,# "primary"
          timeMin=now,
          maxResults=num_of_results, # 10
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])

  if not events:
    print("No upcoming events found.")

  # Prints the start and name of the next 10 events
  for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    print(start, event["summary"])