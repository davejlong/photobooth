#!/usr/bin/env python

import pygame
import os
from time import sleep

class Interface:
    real_path = os.path.dirname(os.path.realpath(__file__))

    ###
    # Initialize and configure a pygame instant
    ###
    def init_pygame(self):
        pygame.init()
        self.display_info = pygame.display.Info()
        size = (self.display_info.current_w, self.display_info.current_h)
        pygame.display.set_caption("Photo Booth")
        pygame.mouse.set_visible(False)
        return pygame.display.set_mode(size, pygame.FULLSCREEN)

    ###
    # Display an image in the pygame instance
    ###
    def show_image(self, image):
        screen = self.init_pygame()
        img = pygame.image.load(self.real_path + "/media/" + image)
        offset_x, offset_y = self.offsets(img.get_size())
        screen.blit(img, (offset_x, offset_y))
        pygame.display.flip()

    ###
    # Provide dynamic offsets to center on screen
    ###
    def offsets(self, dimensions):
        offset_x = (self.display_info.current_w - dimensions[0]) / 2
        offset_y = (self.display_info.current_h - dimensions[1]) / 2
        return (offset_x, offset_y)

def main():
    interface = Interface()
    for image in ["intro", "instructions", "processing", "finished2"]:
        interface.show_image(image + ".png")
        sleep(2)

if __name__ == "__main__":
    main()
