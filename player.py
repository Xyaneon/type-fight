#!/bin/python

import math, os, pygame

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
        self.updown_juice = 0
        self.health_percent = 100

    def get_rects(self):
        '''Returns a pair of pygame.Rect objects with size and position info.
        These Rects represent the left and right arms, respectively.'''
        return (self.left_arm_rect, self.right_arm_rect)

    def render(self):
        '''Returns a pygame.Surface with the rendered player parts.'''
        self.updown_juice += (2.0 * math.pi) / 60.0
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))

        # Left arm
        self.left_arm_rect = self.left_arm_image.get_rect()
        la_center_rect = self.rect.copy()
        la_center_rect.centerx = self.surface.get_rect().centerx - self.left_arm_rect.get_width() / 2
        la_center_rect.centery = self.surface.get_rect().centery + 15 * math.sin(self.updown_juice)
        self.surface.blit(self.left_arm_image, la_center_rect)

        # Right arm
        self.right_arm_rect = self.right_arm_image.get_rect()
        ra_center_rect = self.rect.copy()
        ra_center_rect.centerx = self.surface.get_rect().centerx + self.right_arm_rect.get_width() / 2
        ra_center_rect.centery = self.surface.get_rect().centery + 15 * math.sin(self.updown_juice)
        self.surface.blit(self.right_arm_image, ra_center_rect)

        return self.surface
