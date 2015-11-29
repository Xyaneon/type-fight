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

        # Health bars
        self.player_health_bkg_rect = pygame.Rect(370, 40, 320, 34)
        self.player_health_bkg_color = pygame.color.Color(0, 255, 0)
        self.player_health_fg_rect = self.player_health_bkg_rect.inflate(-8, -8)
        self.player_health_fg_color = pygame.color.Color(0, 255, 0, 150)
        self.opponent_health_bkg_rect = pygame.Rect(370, 128, 320, 34)
        self.opponent_health_bkg_color = pygame.color.Color(255, 0, 0)
        self.opponent_health_fg_rect = self.opponent_health_bkg_rect.inflate(-8, -8)
        self.opponent_health_fg_color = pygame.color.Color(255, 0, 0, 150)

    def render(self, c_entry, c_output, player_health, opponent_health):
        '''Returns a pygame.Surface with all the rendered HUD elements.
        Requires the command entry and output, and some game info to render.'''
        # Main HUD portion
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))
        self.surface.blit(self.hud_bkg_image, self.hud_bkg_image.get_rect())
        self.surface.blit(c_entry.surface, (315, 775))
        self.surface.blit(c_output.surface, (34, 90))
        # Health bars
        phfr = self.player_health_fg_rect.copy()
        phfr.width = phfr.width * (float(player_health) / 100.0)
        pygame.draw.rect(self.surface, self.player_health_bkg_color, self.player_health_bkg_rect, 2)
        pygame.draw.rect(self.surface, self.player_health_fg_color, phfr)
        if opponent_health > 0:
            ohfr = self.opponent_health_fg_rect.copy()
            ohfr.width = ohfr.width * (float(opponent_health) / 100.0)
            pygame.draw.rect(self.surface, self.opponent_health_bkg_color, self.opponent_health_bkg_rect, 2)
            pygame.draw.rect(self.surface, self.opponent_health_fg_color, ohfr)
        return self.surface
