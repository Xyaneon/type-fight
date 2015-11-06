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
        self.state_frames_remaining = 120
        self.weak_spots = []

    def get_rect(self):
        '''Returns a pygame.rect.Rect with size and position info.'''
        return self.rect

    def take_damage(self, damage):
        '''Deals damage to this Opponent.'''
        self.health_percent -= damage
        self.state_transition('damaged', 0.5)
        if self.health_percent <= 0:
            self.health_percent = 0
            self.state = 'defeated'
            self.updown_juice = 0

    def state_transition(self, state, state_seconds):
        '''Go into the next state for so many seconds.'''
        self.state = state
        self.state_frames_remaining = int(state_seconds * 60)

    def update_state(self):
        '''Implements a simple state machine for determing the Opponent's
        next state and how much more time remains in the current one.'''
        if self.state not in ['defeated']:
            self.state_frames_remaining -= 1
            if self.state_frames_remaining <= 0:
                if self.state == 'idle':
                    # Start charging an attack
                    self.state_transition('charging', 3)
                elif self.state == 'damaged':
                    self.state_transition('idle', 2)
                if self.state == 'charging':
                    # TODO: implement an attack here
                    self.state_transition('idle', 2)

    def render(self):
        '''Returns a pygame.Surface with the rendered opponent.'''
        self.rect = self.opponent_image.get_rect()
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))
        center_rect = self.rect.copy()
        center_rect.centerx = self.surface.get_rect().centerx
        if self.state in ['idle', 'damaged', 'charging']:
            self.updown_juice += (2.0 * math.pi) / 60.0
            center_rect.centery = self.surface.get_rect().centery + 10 * math.sin(self.updown_juice)
        elif self.state == 'defeated':
            self.updown_juice += 5
            center_rect.centery = self.surface.get_rect().centery + self.updown_juice
        self.surface.blit(self.opponent_image, center_rect)
        return self.surface

class TrainingDummy(Opponent):
    '''Opponent subclass used for the tutorial level.'''
    # TODO: Implement attack patterns via function overrides.
    pass
