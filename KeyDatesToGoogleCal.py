# Importing essentual modules
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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



# Iterate over the data printing the events date and name 
for month in data:
    events = data[month]
    for date in events:
        print(date, events[date])
    print("\n\n")

# for i in data["January"].keys():
#     print(i)


