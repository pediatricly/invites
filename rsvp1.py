#! /usr/bin/python26

'''
What am I doing?
Started 7 Jan 16. Conceived Nov-Dec 15 as part of the invites project
First implementation 7 Jan 16 for Symposium JPM Health Summit dinner RSVPs

This is just a CGI page to take RSVPs / votes. It just has to store data passed
using the cgi FieldStorage() to some outfile & show a confirmation message in
html using a template.

Info is all really generated in URLs sent via an email mail merge.

For first pass, collect:
    - FName, LName
    - email, for convenience & unique ID
    - yes, no, maybe
    - vote field, in this case for restaurant choice

Gravy would be add to Calendar or a link to an invite
More gravy - little Google Map image of the locale
More gravy - blast tax window!

'''

#################################################################################
#####   CGI Setup
#####   from the qualcgi1.py file. Put this first so you capture errors
#################################################################################
#try:

import cgi, cgitb
# Debugging - has the webserver print a traceback instead of just a page
# not found error if there's an error in the code
cgitb.enable()

# cgi.escape() I think this is a security feature to keep people from
# entering code into input fields
# Create instance of FieldStorage
form = cgi.FieldStorage()
FName = form.getvalue('FName')
LName = form.getvalue('LName')
email = form.getvalue('email')
rsvp = form.getvalue('rsvp')
#vote = form.getvalue('vote')
'''

LName = "Scahill"
FName = "Mike"
email = 'mdscahill@gmail.com'
rsvp = "yes"
#vote = None
'''

cgiList = [email, FName, LName, rsvp]
cgiNameList = ['email', 'FName', 'LName', 'rsvp']
if None in cgiList:
    raise NameError
#except: pass

#==================================================================================
import csv
import os.path
from urllib import urlencode
from string import Template
import datetime as DT
#import pytz

###################################################################
### Define Globals
###################################
try: version = os.path.basename(__file__)
except: version = 'rsvp1'

csvfile = 'rsvpLog1.csv'
htmlTemplate = 'rsvpTemplate1.html'
errTemplate = 'rsvpErrTemp1.html'
blastTax = ''
closedHTML = 'rsvpClosed.html'

# How are you defining the votes - careful that the input URL needs to match
# this
yes = 'yes'
maybe ='maybe'
no = 'no'
rsvpDict = {}

# Event Details
eName = 'GSB JPM Med-Biz After-After Party'
eDateD = DT.date(2016, 1, 13)
eDate2D = eDateD # Assumes same start & stop date, can change here
#pst = pytz.timezone('US/Pacific')
eStartT = DT.time(20,0,0,0) #Start time in 24-hr
eStopT = DT.time(21,30,0,0) #using pytz, add: , pst) to get tmzone support
location = "TBD - vote below if you're coming!"
cutoffD = DT.date(2016, 1, 10)
timeStampDT = DT.datetime.now()
###################################################################
### Make the date & times pretty
###################################################################
eStartDT = DT.datetime.combine(eDateD, eStartT)
eStopDT = DT.datetime.combine(eDate2D, eStopT)

eDateStart = eStartDT.strftime("%A, %d %b %Y %I:%M %p")
eDateStop = eStopDT.strftime("%A, %d %b %Y %I:%M %p")
eDate = eDateD.strftime("%A, %d %b %Y")
eStart = eStartT.strftime("%I:%M %p")
eStop = eStopT.strftime("%I:%M %p")
cutoff = cutoffD.strftime("%A, %d %b %Y")
timeStamp = timeStampDT.strftime("%Y%m%d_%H%M")
###################################################################
### Store the CGI form data in outfile
###################################################################
if DT.date.today() <= cutoffD:
    cgiList.append(timeStamp)
    cgiNameList.append('timeStamp')

    with open(csvfile) as csvopen:
        reader = csv.DictReader(csvopen, fieldnames=cgiNameList)
        for row in reader:
            if row['email'] != 'email':
                rsvpDict[row['email']] = row
