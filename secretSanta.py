import random
import csv
import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


nameDirectory = dict({})
names = []

with open('names.csv', mode='r') as csvFile:
	namesList=csv.DictReader(csvFile)
	for row in namesList:
		names.append(row["name"])
		nameDirectory[row["name"]] = row["email"] 

nameMapping = []

# function for random matching
def assignRandomMatch(person, matchPoolArray):
	foolProofRandomMatch = random.choice(matchPoolArray)
	while(foolProofRandomMatch == person):
		foolProofRandomMatch = random.choice(matchPoolArray)
	return foolProofRandomMatch

def setUpEmailContent(santa, match):
		mail_content = '''Hello {0},
Secret Santa Bot has randomly picked {1} as your giftee. Remember that no gift is too small to give; nor too simple to receive. It's the thought of gifting that matters.
Merry Christmas!! 
Thank You
'''.format(santa, match)
		return mail_content

#send email to gitee with match name
# @param santa string
# @param santaEmail string
# @param match string
def sendEmail(santa, santaEmail, match):
	sender_address = config.email_address
	sender_pass = config.password
	receiver_address = santaEmail
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Secret Santa Gift Exchange Mactching'   #The subject line
	#The body and the attachments for the mail
	mailContent = setUpEmailContent(santa, match)
	message.attach(MIMEText(mailContent, 'plain'))
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	try:
		session.sendmail(sender_address, receiver_address, text)
		print('Mail Sent to: '+ santa)
	except:
		print('Could not send mail to: '+ santa)
	finally:
		session.quit()
	

for name in nameDirectory:
	randomMatch = assignRandomMatch(name, names)
	temp= {}
	temp['SantaName'] = name
	temp['Giftee'] = randomMatch
	temp['SantaEmail'] = nameDirectory.get(name)
	nameMapping.append(temp)
	names.remove(randomMatch)
	#sendEmail(name, nameDirectory.get(name), randomMatch)
print('nameMapping', nameMapping)
print(nameDirectory)
with open('matchedNames.csv', mode='wb',) as writeCsvFile:
	fieldnames = ['SantaName', 'Giftee', 'SantaEmail']
	writer = csv.DictWriter(writeCsvFile, fieldnames=fieldnames)
	writer.writeheader()
	for name in nameMapping:
		writer.writerow({ 'Giftee': name['Giftee'], 'SantaEmail': name['SantaEmail'], 'SantaName': name['SantaName']})

