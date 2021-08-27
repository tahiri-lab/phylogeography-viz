import smtplib
from email.message import EmailMessage
#import config


def send_email(subject,msg,reciever):
    EMAIL_ADDRESS = 'testpythonsend08@gmail.com'
    PASSWORD = 'woshixiangzai888'

    msg = EmailMessage()
    msg['Subject'] = 'Subject of the Email' # Subject of Email
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = '806981384wl@gmail.com' # Reciver of the Mail
    msg.set_content('Mail Body') # Email body or Content

    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
           
        smtp.login(EMAIL_ADDRESS,PASSWORD)
        smtp.send_message(msg)
      
    print("Success: Email sent!")
    

subject = "HI"
msg = "hjkhlk"

reciever = '806981384wl@gmail.com'

send_email(subject,msg,reciever)





'''
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

textfile = "textfile"
# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

me = 'testpythonsend08@gmail.com'
you = '806981384wl@gmail.com@gmail.com'
msg['Subject'] = f'The contents of {textfile}'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
'''