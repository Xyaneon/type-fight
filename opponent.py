#!/bin/python

import os, pygame

class Opponent:
    '''Class representing the opponent the player can see.'''
    def __init__(self):
        self.surface = None
        self.opponent_image = pygame.image.load(os.path.join('graphics',
                                  'opponent_neutral.png')).convert_alpha()
        self.rect = self.opponent_image.get_rect()

    def get_rect(self):
        '''Returns a pygame.rect.Rect with size and position info.'''
        return self.rect

    def render(self):
        '''Returns a pygame.Surface with the rendered opponent.'''
        # TODO: More advanced manipulation for movement and stuff
        self.rect = self.opponent_image.get_rect()
        self.surface = pygame.Surface((self.opponent_image.get_width(),
                                       self.opponent_image.get_height()),
                                      pygame.SRCALPHA).copy()
        self.surface.blit(self.opponent_image, self.opponent_image.get_rect())
        return self.surface