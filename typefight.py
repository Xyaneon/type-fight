#!/bin/python

import os, pygame, pygame.mixer, sys
from pygame.locals import *
from commandentry import CommandEntry
from commandoutput import CommandOutput
from hud import Hud
from opponent import Opponent
from player import Player

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
hud = Hud(screen)
player = Player(screen)
fight_bkg = pygame.image.load(os.path.join('graphics', 'fight_bkg.png')).convert()
win_fg = pygame.image.load(os.path.join('graphics', 'win_fg.png')).convert_alpha()
lose_fg = pygame.image.load(os.path.join('graphics', 'lose_fg.png')).convert_alpha()

pygame.key.set_repeat(500, 50)

# Mouse setup
mouse_list = [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]
mouse_button_list = [MOUSEBUTTONDOWN, MOUSEBUTTONUP]
pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

# Pygame mixer setup for sounds
try:
    pygame.mixer.init()
    mus_fight = pygame.mixer.music.load(os.path.join('music', 'Harmful or Fatal.ogg'))
    pygame.mixer.music.play()
except Exception as e:
    print e

# Main objects setup
c_entry = CommandEntry()
c_output = CommandOutput()

def run_fight(opponent=Opponent(screen)):
    '''Main loop code for each fight. Takes an Opponent to use.'''
    c_output.add_line('Fight initiated')
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
                c_entry.handle_keydown_event(event,
                                             player,
                                             opponent,
                                             c_output)

        # State updating
        opponent.update_state(player, c_output)

        # Draw graphics
        c_entry.render()
        c_output.render()
        game_surface.blit(fight_bkg, game_surface.get_rect())
        hud_surface = hud.render(c_entry,
                                 c_output,
                                 player.health_percent,
                                 opponent.health_percent)
        game_surface.blit(opponent.render(screen), opponent.get_rect())

        player.render(screen)
        game_surface.blit(player.left_arm_image, player.la_center_rect)
        game_surface.blit(player.right_arm_image, player.ra_center_rect)

        screen.blit(game_surface, game_surface.get_rect())
        screen.blit(hud_surface, hud_surface.get_rect())
        if opponent.state == 'defeated':
            screen.blit(win_fg, screen.get_rect())
        elif player.health_percent <= 0:
            screen.blit(lose_fg, screen.get_rect())
        pygame.display.flip()

        # Proceed to next frame. We are aiming to run at 60 FPS
        fps_clock.tick(60)

#*****************
# Main game code *
#*****************
run_fight(Opponent(screen))
