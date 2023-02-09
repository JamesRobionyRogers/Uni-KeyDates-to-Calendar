# Modified from quickstart guide: https://developers.google.com/calendar/api/quickstart/python#prerequisites

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# @return Credentials object
def authenticate():

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # If there are existing credentials available, load them.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # Checking if creds are expired and refreshing them if they are
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Running a local server for authentication and authorization
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the credentials to file for the next run
            # with open('token.json', 'w') as token:
            #     token.write(creds.to_json())

    return creds
