#!/usr/bin/env python3.6

# Reference https://sites.google.com/site/moosyresearch/projects/samsung_shape#TOC-Grouping-speakers

from __future__ import print_function
import sys
import os.path
import os
import time
import pychromecast
from gtts import gTTS
import requests
from mutagen.mp3 import MP3

# Log entry the notification script is starting
##################################################################################################################
# Set path to Domoticz
URL_DOMOTICZ = 'http://192.168.1.2:8080/'
# Log entry - starting script
req = requests.get(URL_DOMOTICZ + 'json.htm?type=command&param=addlogmessage&message="Starting notify script"')
##################################################################################################################


# Turns the notification into an mp3 file and saves it to the www/media/directory as notification.mp3
##################################################################################################################
# Grap the message being passed
message = sys.argv[1] 
# message = "You wait a certain amount of time after each check, and then read the file when the path exists. The script can be stopped with the KeyboardInterruption exception if the file is never created. You should also check if the path is a file after, to avoid some unwanted exceptions."

# Log entry - notification message
req = requests.get(URL_DOMOTICZ + 'json.htm?type=command&param=addlogmessage&message="Message: ' + message + '"')
# Create and save the message
tts = gTTS(text = message, lang = 'en', slow = False)
# Saves the mp3 to the www/media directory within Domoticz 
# Use path to the location of your www/media directory
tts.save("C:/Program Files (x86)/Domoticz/www/media/notification.mp3")

# Wait for file to be created
while not os.path.exists("C:/Program Files (x86)/Domoticz/www/media/notification.mp3"):
    time.sleep(2)
    print("waiting...")

##################################################################################################################


# Creates a Samsung multiroom speaker group "Alert"
##################################################################################################################

#Define speaker vars
# Main speker IP and MAC addresses
main_ip = "192.168.1.26"
main_mac = "B8:BB:AF:D1:76:AE"
# Sub speaker(s)
sub_ip = "192.168.1.27"
sub_mac = "B8:BB:AF:D1:B6:A2"

#URLS to create a group
# Main speaker
# First CDATA is the group name being created
# spknum value is total number of speakers in the group
# subspkip is IP of sub speaker - not sure what this would be if more than two speakers
# subspkmac is MAC address of sub speaker - again not sure what this would be if more than two speakers
# For more info reference https://github.com/saykalik/SamsungSpeakerController
group_main_url = 'http://' + main_ip + ':55001/UIC?cmd=<pwron>on</pwron><name>SetMultispkGroup</name><p type="cdata" name="name" val="empty"><![CDATA[Alert Group]]></p><p type="dec" name="index" val="1"/><p type="str" name="type" val="main"/><p type="dec" name="spknum" val="2"/><p type="str" name="audiosourcemacaddr" val="' + main_mac + '"/><p type="cdata" name="audiosourcename" val="empty"><![CDATA[R1 Living Room]]></p><p type="str" name="audiosourcetype" val="speaker"/><p type="str" name="subspkip" val="' + sub_ip +'"/><p type="str" name="subspkmacaddr" val="' + sub_mac +'"/>'

# Sub spealer call
# Main thing her CDATA must match that used in main speaker CDATA
group_sub_url = 'http://' + sub_ip + ':55001/UIC?cmd=<pwron>on</pwron><name>SetMultispkGroup</name><p type="cdata" name="name" val="empty"><![CDATA[Alert Group]]></p><p type="dec" name="index" val="1"/><p type="str" name="type" val="sub"/><p type="dec" name="spknum" val="2"/><p type="str" name="mainspkip" val="' + main_ip +'"/><p type="str" name="mainspkmacaddr" val="' + main_mac +'"/>'

#Execute creation of the Samsung group by calling the URLS
req = requests.get(group_main_url)
req = requests.get(group_sub_url)
# Alert speaker group is created and ready to use 
##################################################################################################################



# Play notification message on Samsung speaker group
##################################################################################################################

# URL to mp3 file to be played
url_to_mp3 = URL_DOMOTICZ + 'media/notification.mp3'

# Get the play time of the mp3 file in seconds to know when to ungroup the speakers
audio = MP3("C:/Program Files (x86)/Domoticz/www/media/notification.mp3")
play_time = audio.info.length

print(play_time)

# URL to the main speaker IP address to play message - this will play to all sub speakers in the group
send_url = 'http://' + main_ip + ':55001/UIC?cmd=<pwron>on</pwron><name>SetUrlPlayback</name><p type="cdata" name="url" val="empty"><![CDATA[' + url_to_mp3 + ']]></p><p type="dec" name="buffersize" val="0"/><p type="dec" name="seektime" val="0"/><p type="dec" name="resume" val="1"/>'
req = requests.get(send_url)


# Wait out the play time plus 5 seconds then ungroup speakers

time.sleep(play_time + 5)

# Ungroup speakers 
ungroup_main_url = 'http://' + main_ip + ':55001/UIC?cmd=<name>SetUngroup</name>'
ungroup_sub_url = 'http://' + sub_ip + ':55001/UIC?cmd=<name>SetUngroup</name>'
req = requests.get(ungroup_main_url)
req = requests.get(ungroup_sub_url)
##################################################################################################################

#Script complete - clean up and bug out
os.remove("C:/Program Files (x86)/Domoticz/www/media/notification.mp3")
exit()
