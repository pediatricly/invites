#!/usr/bin/python

# IX Web needs this shebang for the better Python verion
#!/usr/bin/python2.6

"""
Started on a whim, 7dec15. Realized I could make a system for homebrew invites.
This script does the mail merge. Generates custom email that includes custom
RSVP links
Those links, at least for yes & maybe, should go to a CGI form that allows
specification of +1s, stuff to bring, public response, etc. Could even figure
out how to make a custom Google Cal link, FB event link, etc on form. Includes
map, stats, photos, etc.
Super fancy version shows a list of who's going (based on public response).


7jan16 - In a hackathon, I turned this into a functional product for invites to
Symposium afterparty. Shortcut through a few things, so here are my notes:
    Mail Merge: I commented out the email sending function from this script.
    Used YetAnotherMailMerge in GMail. I also replaced silly urlGen with urllib.

    How it works:
        - Set the csv column headers in global. Doesn't need these to read but
        uses them to write the results back out and organize URLs consistently
        - Set invite detail strings. These only get templated into the invite.
        It would be a nice *NEW FEATURE* to import these to/from rsvp1.py because
        I have to set them there as well.
        - Define other vars that the template.html expects & put them in a dict.
        This is what gets used for string.Template later.
        - Setup the parameters that are passed into the rsvp URLs. These appear
        in the formatted invite and must encode the data rsvp1.py is expecting.
        *NEW FEATURE* might be to define a class or somehow import them so they
        are assured to be consistent even when changing vars / templates.
    Then the code does the rest:
        - Read the contacts csv into a list of dicts
        - Read the template html (strip into a text version. used to read the
        $vars but that was a bad idea)
        - Loop through contacts list & update $vars to customize them. Note that
        only a subset are used. First pass just used nickname & URLs. If you want
        to use say LName (oustide the URL), need to add it to templateDict and
        update it within the loop (eg nickName -> nickNameI)
        - End of the loop, template gets customized. Code is there to send this
        via SMTP directly but ended up saving it to an output csv to use for an
        outside mail merge (GMail's YetAnotherMailMerge seemed to handle the html
        fine).
    Stuff You Need to Setup to Work It:
        - contactsList.csv. I think the dictReader can handle different order
        but best to use what's listed in headers []
        - template.html. Has a bunch of $vars including the key $rsvpURLs
        - rsvp1.py which takes the rsvpURLs, stores data & shows a nice webpage
        - vote1.py is optional for additional data, say conditional on the rsvp.
        It's a second webpage in this sequence.

"""

import urllib2
# import smtplib
import csv
import re
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import os.path
from string import Template
import urllib
from invitesConfig import *

try: version = os.path.basename(__file__)
except: version = 'inviteGen.py'

#########################################################
### Define Globals
##########################################################
'''
sender = 'precipalert@gmail.com'
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login('precipalert', 'sheil@650')
#This seems to work as long as allow low security apps is *relatively* freshly
#set.
'''


# Watch for **templateDict** below. Can't be set here.
# This dict determines which vars go into the invite html template.
# Every $var from template needs to be added there.

##########################################################
### Read in the contact list from csv to list of dicts
##########################################################
'''
Through westValue, saw that a more std, ?better?  data structure seems to be a
list of dicts. (Indeed, JSON & xml are like this.)

This would be:
    [{FName: Mike, LName: Scahill...}, {FName: Michele, LName: D...}...],
'''
while True:
    # contactsCSV = raw_input("Enter contact csv name in working dir: ")
    try:
        fh = open(contactsCSV, 'rb')
        break
    except:
        print "Sorry! I'm having trouble opening that file. Wanna try again?"
        break

contactList = list(csv.DictReader(fh))
#This is a list of dicts with keys col headings & values the indiv data.
#Each dict is one row in the contacts table
fh.close()

receivers = []
for cList in contactList:
    receivers.append(cList[emailStr])
#receivers is the list of emails. Need this separate for the email function
#Actually, I think I won't need it. Probably just want to loop through the
#whole function for each contact row.



##########################################################
### Compose the alert message
##########################################################
htmlTemplate = str(open(inviteTemplate, 'rb').read())
textTemplate = re.sub(r'<[/\w]+>', '', htmlTemplate)
textTempWords = textTemplate.split()

'''
# This loop is really a cheat to make the dict. I don't see anyway to assign
# var names safely from strings. Ran this to get a formatted list & copied it
# to define the templateDict below
#
# This proved buggy, logically dubious and more hassle than it's worth. Just need
# to be careful to match variable names here with what the template expects.

templateVars = []
for word in textTempWords:
    word = re.sub(r'\W$', '', word)
    if word[0] == '$': templateVars.append(word[1:])

for var in templateVars:
    print var + '=' + var + ','
print templateDict
'''

