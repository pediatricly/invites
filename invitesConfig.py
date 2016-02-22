"""
Planning an event? You've come to the right place...

This is the hub for a suite of files I made Dec-Feb 2016 to create custom
invitations, take RSVPs automatically and even allow for voting (eg on venue).

Basic Flow:
1. Have csv of contacts to invite
2. Create custom invitations using html template and inviteGen.py
3. Send invites with GMail Yet Another Mail Merge or similar
(could use inviteGen's smtp function, too)
4. People who click the links in the invite email are directed to html generated
by rsvp.py
5. Option to direct from rsvp to vote.py
6. Results printed by rsvpList & voteList


How To Use 'Em
1. Figure out your event & whether you need to use votes.
2. Setup contactsCSV with the fields specified in headers
3. Write the invitation email as html and specify the filename below as
inviteTemplate
4. Specify all the parameters below - event details, message snippets, votes etc.
(CGI fields are still strings. Careful if you end up messing with the parameters)
As of 21Feb16, these are the vars you can use in the...
invitation text:
(nickNameI=nickNameI, LNameI=LNameI, FNameI=FNameI,
                    eName=eName, emailI=emailI, eStart=eStart, eStop=eStop,
                    eDate = eDate, eDate2=eDate2, location=location,
                    cutoff=cutoff, rsvpYesI=rsvpYesI, rsvpMaybeI=rsvpMaybeI,
                    rsvpNoI=rsvpNoI, newHTML=newHTML)

rsvp page:
(eName=eName, eDate=eDate, eStart=eStart, eStop=eStop,
                    location=location, FName=FName, rsvp=rsvp, bonus=bonus,
                    custom=custom, customClosed=customClosed, version=version,
                    cutoff=cutoff, imgUrl=imgUrl, blastTax=rsvpBlastTax)

vote page:
(eName=eName, eDate=eDate, eStart=eStart, eStop=eStop,
                    location=location, FName=FName, vote=vote, bonus=voteBonus,
                    custom=voteCustom, version=version, cutoff=cutoff,
                    imgUrl=imgUrl, blastTax=voteBlastTax)
Cutoff is big. rsvp.py essentially shuts off for new responses at that time.

5. Run inviteGen.py. Emails in HTML are output into the msgHTML column.
6. Use GMail YAMM or similar to send those custom emails. (Use an essentially
blank email draft with $%msgHTML% to pull that in. Should preserve the HTML
format)
7. Links in those emails pipe CGI data into rsvp.py which stores rsvps in
rsvpLog1.csv. These are unique by email and timestamped when gathered. New rsvp
with same email overwrite the old rsvp.
After cutoff, rsvp attempts are not saved and the rsvpClosed.html is shown.
8. If you specified voting (below), votes direct from rsvp to vote.py. Votes are
logged in voteLog1.csv. Same as rsvp, votes are unique by email and overwrite if
a second vote comes from the same email.
9. Can view rsvps and votes simply in rsvpList & voteList


"""
import datetime as DT
from string import Template


###################################################################
# For all pages:
###################################################################
imgUrl = "http://www.pediatricly.com/images/turkeySmall.jpg"

# Event Details
eName = 'GSB JPM After-After Party'
eDateD = DT.date(2016, 1, 13)
eDate2D = eDateD # Assumes same start & stop date, can change here
#pst = pytz.timezone('US/Pacific')
eStartT = DT.time(20,0,0,0) #Start time in 24-hr
eStopT = DT.time(21,30,0,0)
location = "TBD - based on your vote"
cutoffD = DT.datetime(2016, 5, 10,17,0)

# Set words used in url & variable checks
yes = 'yes'
maybe ='maybe'
no = 'no'
rsvp = 'rsvp'
###################################################################
### Make the date & times pretty
###################################################################
eStartDT = DT.datetime.combine(eDateD, eStartT)
eStopDT = DT.datetime.combine(eDate2D, eStopT)

eDateStart = eStartDT.strftime("%A, %d %b %Y %I:%M %p")
eDateStop = eStopDT.strftime("%A, %d %b %Y %I:%M %p")
eDate = eDateD.strftime("%A, %d %b %Y")
eDate2 = eDate2D.strftime("%A, %d %b %Y")
eStart = eStartT.strftime("%I:%M %p")
eStop = eStopT.strftime("%I:%M %p")
cutoff = cutoffD.strftime("%A, %d %b %Y at %I:%M %p EST")

