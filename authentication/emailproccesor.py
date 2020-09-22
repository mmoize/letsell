
from email.mime.text  import MIMEText
import smtplib

from email.mime.multipart import MIMEMultipart

message = MIMEMultipart()
message['from'] = 'Moses Murhi'
message['to'] = "murhi46@gmail.com"
message['subject'] = "this is a text"

message.attach(MIMEText('body'))

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("mosesmvp@gmail.com", "0o9i8uuh")
    smtp.send_message(message)
    print('sent...')


