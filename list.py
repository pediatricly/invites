import csv

s = """
Sabah Oney <sabahoney@gmail.com>,
Ian Shakil <ishakil@gmail.com>,
Sean Mehra <sean@mehra.fm>,
Shaka Bahadu <bahadu@gmail.com>,
Eric Leroux <leroux6000@gmail.com>,
Michael Winlo <mwinlo@me.com>,
Viren Shetty <virenpshetty@gmail.com>,
Julia Bernstein <jfbernstein@gmail.com>,
Becca Levin <becca.levin@gmail.com>,
Tia Gao <tiagao@gmail.com>,
Ryan Padrez <Ryan.Padrez@ucsf.edu>,
Pallen Chiu <pchiu@alumni.gsb.stanford.edu>,
Akins Van Horne <akins.vanhorne@gmail.com>,
Justin Durack <jdurack@gmail.com>,
Austin Kiessig <akiessig@gmail.com>,
nupur srivastava <nupur.srivastava84@gmail.com>,
Kent Keirsey <keirsey4@gmail.com>,
Sohan Japa <sjapa6@gmail.com>,
Sonia Samagh <SSamagh@healthcarepartners.com>,
Julie Papanek <julie.papanek@gmail.com>,
Gurmeet Sran <gsran@yahoo.com>,
Alexa Bisinger <alexa.d.bisinger@gmail.com>,
Chitra Akileswara <chitra.a@gmail.com>,
Jonathan Avida <avida.jonathan@gmail.com>,
Glenwood Barbee <glenwood.barbee@gmail.com>,
Sarah Milby <milby_sarah@gsb.stanford.edu>,
Fabien Beckers <fabien@arterys.com>,
Christopher Bockman <c.bockman@gmail.com>,
Andrew Lockhart <andrewjameslockhart@gmail.com>,
Chris Klomp <cklomp@gmail.com>,
Naoko Shirota <naoko.shirota@gmail.com>,
Mudit Garg <mudit@analyticsmd.com>,
Shaundra Eichstadt <shaundraeichstadt@gmail.com>,
Tiffany Card <tiffany.card@gmail.com>,
Jossy Tseng <jossy.tseng10@gmail.com>,
Erin Palm <erin.ann.palm@gmail.com>,
Jessica Hou <houjess@gmail.com>,
"""

lines = s.split(',')
#print lines
newlist = []
for line in lines:
    new = line.replace('\n', '')
    new2 = new.replace('<', '')
    new3 = new2.replace('>', '')
    newlist.append(new3)
print newlist
headers = ['FName', 'LName', 'email']

contactDict = {}
contactList = []
for person in newlist:
    values = person.split()
    pdict = dict(zip(headers, values))
    contactList.append(pdict)

'''
CAREFUL - don't run this without a close look!
It will overwrite nicknames etc!
with open('contactList.csv', 'wb') as csvout:
    writer = csv.DictWriter(csvout, headers)
    writer.writeheader()
    for person in contactList:
        writer.writerow(person)
'''
