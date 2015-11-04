#!/usr/bin/python

# dryer.py by ThreeSixes (https://github.com/ThreeSixes/)
# Simple python script that sends notifications via GMail when the dryer is done.
# The RPI GPIO pins 3v3 and GPIO 18 should be connected to the normally open
# contacts on a relay with its coil wired in paralell with the dryer's buzzer. 
# This was designed for a Raspberry PI and uses Supervisor to keep the script running.

# Imports
import time
import datetime
import smtplib
import RPi.GPIO as GPIO

# Monitor settings
loopDelay = 0.1 # How long in seconds should we wait until checking the relay again?
triggerDelay = 300 # How long in seconds until it's possible to send another notification.

# E-Mail settings
gmailUser = "someGmailUser"
gmailPass = "someGmailPassword"
srcEmail = gmailUser + "@gmail.com"
dstEmailList = [
    "someone@somewhere.com"
    ]
msg = "\r\n".join([
    "From: " + srcEmail,
    "To: " + ", ".join(dstEmailList),
    "Subject: Dryer",
    "",
    "Laundry is done."
    ])

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Send email
def notify():
    print(str(datetime.datetime.utcnow()) + " - Notifying...")
    gmailSmtp = smtplib.SMTP('smtp.gmail.com:587')
    gmailSmtp.ehlo()
    gmailSmtp.starttls()
    gmailSmtp.login(gmailUser, gmailPass)
    gmailSmtp.sendmail(srcEmail, dstEmailList, msg)
    gmailSmtp.quit()

# Monitor
def monitor():
    print(str(datetime.datetime.utcnow()) + " - Monitoring dryer...")
    # Infinite loop of checking.
    while True:
        
        # Check the GPIO pin.
        pinState = GPIO.input(18)
        
        # If we have contact...
        if pinState == True:
            print(str(datetime.datetime.utcnow()) + " - Buzz.")
            
            # Send the notifications.
            notify()
            
            print(str(datetime.datetime.utcnow()) + " - Sleeping " + str(triggerDelay) + " sec.")
            time.sleep(triggerDelay)
        else:
            time.sleep(loopDelay)

print(str(datetime.datetime.utcnow()) + " - Dryer monitor starting...")

# Start watching.
monitor()
