#!/bin/python

import pygame, pygame.mixer
from pygame.locals import *

pygame.init()

fps_clock = pygame.time.Clock()

# Game window setup
size = width, height = pygame.display.Info().current_w, \
                       pygame.display.Info().current_h
pygame.display.set_caption("Type Fight!")
flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
screen = pygame.display.set_mode((0, 0), flags)
screen.set_alpha(None)
game_surface = pygame.Surface((screen.get_width(), screen.get_height()))
hud_surface = pygame.Surface((screen.get_width(), screen.get_height()))

# TODO: Add loading code for custom font(s) here

pygame.key.set_repeat(500, 50)

# Mouse setup
mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

# Pygame mixer setup for sounds
pygame.mixer.init()

#*****************
# Main loop code *
#*****************
while 1:
    # TODO: Main game loop goes here
    for event in pygame.event.get():
    if event.type is QUIT:
        pygame.quit()
        sys.exit()
    elif event.type in mouse_list:
        mouse_x, mouse_y = event.pos
        mouse_event = event
        if event.type in mouse_button_list:
            mouse_button = event.button
            if event.type is MOUSEBUTTONDOWN:
                # TODO: Mouse button down handling code
            else:
                # TODO: Assume mouse button up
        else:
            # TODO: Handle mouse movement event
    elif event.type is KEYDOWN:
        # TODO: Handle key press event
    fps_clock.tick(60)
