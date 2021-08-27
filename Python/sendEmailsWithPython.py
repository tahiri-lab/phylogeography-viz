
import smtplib
import config


def send_email(subject,msg,reciever):
    try:
        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(config.EMAIL_ADDRESS,config.PASSWORD)
            message = 'Subject: {}\n\n{}'.format(subject,msg)
            smtp.sendmail(config.EMAIL_ADDRESS, reciever, message)
      
        print("Success: Email sent!")
    except:
        print("Email failed to send！")

subject = "HI"
msg = "hjkhlk"

reciever = '80@gmail.com'

send_email(subject,msg,reciever)