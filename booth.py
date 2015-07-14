#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import picamera

import interface

leds = (8, 10, 9, 11)
picture_button = 24
quit_button = 23
shutdown_button = 25
reboot_button = 22

_app_root = os.path.dirname(os.path.realpath(__file__))
_pics_root = _app_root + "/pics"

def main():
        print "GPIO RPI Revision: ", GPIO.RPI_REVISION
        print "GPIO Version: ", GPIO.VERSION
        
	print "Initializing"
        if not os.path.exists(_pics_root):
                os.makedirs(_pics_root)
	GPIO.setmode(GPIO.BCM)
	for led in leds:
		GPIO.setup(led, GPIO.OUT)
                GPIO.output(led, False)
        for button in (picture_button, quit_button, shutdown_button, reboot_button):
                GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# TODO: Setup handling to ensure no event queue
	# GPIO.add_event_detect(picture_button, GPIO.RISING, callback=take_picture, bouncetime=300)

        GPIO.add_event_detect(quit_button, GPIO.RISING, callback=quit_handler, bouncetime=300)
        GPIO.add_event_detect(shutdown_button, GPIO.RISING, callback=shutdown_handler, bouncetime=300)
        GPIO.add_event_detect(reboot_button, GPIO.RISING, callback=reboot_handler, bouncetime=300)

        reset()

def reset():
        interface.init_pygame()
        interface.show_image("intro.png")

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

def take_picture():
	print "Taking a picture"
	on_all()
        interface.show_image("instructions.png")
	for led in leds:
		time.sleep(1)
		off(led)
	time.sleep(0.5)
	on_all()
	# time.sleep(1)
        # Take the picture
        snap()
	off_all()
        time.sleep(5)
        reset()

def snap():
        camera = picamera.PiCamera()
        resolution = (interface.display_info.current_w, interface.display_info.current_h)
        resolution = (1920, 1080)
        camera.resolution = resolution
        camera.start_preview()
        time.sleep(1)
        now = time.strftime("%Y-%m-%d-%H:%M:%S")
        try:
                GPIO.output(leds[0], GPIO.LOW)
		for i, filename in enumerate(camera.capture_continuous(_pics_root + "/" + now + "-{counter}.jpg")):
                        if i == (len(leds)-1):
                                break
                        time.sleep(2)
                        GPIO.output(leds[i+1], GPIO.LOW)
        finally:
                interface.show_image("finished2.png")
                camera.stop_preview()
                camera.close()

def quit():
        print "Quitting Photobooth"
        on(leds[0])
        time.sleep(1)
        GPIO.cleanup()
        sys.exit(0)

def quit_handler(channel):
        quit()

def shutdown_handler(channel):
        print "Shutting down..."
        on_all()
        time.sleep(3)
        os.system("shutdown -h now")

def reboot_handler(channel):
        print "Rebooting..."
        on_all()
        time.sleep(3)
        os.system("reboot")
        

def signal_handler(signal, frame):
        quit()
signal.signal(signal.SIGINT, signal_handler)

main()
while True:
        GPIO.wait_for_edge(picture_button, GPIO.RISING)
	time.sleep(0.2)
        take_picture()
