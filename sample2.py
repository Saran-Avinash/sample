#smart parking
#sudo apt update
#sudo apt upgrade
#sudo apt install git
#iyau pohs vhke wppc


import RPi.GPIO as GPIO
import time
import requests
import smtplib
from email.mime.text import MIMEText

GPIO.setmode(GPIO.BCM)

TRIG = 17
ECHO = 27
LED_RED = 23
LED_GREEN = 22

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

api = "Api_key"
URL = "https://api.thingspeak.com/update"

smtp_server = "smtp.gmail.com"
port = 587
email = "Your_Email"
password = "Password(Key)"
receiver = "receiver_Email"
sent = False

def send():
    global sent
    if not sent:
        try:
            subject = "for checking"
            body = "Parking slot is occupied"
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = email
            msg["To"] = receiver

            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, receiver, msg.as_string())
            server.quit()

            print("Email sent successfully")
            sent = True
        except Exception as e:
            print(e)

def measure():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

def sendToThingSpeak(distance):
    payload = {"api_key": api, "field1": distance}
    try:
        response = requests.post(URL, data=payload)
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(response.status_code)
    except Exception as e:
        print(e)

try:
    while True:
        distance = measure()
        print(distance)

        if distance < 100:
            GPIO.output(LED_RED, GPIO.HIGH)
            GPIO.output(LED_GREEN, GPIO.LOW)
            send()
            print("Parking space occupied")
        else:
            GPIO.output(LED_GREEN, GPIO.HIGH)
            GPIO.output(LED_RED, GPIO.LOW)
            print("Parking space available")

        sendToThingSpeak(distance)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
            