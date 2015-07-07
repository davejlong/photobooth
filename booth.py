import RPi.GPIO as GPIO
import time
import signal
import sys

red_pin = 7
green_pin = 11
blue_pin = 13

def main():
	print("Running")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(red_pin, GPIO.OUT)
	GPIO.setup(green_pin, GPIO.OUT)
	GPIO.setup(blue_pin, GPIO.OUT)
	while True:
		take_picture()
		off_all()
		time.sleep(5)

def on_all():
	on(red_pin)
	on(green_pin)
	on(blue_pin)

def off_all():
	off(red_pin)
	off(green_pin)
	off(blue_pin)

def on(pin):
	GPIO.output(pin, GPIO.HIGH)

def off(pin):
	GPIO.output(pin, GPIO.LOW)

def take_picture():
	print("Taking a picture")
	on_all()
	time.sleep(1)
	off(red_pin)
	time.sleep(1)
	off(green_pin)
	time.sleep(1)
	off(blue_pin)
	time.sleep(0.5)
	on_all()
	time.sleep(1)

def signal_handler(signal, frame):
	print("Shutting down")
	GPIO.cleanup()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

main()
