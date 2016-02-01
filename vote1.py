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
email = form.getvalue('email')
vote = form.getvalue('vote')
'''

email = "dblockvk@gmail.com"
FName = 'Mike'
vote = 'Marlowe'
'''

cgiList = [email, FName, vote]
cgiNameList = ['email', 'FName', 'vote']
cgiErr = 0
if None in cgiList:
    cgiErr = 1

#==================================================================================
import csv
import os.path
from urllib import urlencode
from string import Template
import datetime as DT
from invitesConfig import *
#import pytz

###################################################################
### Define Globals
###################################
try: version = os.path.basename(__file__)
except: version = 'vote1'

voteDict = {}

timeStampDT = DT.datetime.now()
timeStamp = timeStampDT.strftime("%Y%m%d_%H%M")
###################################################################
### Store the CGI form data in outfile
###################################################################
cgiList.append(timeStamp)
cgiNameList.append('timeStamp')

with open(voteCSV) as csvopen:
    reader = csv.DictReader(csvopen, fieldnames=cgiNameList)
    for row in reader:
        if row['email'] != 'email':
            voteDict[row['email']] = row
# Populates voteDict with the old vote csv as a dict of dicts. This is just to
# make it easy to update new vote's using email as the main key. As such, that
# last line sets email as the key of the big dict:
# {'mdsc@gmail.com': {'LName': ' Scahill', 'timeStamp': ' 20160107_2101',
# 'email': 'mdsc@gmail.com', 'FName': ' Mike', 'vote': ' yes'}, 'email@u.com' :
# {'LName':...

newVote = dict(zip(cgiNameList, cgiList))
# zip is a nifty function that turns 2 lists into a dict, aka turns 2 vectors
# len = m into an m x 2 matrix. (Also works to make a list of lists)

voteDict[email] = newVote
# Finally, this makes the new entry from CGI data into the {email : {dict}}
# format and adds / overwrites it into the voteDict

with open(voteCSV, 'w') as csvopen:
    writer = csv.writer(csvopen)
    writer.writerow(cgiNameList)
#Py2.6 on IXWeb doesn't support DictWriter.writeheaders(), hence the clumsy
#2 writer objects
    dictWriter = csv.DictWriter(csvopen, fieldnames=cgiNameList)
    for item in voteDict:
        row = voteDict.get(item, cgiNameList)
        dictWriter.writerow(row)

###################################################################
### Use the string.Template to store custom HTML as a big string
###################################################################

templateFH = open(votehtmlTemplate, 'r')
mainTemplate = templateFH.read()

templateVars = dict(eName=eName, eDate=eDate, eStart=eStart, eStop=eStop,
                    location=location, FName=FName, vote=vote, bonus=voteBonus,
                    custom=voteCustom, version=version, cutoff=cutoff,
                    imgUrl=imgUrl, blastTax=voteBlastTax)

finalHTML = Template(mainTemplate).safe_substitute(templateVars)

# Save for local debugging, not CGI
# outfile2 =  open("vote1_templated.html", 'w')
# outfile2.write(finalHTML)

###################################################################
### For CGI, print the final templated HTML
###################################################################
if cgiErr ==1:
    cgiErrTemplateFH = open(voteErrTemplate, 'r')
    cgiErrTemplate = cgiErrTemplateFH.read()
    print "Content-type:text/html\r\n\r\n"
    print Template(cgiErrTemplate).safe_substitute(version=version,
                                                   blastTax=voteBlastTax,
                                                   imgUrl=imgUrl)
else:
    print "Content-type:text/html\r\n\r\n"
    # Need this header to start off the html file in CGI (not when saving html)

    print finalHTML


