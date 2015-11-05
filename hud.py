#!/bin/python

import os, pygame

class Hud:
    '''Class for the HUD display.'''
    def __init__(self, screen):
        '''Initializes this Hud instance. Requires a Surface for the screen.'''
        self.rect = None
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        self.hud_bkg_image = pygame.image.load(os.path.join('graphics',
                                 'hud_bkg.png')).convert_alpha()

    def render(self, c_entry):
        '''Returns a pygame.Surface with all the rendered HUD elements.
        Requires a CommandEntry object reference to have render on top.'''
        self.surface.fill(pygame.color.Color(0, 0, 0))
        self.surface.blit(self.hud_bkg_image, self.hud_bkg_image.get_rect())
        self.surface.blit(c_entry.surface, (345, 775))
        return self.surface
