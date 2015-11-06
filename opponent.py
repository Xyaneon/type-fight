#!/bin/python

import math, os, pygame

class Opponent:
    '''Class representing the opponent the player can see.'''
    def __init__(self, screen):
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        self.opponent_image = pygame.image.load(os.path.join('graphics',
                                  'opponent_neutral.png')).convert_alpha()
        self.rect = self.opponent_image.get_rect()
        self.updown_juice = 0
        self.health_percent = 100
        self.attack_delay_frames = 0
        self.state = 'idle'
        self.weak_spots = []

    def get_rect(self):
        '''Returns a pygame.rect.Rect with size and position info.'''
        return self.rect

    def render(self):
        '''Returns a pygame.Surface with the rendered opponent.'''
        self.rect = self.opponent_image.get_rect()
        self.updown_juice += (2.0 * math.pi) / 60.0
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))
        center_rect = self.rect.copy()
        center_rect.centerx = self.surface.get_rect().centerx
        center_rect.centery = self.surface.get_rect().centery + 10 * math.sin(self.updown_juice)
        self.surface.blit(self.opponent_image, center_rect)
        return self.surface
