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
    <meta name="description" content="Current Vote List">
    <link rel="stylesheet" href="http://www.pediatricly.com/css/invites.css">
    <title>Current Vote List</title>
</head>
<body>
'''
now = DT.datetime.now().isoformat()
print '<h2>Vote List for %s</h2>' % eName
print '<h4>Current as of %s</h4>' % now

yeses = 0
maybes = 0
nos = 0
print '<table>'

with open(voteCSV) as voteOpen:
    # print voteOpen.read()
    for i, line in enumerate(voteOpen):
        print '<tr>'
        cells = line.split(',')
        if cells[voteSlot] == choices[0]:
            yeses += 1
        elif cells[voteSlot] == choices[1]:
            maybes +=1
        elif cells[voteSlot] == choices[2]:
            nos += 1
        if i == 0:
            for cell in cells:
                print '<th>' + str(cell) + '</th>'
        else:
            for cell in cells:
                print '<td>' + str(cell) + '</td>'
        print '</tr>'

print '</table><p>'

print '<strong>%s: %s<br>' % (choices[0], yeses)
print '<strong>%s: %s<br>' % (choices[1], maybes)
print '<strong>%s: %s<br></p>' % (choices[2], nos)
