
import smtplib
#import config


def send_email(subject,msg,reciever):
    EMAIL_ADDRESS = '******@gmail.com'
    PASSWORD = '******'

    try:
        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS,PASSWORD)
            message = 'Subject: {}\n\n{}'.format(subject,msg)
            smtp.sendmail(EMAIL_ADDRESS, reciever, message)
      
        print("Success: Email sent!")
    except:
        print("Email failed to send！")

subject = "HI"
msg = "hjkhlk"

reciever = '806981384wl@gmail.com'

send_email(subject,msg,reciever)