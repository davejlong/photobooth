#!/usr/bin/env python

import pygame
import os
from time import sleep

_real_path = os.path.dirname(os.path.realpath(__file__))

display_info = None

def init_pygame():
        pygame.init()
        global display_info
        display_info = pygame.display.Info()
        size = (display_info.current_w, display_info.current_h)
        pygame.display.set_caption("Photo Booth")
        pygame.mouse.set_visible(False)
        return pygame.display.set_mode(size, pygame.FULLSCREEN)

###
# Display an image in the pygame instance
###
def show_image(image):
        img = pygame.image.load(_real_path + "/media/" + image)
        offset_x, offset_y = offsets(img.get_size())
        screen.blit(img, (offset_x, offset_y))
        pygame.display.flip()

###
# Provide dynamic offsets to center on screen
###
def offsets(dimensions):
        offset_x = (display_info.current_w - dimensions[0]) / 2
        offset_y = (display_info.current_h - dimensions[1]) / 2
        return (offset_x, offset_y)

screen = init_pygame()

def _main():
    interface = Interface()
    for image in ["intro", "instructions", "processing", "finished2"]:
        interface.show_image(image + ".png")
        sleep(2)

if __name__ == "__main__":
    _main()
