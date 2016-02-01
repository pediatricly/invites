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
cutoff = cutoffD.strftime("%A, %d %b %Y at %I:%M %p EST")

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
yes = 'yes'
maybe ='maybe'
no = 'no'

custom = '' # Shows in html after the rsvp+bonus only for no votes
customClosed = '' # Shows in html only when after cutoff in custom HTML template

###################################################################
### Use the string.Template to store custom HTML as a big string
###################################################################
# This only ends up in the HTML if vote == yes or vote == maybe:
# Only the final product, customRsvpHTML ends up in rsvp1.py
# For no votes, plain custom (above) is used
customRsvpTemplate = """
<b>Would you like to vote on where we go for dinner?</b><br>
Click the name for the Yelp listing. Click "Vote" to cast your ballot.
<ul>
<li><a href="http://www.yelp.com/biz/marlowe-san-francisco-2" target="_blank">Marlowe</a> | <a href="$link1">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/tropisue%C3%B1o-san-francisco-3" target="_blank">Tropisueno</a> | <a href="$link2">[Vote!]</a></li>
    <li><a href="http://www.yelp.com/biz/t%C3%ADn-vietnamese-cuisine-san-francisco-3" target="_blank">Tin Vietnamese</a> | <a href="$link3">[Vote!]</a></li>
</ul>
"""

urlBase = 'http://www.pediatricly.com/cgi-bin/invites/vote1.py?'
choices = ['Marlowe', 'Tropisueno', 'Tin_Vietnamese']
# choices = []

bonusYes = "Can't wait to see you there!"
bonusMaybe = "Hope that turns into a yes. Keep us posted."
bonusNo = "Will be sorry to miss you!"

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



