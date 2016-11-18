#!/usr/bin/env python

import paho.mqtt.client as mqtt
import Image, ImageDraw, ImageFont
from os import chdir,path
import os
import sys
import time
import PIL
from papirus import Papirus
from papirus import PapirusText
from papirus import PapirusImage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from PIL._util import isStringType
import RPi.GPIO as GPIO
import argparse
import wx
from time import sleep
import datetime
love=like=satisfy=NotSatisfy=0
WHITE = 1
BLACK = 0
# Set the font size for the display
textSize = 30

text=PapirusText()
papirus = Papirus()
SIZE=27
file=open("log.txt","r")
love=int(file.readline())
like=int(file.readline())
satisfy=int(file.readline())
NotSatisfy=int(file.readline())
file.close()
last_min=0       
last_hr=0
counter=0

def Display(result1,result2,result3,result4):
        global counter
        FOREGROUND = (0,0,0)#text colour = WHITE
        TEXT1=str(result1)
        TEXT2=str(result2)
        TEXT3=str(result3)
        TEXT4=str(result4)
        font_path = '/usr/share/fonts/truetype/freefont/FreeMono.ttf'
        font = ImageFont.truetype(font_path,textSize,encoding='unic')
        text1=TEXT1.decode('utf-8')
        text2=TEXT2.decode('utf-8')
        text3=TEXT3.decode('utf-8')
        text4=TEXT4.decode('utf-8')
        (width,height) = font.getsize(text1)
        (width,height) = font.getsize(text2)
        (width,height) = font.getsize(text3)
        (width,height) = font.getsize(text4)

        x = Image.open('/home/pi/emojiBackground.bmp')
        bg=Image.new('RGB',(264,176),"#FFFFFF")
        W,H = bg.size
        bg.paste(x,(0,0))
        draw = ImageDraw.Draw(bg)
        draw.text((50,5),text1,font=font,fill=FOREGROUND)
        draw.text((50,47),text2,font=font,fill=FOREGROUND)
        draw.text((50,88),text3,font=font,fill=FOREGROUND)
        draw.text((50,132),text4,font=font,fill=FOREGROUND)
        bg.save('/home/pi/image.bmp')
        image=Image.open('/home/pi/image.bmp')
        papirus.display(image)
        if(counter==7):
                papirus.update()
                counter=0
        else:
                counter+=1
                papirus.partial_update()        

# Callback from when client receives a CONNACK response from the server

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

# Subscribing in on_connect means that if we lose connection 
# and reconnect then subscriptions will be renewed

	client.subscribe("officeTemp")

# Callback for when a PUBLISH message is received from the server


def on_message(client, userdata, msg):
	print("got message on topic %s: %s" % (msg.topic, msg.payload))
	displayTemp = msg.payload
	global love ,like,satisfy,NotSatisfy,last_min,last_hr
	if displayTemp=="1":
                love+=1
                image = Image.open('/home/pi/heartEye.bmp')
                papirus.display(image)

        elif displayTemp=="2":
                like+=1
                image = Image.open('/home/pi/like_1_.bmp')
                papirus.display(image)

        elif displayTemp=="3":
                satisfy+=1
                image = Image.open('/home/pi/Smile.bmp')

        elif displayTemp=="4":
                NotSatisfy+=1
                image = Image.open('/home/pi/Sad.bmp')
                papirus.display(image)
                
        papirus.partial_update()
        file=open("log.txt","w")
        file.write(str(love)+"\n"+str(like)+"\n"+str(satisfy)+"\n"+str(NotSatisfy))
        file.close()
        now = datetime.datetime.now()
        if((now.minute-last_min>=10)or(now.minute!=last_min and last_hr!=now.hour)):
                last_min=now.minute
                last_hr=now.hour
                file=open("log"+str(now.hour)+":"+str(now.minute)+".txt","w")
                file.write(str(love)+"\n"+str(like)+"\n"+str(satisfy)+"\n"+str(NotSatisfy))
                file.close()
                
        
	Display(love,like,satisfy,NotSatisfy)
                
# Set up the connection to the MQTT broker

client = mqtt.Client() 
client.username_pw_set(username="pi", password="pipi") 
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.128", 1883, 10000)


# Blocking call that processes network traffic, dispatches callbacks
# and handles reconnecting
# Other loop*() fucntions are available that give a threaded interface
# and a manual interface

try:
	client.loop_forever()

# deal with ^C

except KeyboardInterrupt:
	print("interrupted!")

