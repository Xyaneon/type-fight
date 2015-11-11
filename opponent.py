#!/bin/python

import math, os, pygame, random

# Sound effects for attacks
pygame.mixer.init()
snd_punch = pygame.mixer.Sound(os.path.join('sounds', 'punch.wav'))

class Opponent:
    '''Class representing the opponent the player can see.'''
    def __init__(self, screen):
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        # Asset loading
        self.image_neutral = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_neutral.png')).convert_alpha()
        self.image_block_left = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_block_left.png')).convert_alpha()
        self.image_block_right = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_block_right.png')).convert_alpha()
        self.image_block_both = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_block_both.png')).convert_alpha()
        self.image_charging_left = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_charging_left.png')).convert_alpha()
        self.image_charging_right = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_charging_right.png')).convert_alpha()
        self.image_charging_both = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_charging_both.png')).convert_alpha()
        self.image_attack_left = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_attack_left.png')).convert_alpha()
        self.image_attack_right = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_attack_right.png')).convert_alpha()
        self.image_attack_both = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_attack_both.png')).convert_alpha()
        self.image_damaged = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_damaged.png')).convert_alpha()
        self.image_defeated = pygame.image.load(os.path.join('graphics', 'Mockup',
                                  'opponent_defeated.png')).convert_alpha()
        # Member variable setup
        self.opponent_image = self.image_neutral
        self.rect = self.opponent_image.get_rect()
        self.updown_juice = 0
        self.health_percent = 100
        self.attack_delay_frames = 0
        self.state = 'idle'
        self.state_frames_remaining = 60
        self.weak_spots = []

    def get_rect(self):
        '''Returns a pygame.rect.Rect with size and position info.'''
        return self.rect

    def take_damage(self, damage, direction):
        '''Deals damage to this Opponent.'''
        if not ((self.state == 'block_left' and direction == 'left') or \
                (self.state == 'block_right' and direction == 'right') or \
                (self.state == 'block_both' and direction == 'center')):
            self.health_percent -= damage
            self.state_transition('damaged', 0.25)
            if self.health_percent <= 0:
                self.health_percent = 0
                self.state_transition('defeated', 1)
                self.updown_juice = 0

    def state_transition(self, state, state_seconds):
        '''Go into the next state for so many seconds.'''
        self.state = state
        if state == 'idle':
            self.opponent_image = self.image_neutral
        if state == 'block_left':
            self.opponent_image = self.image_block_left
        if state == 'block_right':
            self.opponent_image = self.image_block_right
        if state == 'block_both':
            self.opponent_image = self.image_block_both
        if state == 'charging_left':
            self.opponent_image = self.image_charging_left
        if state == 'charging_right':
            self.opponent_image = self.image_charging_right
        if state == 'charging_both':
            self.opponent_image = self.image_charging_both
        if state == 'attack_left':
            self.opponent_image = self.image_attack_left
        if state == 'attack_right':
            self.opponent_image = self.image_attack_right
        if state == 'attack_both':
            self.opponent_image = self.image_attack_both
        if state == 'damaged':
            self.opponent_image = self.image_damaged
        if state == 'defeated':
            self.opponent_image = self.image_defeated
        self.state_frames_remaining = int(math.floor(state_seconds * 60.0))

    def update_state(self, player):
        '''Implements a simple state machine for determing the Opponent's
        next state and how much more time remains in the current one.
        Also takes a Player instance in case damage needs to be dealt as a
        result of an attack.'''
        if self.state not in ['defeated']:
            self.state_frames_remaining -= 1
            if self.state_frames_remaining <= 0:
                if self.state == 'idle':
                    # Start charging an attack or block; showcase possibilities
                    action_list = ['charging_left',
                                   'charging_right',
                                   'charging_both',
                                   'block_left',
                                   'block_right',
                                   'block_both']
                    self.state_transition(random.choice(action_list), 1)
                elif self.state == 'damaged':
                    self.state_transition('idle', 2)
                elif self.state == 'charging_left':
                    player.take_damage(5, 'left')
                    snd_punch.play()
                    self.state_transition('attack_left', 0.25)
                elif self.state == 'charging_right':
                    player.take_damage(5, 'right')
                    snd_punch.play()
                    self.state_transition('attack_right', 0.25)
                elif self.state == 'charging_both':
                    player.take_damage(5, 'both')
                    snd_punch.play()
                    self.state_transition('attack_both', 0.25)
                elif self.state in ['block_left', 'block_right', 'block_both']:
                    self.state_transition(random.choice(['idle', 'charging_left', 'charging_right', 'charging_both']), 1)
                elif self.state in ['attack_left', 'attack_right', 'attack_both']:
                    self.state_transition('idle', 1)

    def render(self):
        '''Returns a pygame.Surface with the rendered opponent.'''
        self.rect = self.opponent_image.get_rect()
        self.surface.fill(pygame.color.Color(0, 0, 0, 0))
        center_rect = self.rect.copy()
        center_rect.centerx = self.surface.get_rect().centerx
        if self.state in ['idle', 'damaged', 'charging_left', 'charging_right']:
            self.updown_juice += (2.0 * math.pi) / 60.0
            center_rect.centery = self.surface.get_rect().centery + 10 * math.sin(self.updown_juice)
        elif self.state == 'defeated':
            self.updown_juice += 5
            center_rect.centery = self.surface.get_rect().centery + self.updown_juice
        else:
            self.updown_juice = 0
            center_rect.centery = self.surface.get_rect().centery
        self.surface.blit(self.opponent_image, center_rect)
        return self.surface

class TrainingDummy(Opponent):
    '''Opponent subclass used for the tutorial level.'''
    # TODO: Implement attack patterns via function overrides.
    pass