###################################################################
# For invitesGen
###################################################################
# Column Names as variables. Can adjust the strings to match the csv
FName = 'FName'
LName = 'LName'
nickName = 'nickName'
sex = 'sex' # Not setup to be used in inviteGen1 yet
email = 'email'
new = 'new'
custom1 = 'custom1'
custom2 = 'custom2'
msgHTML = 'msgHTML' # This becomes the last header when writing templated html
# to csv

# headers is used by dictWriter (not reader) to setup the csv output file
headers = [FName, LName, nickName, sex, email, new, custom1, custom2, msgHTML]

# subject = 'JPM Med-Biz Symposium After-After Party' # Invite email subject line
# (not using this in current version where this is actually set using YAMM in
# GMail)

# Input contact list, commented raw_input in file if you want
contactsCSV = 'contactList.csv'
inviteTemplate = 'msgTemplate.html'
invitesOut = 'invitesOut.csv'

rsvpVars = [FName, LName, email] # This is just getting text labels set above
# These are the variables that get urlencoded into the rsvp URLs using a loop to
# create rsvpDict to pull individual values into the URL
# &rsvp=yes maybe no are concatenated on using strings set above.
rsvpBase = 'http://www.pediatricly.com/cgi-bin/rsvp.py?'

# Extra html added to the invite message only if contactList[person][new] == 'y'
newBonus = "I think I mentioned when last we spoke that I've been organizing semi-formal networking dinner events for cool folks doing medical-business stuff. Would love to have you join for this next event.<br>"
###################################################################
# For the RSVP page:
###################################################################
rsvpCSV = 'rsvpLog1.csv'
rsvphtmlTemplate = 'rsvpTemplate1.html'
rsvpErrTemplate = 'rsvpErrTemp1.html'
rsvpBlastTax = ''
closedHTML = 'rsvpClosed.html'
# How are you defining the votes - careful that the input URL needs to match
# this

# These get added directly after the RSVP according to the response.
bonusYes = "Can't wait to see you there!"
bonusMaybe = "Hope that turns into a yes. Keep us posted."
bonusNo = "Will be sorry to miss you!"

custom = '' # Shows in html after the rsvp+bonus. custom Yes, Maybe, No get
# concatenated to this. So custom is a unviersal response to add to the HTML and
# the others are response-specific.
customClosed = '' # Shows in html only when after cutoff in custom HTML template

# These only end up in the HTML if vote == yes, maybe or no respectively.
# They get templated in rsvp1.py using vote links if specified then concatenated to
# custom.
# Only the final product, customRsvpHTML ends up in rsvp1.py
customYesTemplate = """
<b>Would you like to vote on where we go for dinner?</b><br>
Click the name for the Yelp listing. Click "Vote" to cast your ballot.
<ul>
<li><a href="http://www.yelp.com/biz/marlowe-san-francisco-2" target="_blank">Marlowe</a> | <a href="$link1">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/tropisue%C3%B1o-san-francisco-3" target="_blank">Tropisueno</a> | <a href="$link2">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/t%C3%ADn-vietnamese-cuisine-san-francisco-3" target="_blank">Tin Vietnamese</a> | <a href="$link3">[Vote!]</a></li>
</ul>
"""
customMaybeTemplate = customYesTemplate
customNoTemplate = ''

# These are looped and added to the custom templates above if desired. Can leave
# blank if there's nothing to vote on.
urlBase = 'http://www.pediatricly.com/cgi-bin/invites/vote.py?'
choices = ['Marlowe', 'Tropisueno', 'Tin_Vietnamese']
# choices = []
cgiNameListRSVP = ['email', 'FName', 'LName', 'rsvp']
rsvpSlot = 3 # The index of the above list where rsvp is
###################################################################
# For the vote page:
###################################################################
voteCSV = 'voteLog1.csv'
votehtmlTemplate = 'voteTemplate1.html'
voteErrTemplate = 'rsvpErrTemp1.html' # Room for it but using 1 error template so far
voteBlastTax = ''
voteCustom = 'Mike will let you know once the votes are tallied and the location confirmed.'
# if vote == yes or vote == maybe:
voteBonus = ''

voteSlot = 2

