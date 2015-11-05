#!/bin/python

import os, pygame, pygame.mixer, sys
from pygame.locals import *
from commandentry import CommandEntry

pygame.init()

fps_clock = pygame.time.Clock()

# Game window setup
window_size = (1080, 911)
size = width, height = pygame.display.Info().current_w, \
                       pygame.display.Info().current_h
pygame.display.set_caption("Type Fight!")
# Set flags to FULLSCREEN | DOUBLEBUF | HWSURFACE if we add fullscreen support later
flags = 0
screen = pygame.display.set_mode(window_size, flags)
screen.set_alpha(None)
game_surface = pygame.Surface((screen.get_width(), screen.get_height()))
hud_surface = pygame.Surface((screen.get_width(), screen.get_height()))

hud_bkg_image = pygame.image.load(os.path.join('graphics', 'hud_bkg.png')).convert_alpha()

pygame.key.set_repeat(500, 50)

# Mouse setup
mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

# Pygame mixer setup for sounds
pygame.mixer.init()

# Main objects setup
c_entry = CommandEntry()

#*****************
# Main loop code *
#*****************
while 1:
    # Event handling
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
                    pass
                else:
                    # TODO: Assume mouse button up
                    pass
            else:
                # TODO: Handle mouse movement event
                pass
        elif event.type is KEYDOWN:
            c_entry.handle_keydown_event(event)

    # Draw graphics
    c_entry.render()
    game_surface.fill(pygame.color.Color(0, 0, 0))
    hud_surface.fill(pygame.color.Color(0, 0, 0))
    hud_surface.blit(hud_bkg_image, hud_bkg_image.get_rect())
    hud_surface.blit(c_entry.surface, (345, 775))
    screen.blit(game_surface, game_surface.get_rect())
    screen.blit(hud_surface, hud_surface.get_rect())
    pygame.display.flip()

    # Proceed to next frame. We are aiming to run at 60 FPS
    fps_clock.tick(60)
