from authenticateUser import authenticate

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Calendar ID for UoO Key Dates
CALENDAR_ID = 'fe37442ef0332cbc52ec1e0e61f1b966e5b7e3c5d4c1ab0ce860789253b2bc38@group.calendar.google.com'

# Authenticating the user via local webserver and building the service
creds = authenticate()

try:
    checker = input("Are you are you want to delete ALL calendar events? [Y/N]:  ")

    if checker.upper() == "Y":
        service = build('calendar', 'v3', credentials=creds)

        # Get a list of all events on the calendar
        events_result = service.events().list(calendarId=CALENDAR_ID).execute()
        events = events_result.get('items', [])

        # Iterating over the events deleting them 
        for event in events:
            service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
            print(f"Event deleted: {event['summary']}")

        print("\n\nAll events have been deleted.")

except HttpError as error:
    print(f'[ERROR] : {error}')
