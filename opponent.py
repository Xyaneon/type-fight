#!/bin/python

import math, os, pygame, random
from gameglobals import *

# Sound effects for attacks
pygame.mixer.init()
snd_punch = pygame.mixer.Sound(os.path.join('sounds', 'punch.wav'))
snd_block = pygame.mixer.Sound(os.path.join('sounds', 'Swords_Collide-Sound_Explorer-2015600826.wav'))

class Opponent:
    '''Class representing the opponent the player can see.'''
    def __init__(self, screen):
        self.surface = pygame.Surface((screen.get_width(),
                                       screen.get_height()),
                                      pygame.SRCALPHA).copy()
        # Asset loading
        self.image_neutral = self._load_image('opponent_neutral.png')
        self.image_block_left = self._load_image('opponent_block_left.png')
        self.image_block_right = self._load_image('opponent_block_right.png')
        self.image_block_both = self._load_image('opponent_block_both.png')
        self.image_charging_left = self._load_image('opponent_charging_left.png')
        self.image_charging_right = self._load_image('opponent_charging_right.png')
        self.image_charging_both = self._load_image('opponent_charging_both.png')
        self.image_attack_left = self._load_image('opponent_attack_left.png')
        self.image_attack_right = self._load_image('opponent_attack_right.png')
        self.image_attack_both = self._load_image('opponent_attack_both.png')
        self.image_damaged = self._load_image('opponent_damaged.png')
        self.image_damaged_left = self._load_image('opponent_damaged_left.png')
        self.image_damaged_right = self._load_image('opponent_damaged_right.png')
        self.image_damaged_up = self._load_image('opponent_damaged_up.png')
        self.image_damaged_down = self._load_image('opponent_damaged_down.png')
        self.image_defeated = self._load_image('opponent_defeated.png')
        # Member variable setup
        self.opponent_image = self.image_neutral
        self.rect = self.opponent_image.get_rect()
        self.rect.centerx = self.surface.get_rect().centerx
        self.rect.centery = self.surface.get_rect().centery
        self.updown_juice = 0
        self.health_percent = 100
        self.attack_delay_frames = 0
        self.state = 'idle'
        self.state_frames_remaining = 60
        self.weak_spots = []
        self.opponent_name = '[Placeholder]'

    def _load_image(self, filename):
        '''Internal function for loading image assets.'''
        path = os.path.join('graphics', 'Mockup', filename)
        return pygame.image.load(path).convert_alpha()

    def get_rect(self):
        '''Returns a pygame.rect.Rect with size and position info.'''
        return self.rect

    def take_damage(self, damage, direction):
        '''Deals damage to this Opponent.'''
        if not ((self.state == 'block_left' and direction == 'left') or \
                (self.state == 'block_right' and direction == 'right') or \
                (self.state == 'block_both' and direction == 'center')):
            snd_punch.play()
            self.health_percent -= damage

            # Transition to damaged state for stun and animation
            self.state_transition('damaged', 0.2)
            if direction == 'left':
                self.opponent_image = self.image_damaged_left
            elif direction == 'right':
                self.opponent_image = self.image_damaged_right

            # Check if defeated
            if self.health_percent <= 0:
                self.health_percent = 0
                self.state_transition('defeated', 1)
                self.updown_juice = 0
        else:
            # Attack was blocked
            snd_block.play()

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
            self.opponent_image = random.choice([self.image_damaged,
                                                 self.image_damaged_up,
                                                 self.image_damaged_down])
        if state == 'defeated':
            self.opponent_image = self.image_defeated
        self.state_frames_remaining = int(math.floor(state_seconds * float(FPS_TARGET)))

    def update_state(self, player, c_output):
        '''Implements a simple state machine for determing the Opponent's
        next state and how much more time remains in the current one.
        Also takes a Player instance in case damage needs to be dealt as a
        result of an attack, and a CommandOutput for any output.'''
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
                    self.state_transition(random.choice(['idle', 'block_left', 'block_right', 'block_both']), 2)
                elif self.state == 'charging_left':
                    player.take_damage(5, 'left')
                    self.state_transition('attack_left', 0.25)
                elif self.state == 'charging_right':
                    player.take_damage(5, 'right')
                    self.state_transition('attack_right', 0.25)
                elif self.state == 'charging_both':
                    player.take_damage(5, 'both')
                    self.state_transition('attack_both', 0.25)
                elif self.state in ['block_left', 'block_right', 'block_both']:
                    self.state_transition(random.choice(['idle', 'charging_left', 'charging_right', 'charging_both']), 1)
                    if self.state == 'charging_left':
                        c_output.add_line('Incoming left attack!')
                    elif self.state == 'charging_right':
                        c_output.add_line('Incoming right attack!')
                    elif self.state == 'charging_both':
                        c_output.add_line('Incoming center attack!')
                elif self.state in ['attack_left', 'attack_right', 'attack_both']:
                    self.state_transition('idle', 1)

    def render(self):
        '''Returns a pygame.Surface with the rendered opponent.
        This also updates the rect variable for this instance.'''
        center_rect = self.opponent_image.get_rect().copy()
        center_rect.centerx = DEFAULT_WINDOW_CENTERX
        if self.state in ['idle', 'damaged', 'charging_left', 'charging_right']:
            self.updown_juice += (2.0 * math.pi) / float(FPS_TARGET)
            center_rect.centery = DEFAULT_WINDOW_CENTERY + 10 * math.sin(self.updown_juice)
        elif self.state == 'defeated':
            self.updown_juice += 5
            center_rect.centery = DEFAULT_WINDOW_CENTERY + self.updown_juice
        else:
            self.updown_juice = 0
            center_rect.centery = DEFAULT_WINDOW_CENTERY
        self.rect = center_rect
        return self.opponent_image

class TrainingDummy(Opponent):
    '''Opponent subclass used for the tutorial level.'''
    # TODO: Implement attack patterns via function overrides.
    pass
