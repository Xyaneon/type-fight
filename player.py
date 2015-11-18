#!/bin/python

import math, os, pygame

player_arm_spacing = 128 / 2

class Player:
    '''Class representing the player's character onscreen'.'''
    def __init__(self, screen):
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        self.img_left_arm = pygame.image.load(os.path.join('graphics',
                                         'player_left_arm.png')).convert_alpha()
        self.img_right_arm = pygame.image.load(os.path.join('graphics',
                                          'player_right_arm.png')).convert_alpha()
        self.img_left_block = pygame.image.load(os.path.join('graphics',
                                         'player_block_left.png')).convert_alpha()
        self.img_right_block = pygame.image.load(os.path.join('graphics',
                                          'player_block_right.png')).convert_alpha()
        self.left_arm_image = self.img_left_arm
        self.right_arm_image = self.img_right_arm
        self.left_arm_rect = self.left_arm_image.get_rect()
        self.right_arm_rect = self.right_arm_image.get_rect()
        self.rect = self.surface.get_rect()
        self.updown_juice = 0
        self.health_percent = 100
        self.left_arm_state = 'idle'
        self.right_arm_state = 'idle'

    def get_rect(self):
        '''Returns a pygame.Rect representing the rendered surface Rect.'''
        return self.rect

    def take_damage(self, damage, direction):
        '''Deals damage to this Player.'''
        if direction == 'left':
            if self.left_arm_state == 'blocking':
                self.left_arm_state = 'idle'
                self.left_arm_image = self.img_left_arm
                return
            else:
                self.health_percent -= damage
        if direction == 'right':
            if self.right_arm_state == 'blocking':
                self.right_arm_state = 'idle'
                self.right_arm_image = self.img_right_arm
                return
            else:
                self.health_percent -= damage
        if direction == 'both':
            if not self.left_arm_state == 'blocking':
                self.health_percent -= int(math.floor(damage / 2.0))
            if not self.right_arm_state == 'blocking':
                self.health_percent -= int(math.floor(damage / 2.0))
            self.left_arm_state = 'idle'
            self.left_arm_image = self.img_left_arm
            self.right_arm_state = 'idle'
            self.right_arm_image = self.img_right_arm
        self.health_percent -= damage
        if self.health_percent <= 0:
            self.health_percent = 0
            self.left_arm_state = 'defeated'
            self.right_arm_state = 'defeated'
            self.updown_juice = 0

    def block(self, direction=''):
        '''Block in the specified direction.'''
        if direction == '' or direction == 'both' or direction == 'center':
            self.left_arm_state = 'blocking'
            self.left_arm_image = self.img_left_block
            self.right_arm_state = 'blocking'
            self.right_arm_image = self.img_right_block
        elif direction == 'left':
            self.left_arm_state = 'blocking'
            self.left_arm_image = self.img_left_block
        elif direction == 'right':
            self.right_arm_state = 'blocking'
            self.right_arm_image = self.img_right_block

    def render(self):
        '''Returns a pygame.Surface with the rendered player parts.'''
        self.updown_juice += (2.0 * math.pi) / 45.0
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
