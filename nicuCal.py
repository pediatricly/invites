#! /usr/bin/python
'''
I was all excited about writing this to generate Google Calendar links given a
list of dates when I have NICU night shifts (easy cuz mine are all 16hr nights
so all have the same start/stop times.
But then I realized it's even easier - fewer clicks, imports to whichever
calendar I want - just to put these data into a spreadsheet, save as csv and
import.
Calendar Maker in LPCH NICU on GDrive has the format for this.
'''

import datetime as DT
from urllib import urlencode

shifts = [(7,5),
          (7,24),
          (8, 18),
          (8, 28),
          (9, 10),
          (9, 21),
          ]




outfile = 'nicuCalLinks.html'
htmlHeader = '''<!DOCTYPE html>
<html>
      <head>
              <meta charset="utf-8">
              <meta name="description" content="NICU Shifts">
              <link rel="stylesheet" href="">

	      <title>NICU Shifts</title>
      </head>

      <body>
'''
htmlFooter = '''
</body>
</html>'''

eName = 'NOC'
calDetails = ''
location = 'LPCH, 725 Welch Rd, Palo Alto, CA 94304'
eStartT = DT.time(16,0,0,0) #Start time in 24-hr
eStopT = DT.time(8,00,0,0)
today = DT.datetime.now()
currentYear = today.year
currentMonth = today.month
calLinks = []

for shift in shifts:
    month = shift[0]
    day = shift[1]

    if month < currentMonth: year = currentYear + 1
    else: year = currentYear
    eDateD = DT.date(year, month, day)
    eDate2D = eDateD + DT.timedelta(days=1)

    eStartDT = DT.datetime.combine(eDateD, eStartT)
    eStopDT = DT.datetime.combine(eDate2D, eStopT)

    utc = DT.datetime.utcnow()
    utcOffset = utc - today
    eStartDTU = eStartDT + utcOffset #+ DT.timedelta(hours=3) #This corrects for my IX webhost which runs on EST
    eStopDTU = eStopDT + utcOffset #+ DT.timedelta(hours=3)
    str1 = eStartDTU.strftime('%Y%m%dT%H%M00Z')
    str2 = eStopDTU.strftime('%Y%m%dT%H%M00Z')
    calDates = str1 + '/' + str2
    calQuery = {'action' : 'TEMPLATE', 'text' : eName, 'dates' : calDates,
                'details' : calDetails, 'location' : location}
    linkBase = 'http://www.google.com/calendar/event?'
    qs = urlencode(calQuery)
    calLink = linkBase + qs
    print calLink
    calLinks.append(calLink)

with open(outfile, 'wb') as outhtml:
    outhtml.write(htmlHeader)
    for i, link in enumerate(calLinks):
        text = 'Add Shift ' + str(i+1)
        line = '<a href="%s" target="_blank">%s</a><br>' % (link, text)
        outhtml.write(line)
    outhtml.write(htmlFooter)
# eDateStart = eStartDT.strftime("%A, %d %b %Y %I:%M %p")
# eDateStop = eStopDT.strftime("%A, %d %b %Y %I:%M %p")
# eDate = eDateD.strftime("%A, %d %b %Y")
# eDate2 = eDate2D.strftime("%A, %d %b %Y")
# eStart = eStartT.strftime("%I:%M %p")
# eStop = eStopT.strftime("%I:%M %p")


