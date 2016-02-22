#! /usr/bin/python26
import csv
from string import Template
import datetime as DT
from invitesConfig import *
#import pytz
print "Content-type:text/html\r\n\r\n"

print '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="description" content="Current RSVP List">
    <link rel="stylesheet" href="http://www.pediatricly.com/css/invites.css">
    <title>Current RSVP List</title>
</head>
<body>
'''
now = DT.datetime.now().isoformat()
print '<h2>RSVP List for %s</h2>' % eName
print '<h4>Current as of %s</h4>' % now

yeses = 0
maybes = 0
nos = 0
print '<table style="width:100%">'

with open(rsvpCSV) as rsvpOpen:
    for i, line in enumerate(rsvpOpen):
        print '<tr>'
        cells = line.split(',')
        if cells[rsvpSlot] == yes:
            yeses += 1
        elif cells[rsvpSlot] == maybe:
            maybes +=1
        elif cells[rsvpSlot] == no:
            nos += 1
        if i == 0:
            for cell in cells:
                print '<th>' + str(cell) + '</th>'
        else:
            for cell in cells:
                print '<td>' + str(cell) + '</td>'
        print '</tr>'

print '</table><p>'

print '<strong>Yes: %s<br>' % yeses
print '<strong>Maybe: %s<br>' % maybes
print '<strong>No: %s<br></p>' % nos
