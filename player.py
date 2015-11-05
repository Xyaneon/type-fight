#!/bin/python

import math, os, pygame

player_arm_spacing = 128 / 2

class Player:
    '''Class representing the player's character onscreen'.'''
    def __init__(self, screen):
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        self.left_arm_image = pygame.image.load(os.path.join('graphics',
                                  'player_left_arm.png')).convert_alpha()
        self.right_arm_image = pygame.image.load(os.path.join('graphics',
                                   'player_right_arm.png')).convert_alpha()
        self.left_arm_rect = self.left_arm_image.get_rect()
        self.right_arm_rect = self.right_arm_image.get_rect()
        self.rect = self.surface.get_rect()
        self.updown_juice = 0
        self.health_percent = 100

    def get_rect(self):
        '''Returns a pygame.Rect representing the rendered surface Rect.'''
        return self.rect

    def render(self):
        '''Returns a pygame.Surface with the rendered player parts.'''
        self.updown_juice += (2.0 * math.pi) / 60.0
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))

        # Left arm
        la_center_rect = self.left_arm_image.get_rect().copy()
        la_center_rect.right = self.rect.centerx - player_arm_spacing
        la_center_rect.top = self.rect.centery + 15 * math.sin(self.updown_juice)
        self.surface.blit(self.left_arm_image, la_center_rect)

        # Right arm
        ra_center_rect = self.right_arm_image.get_rect().copy()
        ra_center_rect.left = self.rect.centerx + player_arm_spacing
        ra_center_rect.top = self.rect.centery + 15 * math.sin(self.updown_juice)
        self.surface.blit(self.right_arm_image, ra_center_rect)

        return self.surface