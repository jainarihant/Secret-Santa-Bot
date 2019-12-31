import random
import csv
import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

thanksList = []
matchList = []

def setUpEmailContent(santa, message):
		mail_content = '''Hello {0},
Your match recieved your gift and this is their thank you message for you:
  "{1}"
Merry Christmas!! 
Thank You
'''.format(santa, message)
		return mail_content

#send email to gitee with match name
# @param santa string
# @param santaEmail string
# @param match string
def sendEmail(santa, santaEmail, message):
	sender_address = config.email_address
	sender_pass = config.password
	receiver_address = santaEmail
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Thank you Santa!'   #The subject line
	#The body and the attachments for the mail
	mailContent = setUpEmailContent(santa, message)
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

with open('thanks.csv', mode='r') as csvFile:
	namesList=csv.DictReader(csvFile)
	for row in namesList:
		thanksList.append(row)

with open('matchedNames.csv', mode='r') as csvFile:
	matchList=csv.DictReader(csvFile)
	for row in matchList:
		for matchRow in thanksList:
			if matchRow['matchName'] == row['Giftee']:
				#print(str(matchRow['message']))
		 		sendEmail(row['SantaName'], row['SantaEmail'], str(matchRow['message']))