# Populates rsvpDict with the old rsvp csv as a dict of dicts. This is just to
# make it easy to update new rsvp's using email as the main key. As such, that
# last line sets email as the key of the big dict:
# {'mdsc@gmail.com': {'LName': ' Scahill', 'timeStamp': ' 20160107_2101',
# 'email': 'mdsc@gmail.com', 'FName': ' Mike', 'rsvp': ' yes'}, 'email@u.com' :
# {'LName':...

    newRsvp = dict(zip(cgiNameList, cgiList))
# zip is a nifty function that turns 2 lists into a dict, aka turns 2 vectors
# len = m into an m x 2 matrix. (Also works to make a list of lists)

    rsvpDict[email] = newRsvp
# Finally, this makes the new entry from CGI data into the {email : {dict}}
# format and adds / overwrites it into the rsvpDict

    with open(csvfile, 'w') as csvopen:
        writer = csv.writer(csvopen)
        writer.writerow(cgiNameList)
#Py2.6 on IXWeb doesn't support DictWriter.writeheaders(), hence the clumsy
#2 writer objects
        dictWriter = csv.DictWriter(csvopen, fieldnames=cgiNameList)
        for item in rsvpDict:
            row = rsvpDict.get(item, cgiNameList)
            dictWriter.writerow(row)
else: pass

###################################################################
### Use the string.Template to store custom HTML as a big string
###################################################################
customTemplate = """
<b>Would you like to vote on where we go for dinner?</b><br>
Click the name for the Yelp listing. Click "Vote" to cast your ballot.
<ul>
<li><a href="http://www.yelp.com/biz/marlowe-san-francisco-2" target="_blank">Marlowe</a> | <a href="$link1">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/tropisue%C3%B1o-san-francisco-3" target="_blank">Tropisueno</a> | <a href="$link2">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/t%C3%ADn-vietnamese-cuisine-san-francisco-3" target="_blank">Tin Vietnamese</a> | <a href="$link3">[Vote!]</a></li>
</ul>
"""

urlBase = 'http://www.pediatricly.com/cgi-bin/vote1.py?'
choices = ['Marlowe', 'Tropisueno', 'Tin_Vietnamese']
choiceUrls = []
for vote in choices:
    urlVars = {'email' : email, 'FName' : FName, 'vote' : vote}
    suffix = urlencode(urlVars)
    choiceUrls.append(urlBase+suffix)

link1 = choiceUrls[0]
link2 = choiceUrls[1]
link3 = choiceUrls[2]

customHTML = Template(customTemplate).safe_substitute(link1=link1, link2=link2,
                                                  link3=link3)
custom = ''
# if vote == yes or vote == maybe:
bonus = ''
if rsvp == yes:
    bonus = "Can't wait to see you there!"
    custom = customHTML
elif rsvp == maybe:
    bonus = "Hope that turns into a yes. Keep us posted."
    custom = customHTML
else:
    bonus == "Will be sorry to miss you!"

customClosed = ''

templateVars = dict(eName=eName, eDate=eDate, eStart=eStart, eStop=eStop,
                    location=location, FName=FName, rsvp=rsvp, bonus=bonus,
                    custom=custom, customClosed=customClosed, version=version,
                    cutoff=cutoff)

if DT.date.today() <= cutoffD:
    templateFH = open(htmlTemplate, 'r')
    mainTemplate = templateFH.read()
    finalHTML = Template(mainTemplate).safe_substitute(templateVars)
else:
    templateFH = open(closedHTML, 'r')
    closedTemplate = templateFH.read()
    finalHTML = Template(closedTemplate).safe_substitute(templateVars)

# Save for local debugging, not CGI
# outfile2 =  open("rsvp1_templated.html", 'w')
# outfile2.write(finalHTML)


###################################################################
### For CGI, print the final templated HTML
###################################################################


'''
if NameError:
    cgiErrTemplateFH = open(errTemplate, 'r')
    cgiErrTemplate = cgiErrTemplateFH.read()
    print "Content-type:text/html\r\n\r\n"
    print Template(cgiErrTemplate).safe_substitute(version=version,
                                                   )
else:
'''
print "Content-type:text/html\r\n\r\n"
# Need this header to start off the html file in CGI (not when saving html)

print finalHTML


