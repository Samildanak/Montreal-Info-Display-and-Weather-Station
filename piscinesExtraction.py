import os
import requests
from bs4 import BeautifulSoup

def extractPage(url, pagepath='page'):
    session = requests.Session()
    #... whatever other requests config you need here
    response = session.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    path, _ = os.path.splitext(pagepath)
    actualHours = soup.find("h3", string = "Pour les adultes").parent

    timeScheduleString = ""
    timeIndex = 0
    timeScheduleHtml = actualHours.parent.parent.div.div
    for div in timeScheduleHtml:
        for time in div:
            timeScheduleString += time.text
            if timeIndex == 0:
                timeScheduleString += " "
            timeIndex += 1
    return actualHours, timeScheduleString

def beautifyDict(actualHoursHtml):
    actualHoursDict = {}
    for day in actualHoursHtml.div.table.tbody:
        try:
            actualHoursDict[day.td.text] = ""
            for hours in day:
                if hours.text == day.td.text:
                    continue
                actualHoursDict[day.td.text] = hours.text
        except:
            pass
    return actualHoursDict


url = 'https://montreal.ca/lieux/piscine-saint-roch'
actualHours, timeSchedule = extractPage(url)
beautifyDict(actualHours)

print(timeSchedule)