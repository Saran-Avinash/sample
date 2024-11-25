#pi cam
from subprocess import call
import time
import os
import glob
import smtplib
import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import subprocess

gmail_user = "Your_Email"
gmail_pwd = "Your_Email_Password"
FROM = "from_mail"
TO = ["to_mail"]
i = 1

while i:
    subprocess.Popen("raspistill -o cam4.jpg", shell=True)
    time.sleep(5)
    msg = MIMEMultipart()
    time.sleep(1)
    msg['Subject'] = "testing msg sent from python"
    time.sleep(5)
    fp = open("cam4.jpg", "rb")
    time.sleep(1)
    img = MIMEImage(fp.read())
    fp.close()
    time.sleep(1)
    msg.attach(img)
    time.sleep(1)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        print("smtp gmail")
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        print("sending mail from python")
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print("successfully sent the mail")
    except:
        print("failed to send mail")
            