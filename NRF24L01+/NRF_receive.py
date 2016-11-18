import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys
import time
import paho.mqtt.client as mqtt
import os

def on_connect():
    global connected
    connected = 1
    print("%d"%connected)

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

client = mqtt.Client()
client.username_pw_set(username="pi", password="pipi")
client.connect("192.168.1.139",1883)
client.on_connect = on_connect

while(1):
    while not radio.available(0):
        time.sleep(1 / 100)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

    print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
           string += chr(n)
    print("Out received message decodes to: {}".format(string))
    print(chr(n))
    Result = chr(n)
    client.publish("officeTemp",Result)
