from authenticateUser import authenticate

# Importing modules for webscraping
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Importing modules for google calendar api
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scraping the webpage and getting the data
url = "https://www.otago.ac.nz/news/events/keydates/"
responce = requests.get(url)
soup = BeautifulSoup(responce.text, "html.parser")
data = {}

# Stores all the months
months = soup.select(" #content > div > h2")

# Stores all the Dates and Events from each month 
months_tables = soup.select("#content > div > dl")

# Processing the events into a dictionary
for i in range(12):
    month_key = months[i].text          # month text eg. "January" 
    month_events = months_tables[i]     

    # Appendng the events to the month key in the dictionary
    data[month_key] = month_events

# Irterate through each month and create a dictionaly of key = date and value = event
for month in data:
    events = data[month]
    event_dict = {}

    # Iterate over each dt and dd elements 
    for i in range(len(events.select("dt"))):
        date = events.select("dt")[i].text
        event = events.select("dd")[i].text

        # convert date to datetime object from this format: Monday, 9 January
        date = datetime.strptime(date, "%A, %d %B").replace(year=2023)

        # Append the date and event to the dictionary
        event_dict[date] = event

    # Replace the list of events with the dictionary
    data[month] = event_dict


# Defining a filter for events 
filter_words = ['fees', 'begin', 'end', 'semester']
# Thanks for ChatGPT for this filter code
filtered_events = {month: {date: event for date, event in events.items() if any(word in event for word in filter_words)} for month, events in data.items()}

# Google Calendar API

# Authenticating the user via local webserver and building the service
creds = authenticate()

# Try to create the service followed by the resulting events 
try:
    # Calendar to insert event into: 'UoO Key Dates'
    calendar_id = 'fe37442ef0332cbc52ec1e0e61f1b966e5b7e3c5d4c1ab0ce860789253b2bc38@group.calendar.google.com'

    service = build('calendar', 'v3', credentials=creds)

    # Iterating over the data dict storing the months and events
    for month, events in filtered_events.items():

        print(month)

        for date, event_title in events.items():
            event = {
                'summary': f'{event_title}',
                'location': 'University of Otago, 362 Leith Street, Dunedin North, Dunedin 9016, New Zealand',
                # 'description': '',
                'start': {
                    'date': f'{date.date()}',
                },
                'end': {
                    'date': f'{date.date()}',
                },
                'transparency': 'transparent',
                'visibility': 'public'
            }

    
            # Executing the event creation
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")

            # TESTING: Printing the filtered events 
            print(event)

except HttpError as error:
    print(f'[ERROR] : {error}')


