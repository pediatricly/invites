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

31jan16: started parameterization by creating invitesConfig to minimize edits
that need to be made here. Almost everything (except >3 vote links in custom)
can now be set in one place in invitesConfig.

Gravy would be add to Calendar or a link to an invite
More gravy - little Google Map image of the locale
More gravy - blast tax window!

'''
import csv
import os.path
from urllib import urlencode
from string import Template
import datetime as DT
from invitesConfig import *
#import pytz
print "Content-type:text/html\r\n\r\n"
#################################################################################
#####   CGI Setup
#####   from the qualcgi1.py file. Put this first so you capture errors
#################################################################################
try:
    import cgi, cgitb
    # Debugging - has the webserver print a traceback instead of just a page
    # not found error if there's an error in the code
    cgitb.enable()

    # cgi.escape() I think this is a security feature to keep people from
    # entering code into input fields
    # Create instance of FieldStorage
    form = cgi.FieldStorage()
    FName = form.getvalue(FNameStr)
    LName = form.getvalue(LNameStr)
    email = form.getvalue(emailStr)
    rsvp = form.getvalue(rsvpStr)
    #vote = form.getvalue('vote')
except: pass
'''

LName = "Scahill"
FName = "Mike"
email = 'mdscahill@gmail.com'
rsvp = "maybe"
#vote = None
'''
cgiListRSVP = [email, FName, LName, rsvp]
cgiErr = 0
if None in cgiListRSVP:
    cgiErr = 1

###################################################################
### Define Globals
###################################
try: version = os.path.basename(__file__)
except: version = 'rsvp'

rsvpDict = {}
timeStampDT = DT.datetime.now()
timeStamp = timeStampDT.strftime("%Y%m%d_%H%M")

###################################################################
### Store the CGI form data in outfile
###################################################################
if DT.datetime.now() <= cutoffD:
    cgiListRSVP.append(timeStamp)
    cgiNameListRSVP.append('timeStamp')

    with open(rsvpCSV) as csvopen:
        reader = csv.DictReader(csvopen, fieldnames=cgiNameListRSVP)
        for row in reader:
            if row['email'] != 'email':
                rsvpDict[row['email']] = row
# Populates rsvpDict with the old rsvp csv as a dict of dicts. This is just to
# make it easy to update new rsvp's using email as the main key. As such, that
# last line sets email as the key of the big dict:
# {'mdsc@gmail.com': {'LName': ' Scahill', 'timeStamp': ' 20160107_2101',
# 'email': 'mdsc@gmail.com', 'FName': ' Mike', 'rsvp': ' yes'}, 'email@u.com' :
# {'LName':...

    newRsvp = dict(zip(cgiNameListRSVP, cgiListRSVP))
# zip is a nifty function that turns 2 lists into a dict, aka turns 2 vectors
# len = m into an m x 2 matrix. (Also works to make a list of lists)

    rsvpDict[email] = newRsvp
# Finally, this makes the new entry from CGI data into the {email : {dict}}
# format and adds / overwrites it into the rsvpDict

    with open(rsvpCSV, 'w') as csvopen:
        writer = csv.writer(csvopen)
        writer.writerow(cgiNameListRSVP)
#Py2.6 on IXWeb doesn't support DictWriter.writeheaders(), hence the clumsy
#2 writer objects
        dictWriter = csv.DictWriter(csvopen, fieldnames=cgiNameListRSVP)
        for item in rsvpDict:
            row = rsvpDict.get(item, cgiNameListRSVP)
            dictWriter.writerow(row)
else: pass

###################################################################
### Store HTML with string.Template
###################################################################
# This section generates & templates personalized urls for voting in the custom
# section. It draws on the overall customRsvpTemplate, urlBase & choices from
# config.
# It's fine to have no such links & just random custom text
# *BUT* more than 3 urls would require going in here and adding link4 etc
choiceUrls = []
if len(choices) > 0:
    for vote in choices:
        urlVars = {emailStr : email, FNameStr : FName, LNameStr : LName,
                   voteStr : vote}
        suffix = urlencode(urlVars)
        choiceUrls.append(urlBase+suffix)

try:
    link1 = choiceUrls[0]
except: link1 = ''
try:
    link2 = choiceUrls[1]
except: link2 = ''
try:
    link3 = choiceUrls[2]
except: link3 = ''


# The general RSVP personalized text
bonus = ''
if rsvp == yes:
    customYesHTML = Template(customYesTemplate).safe_substitute(link1=link1,
                                                              link2=link2,
                                                              link3=link3)
    bonus = bonusYes
    custom += customYesHTML
elif rsvp == maybe:
    customMaybeHTML = Template(customMaybeTemplate).safe_substitute(link1=link1,
                                                              link2=link2,
                                                              link3=link3)
    bonus = bonusMaybe
    custom += customMaybeHTML
else:
    customNoHTML = Template(customNoTemplate).safe_substitute(link1=link1,
                                                              link2=link2,
                                                              link3=link3)
    bonus = bonusNo
    custom += customNoHTML

templateVars = dict(eName=eName, eDate=eDate, eStart=eStart, eStop=eStop,
                    location=location, FName=FName, rsvp=rsvp, bonus=bonus,
                    custom=custom, customClosed=customClosed, version=version,
                    cutoff=cutoff, imgUrl=imgUrl, blastTax=rsvpBlastTax,
                    calLink=calLink)

# Use closed template if today > cutoffD
if DT.datetime.now() <= cutoffD:
    templateFH = open(rsvphtmlTemplate, 'r')
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

if cgiErr == 1:
    cgiErrTemplateFH = open(rsvpErrTemplate, 'r')
    cgiErrTemplate = cgiErrTemplateFH.read()
    print Template(cgiErrTemplate).safe_substitute(version=version,
                                                   blastTax=rsvpBlastTax,
                                                   imgUrl=imgUrl)
else:
    # Need this header to start off the html file in CGI (not when saving html)

    print finalHTML


