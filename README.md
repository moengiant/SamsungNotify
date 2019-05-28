# SamsungNotify

Reason to use this script:

This is a notification script that uses the gTTS module to speak Domoticz notifications to a Samsung Multiroom Speaker Group.

As we play a lot of music in the house as well use the Chromecast and Google Home/mini devices for other things I created this script to avoid disruption of Chromecast devices. 

Hardeware and software requirements:

1) Samsung wireless speakers - I'm using two R1 speakers
2) Domoticz sever running on a local network
3) Python and a couple of python modules installed  

Key features: 

1) Script creates a multiroom group on the fly and ungroups speakers after message is played
2) Waits for the notification.mp3 file to be created and then calcultes play time length and waits for the file to be played before ungrouping speakers
3) Cleans up files after notification is played by deleting the notification.mp3 file

How to use:

1) Place the Samsung_notify.pyw script in the scripts/python directory in Domoticz. 
2) Add a notification to a device in Domoticz
3) In Domoticz settings -> notifications change the URL/Action field under the Custom HTTP/Actions settings to the following: script://scripts\python\Samsung_notify.pyw #MESSAGE (this path works on Windows 10 - paths for other operating systems may be different)

The script is well documented in the script's comments so take a look at the comments if your not sure about sttings or what the script is doing. 

Enjoy