#############################################################
# Want a control step outside the loop so can check the parsing & field assigns
# before sending the emails thru the loop
# OR maybe you can put in a raw_input step in the loop to pause it?
#############################################################

#############################################################
### Loop through the contactList to generate the emails
#############################################################
for person in contactList:
    # Initialize these here as a reminder what $varnames the template string expects
    # for the rsvp urls
    rsvpYesI = ''
    rsvpMaybeI = ''
    rsvpNoI = ''
    nickNameI = ''
    rsvpDict = {}
    for var in rsvpVars:
        rsvpDict[var] = person[var]
    #These are just URLs. The <a> comes from the html template.
    # rsvp1.py  receives these data
    #Eventually, a way to add +1 or message into RSVP easily
    rsvpYesI += rsvpBase + urllib.urlencode(rsvpDict)
    rsvpYesI += '&' + rsvpStr + '=' + yes
    rsvpMaybeI += rsvpBase + urllib.urlencode(rsvpDict)
    rsvpMaybeI += '&' + rsvpStr + '=' + maybe
    rsvpNoI += rsvpBase + urllib.urlencode(rsvpDict)
    rsvpNoI += '&' + rsvpStr + '=' + no

    LNameI = person[LNameStr]
    FNameI = person[FNameStr]
    emailI = person[emailStr]
    newI = person[newStr]
    if newI != '':
        newBonusI = newBonus
    else:
        newBonusI = ''
    custom1I = person[custom1Str]
    custom2I = person[custom2Str]
    nickNameI = person[nickNameStr]
    if person[newStr] == 'y':
        newI = newBonus
    else:
        newI = ''
    templateDict = dict(nickNameI=nickNameI, LNameI=LNameI, FNameI=FNameI,
                    eName=eName, emailI=emailI, eStart=eStart, eStop=eStop,
                    eDate = eDate, eDate2=eDate2, location=location,
                    cutoff=cutoff, rsvpYesI=rsvpYesI, rsvpMaybeI=rsvpMaybeI,
                    rsvpNoI=rsvpNoI, newI=newI, custom1I=custom1I,
                        custom2I=custom2I)

    finalHTML = Template(htmlTemplate).safe_substitute(templateDict)
    finalText = Template(textTemplate).safe_substitute(templateDict)
    '''
# This section is needed only when using SMTP directly in this script to
# generate the email messages
    recipient = person[email]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    part1 = MIMEText(finalText, 'plain')
    part2 = MIMEText(finalHTML, 'html')

    msg.attach(part1)
    msg.attach(part2)
    print msg
    '''

# When not using SMTP here, next line adds the personally formatted message to
# the contacts list of dicts
    person[msgHTMLStr] = finalHTML


#############################################################
### For outside mail merge, write the contact list including the formatted
### message to an output csvfile
#############################################################
with open(invitesOut, 'wb') as csvout:
    dictWriter = csv.DictWriter(csvout, fieldnames=headers)
    dictWriter.writeheader()
    for person in contactList:
        dictWriter.writerow(person)

    print 'Wrote your messages into %s' % invitesOut


    # mail.sendmail(sender, recipient, msg.as_string())
# Should probably keep these lists in 1 big list of tupules so can loop through
# each field for every recipient
#  - template the text using $var = tupule[#]
#  - send email using receiver = tupule[0] inc custom text field



# Will need to figure out this MIME html business
# Could create an auto text alt by using re.sub on <tag>

'''
#This section below is just copied from precip alert as a reference for how
#the various templates & SMTP commands work

templateVars = dict(location=location, timestamp=timestamp, maxState=maxState,
                    tableOutput=tableText, version=version, hourlySum=hourlySum,
                    dailySum=dailySum)

finalText = Template(textTemplate).safe_substitute(templateVars)
# Degree symbols etc in the JSON unicode break the MIMEText, replace with ascii:
# asciiFinalText = finalText.encode('ascii', 'xmlcharrefreplace')
# xml replace is nice but looks crazy in plain text

asciiFinalText = finalText.encode('ascii', 'ignore')


# Got to make this into a loop so there's only 1 receiver
    msg = MIMEText(asciiFinalText)
    #msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Precipiation Alert: ' + maxState
    msg['From'] = sender
    msg['To'] = receiver
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(userName, password)
    # mail.sendmail(sender, receiver, msg.as_string())
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()
'''

