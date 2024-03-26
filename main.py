import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from authenticate import get_credentials
from functions.insert import event_insert
from functions.list import event_list

SCOPES = ['https://www.googleapis.com/auth/calendar']
service = build("calendar", "v3", credentials=get_credentials(SCOPES))

# event_insert(service)
event_list(service)
