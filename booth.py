import RPi.GPIO as GPIO
import time
import signal
import sys

leds = [7, 11, 13]
button_pin = 15

def main():
	print("Running")
	GPIO.setmode(GPIO.BOARD)
	for led in leds:
		GPIO.setup(led, GPIO.OUT)
	GPIO.setup(button_pin, GPIO.IN)

	# TODO: Setup handling to ensure no event queue
	GPIO.add_event_detect(button_pin, GPIO.RISING, callback=take_picture, bouncetime=300)

def on_all():
	for led in leds:
		on(led)

def off_all():
	for led in leds:
		off(led)

def on(pin):
	GPIO.output(pin, GPIO.HIGH)

def off(pin):
	GPIO.output(pin, GPIO.LOW)

def take_picture(channel):
	print("Taking a picture")
	on_all()
	for led in leds:
		time.sleep(1)
		off(led)
	time.sleep(0.5)
	on_all()
	time.sleep(1)
	off_all()

def signal_handler(signal, frame):
	print("Shutting down")
	GPIO.cleanup()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

main()
while True:
	time.sleep(0.5)
