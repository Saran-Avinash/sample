import time
import urllib.request
import RPi.GPIO as GPIO

trig = 2
echo = 4
Thing = "https://api.thingspeak.com/update?api_key=Your_Api_Key"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def read_distance():
    GPIO.output(trig, True)
    time.sleep(1)
    GPIO.output(trig, False)
    pulse_st = time.time()
    while GPIO.input(echo) == 0:
        pulse_st = time.time()
    pulse_end = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    pulse_dur = pulse_end - pulse_st
    distance = pulse_dur * 17150
    distance = round(distance, 2)
    return distance

while True:
    distance = read_distance()
    print(distance)
    url = Thing + '&field1={:.2f}'.format(distance)
    urllib.request.urlopen(url)
    time.sleep(1)
            
            
            
# import requests
# import RPi.GPIO as gp
# gp.setwarnings(False)

# url = "https://api.thingspeak.com/channels/Channel_Id/feeds.json"
# response = requests.get(url, verify=False)

# data = response.json()
# print("Data from the ThingSpeak.com using Read API:")
# feeds = data.get('feeds', [])
# for entry in feeds:
#     field1 = entry.get("field1")
#     print(field1)
            