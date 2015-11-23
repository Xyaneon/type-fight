#!/bin/python

import logging, math, os, pygame, sys

logging.basicConfig(filename='typefight.log', filemode='w',
                    format='%(levelname)s:%(message)s', level=logging.DEBUG)

prompt_height = 55
pygame.font.init()
command_font = pygame.font.Font("fonts/Share_Tech_Mono/ShareTechMono-Regular.ttf", 32)
command_bkg_color = pygame.color.Color(0, 0, 0)
command_text_color = pygame.color.Color(0, 255, 0)

class CommandEntry:
    '''Class for managing the command entry window.'''
    def __init__(self):
        self.surface = pygame.Surface((385, prompt_height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.text = ''
        self.text_surface = command_font.render('>', True, command_text_color)
        self.cursor_surface = None
        self.cursor_pos = 0
        self.cursor_fade_phase = 0

    def set_text(self, text):
        '''Sets the text displayed in the command entry window.'''
        self.text = text

    def get_text(self):
        '''Returns the currently displayed text in the command entry window.'''
        return self.text

    def handle_keydown_event(self, event, player, opponent):
        '''Handles a KEYDOWN event, which is very important for this particular
        class since it handles text input from the keyboard.
        Also takes the Player and Opponent objects for modification.'''

        # Don't allow the player to keep entering commands after they win
        if opponent.state == 'defeated':
            return

        if event.key == pygame.K_BACKSPACE:
            # Delete text before cursor.
            self.backspace_at_cursor()
        elif event.key == pygame.K_DELETE:
            # Delete text highlighted by (at) cursor.
            self.delete_at_cursor()
        elif event.key == pygame.K_LEFT:
            self.move_cursor_left()
        elif event.key == pygame.K_RIGHT:
            self.move_cursor_right()
        elif event.key == pygame.K_RETURN:
            self.process_command(player, opponent)
        else:
            self.insert_char_at_cursor(event.unicode)
        # Update rendered command text after a keypress instead of doing it
        # continually in render()
        self.text_surface = command_font.render('>' + self.text, True, command_text_color)

    def parse_attack(self, attack_string):
        '''Returns a dictionary with the attack direction and command
        separated out for easier processing.'''
        # Check first whether the direction came before or after the
        # actual command
        try:
            # Direction first?
            direction = attack_string.split()[0]
            if direction not in ['left', 'right', 'center']:
                # Direction second?
                direction = attack_string.split()[-1]
                if direction not in ['left', 'right', 'center']:
                    # No direction found; default to center
                    direction = 'center'
                    command = attack_string
                else:
                    command = ' '.join(attack_string.split()[:-1])
            else:
                command = ' '.join(attack_string.split()[1:])
        except IndexError as e:
            logging.exception('Error in attack parsing')
            # Return generic result instead of crashing
            return {'command': 'punch', 'direction': 'center'}
        return {'command': command, 'direction': direction}

    def process_command(self, player, opponent):
        '''Processes the entered command and modifies Player and Opponent if
        needed.'''
        txt = self.text.strip()
        if txt == 'exit':
            # Temporary debug command to quit the game
            pygame.quit()
            sys.exit()
        elif txt in ['forfeit', 'suicide', 'give up', 'you win', 'seppuku', 'hara kiri']:
            # Temporary debug command to kill yourself
            player.take_damage(100, 'both')
        elif txt in ['fatality', 'obliterate', 'instakill', 'I win', 'murderize']:
            # Temporary debug command to defeat your opponent instantly
            opponent.take_damage(100, 'center')
        else:
            # Treat this as an actual attack command and get the direction
            attack = self.parse_attack(txt)

            if attack['command'] in ['punch', 'jab']:
                opponent.take_damage(5, attack['direction'])
            elif attack['command'] == 'haymaker':
                opponent.take_damage(8, attack['direction'])
            elif attack['command'] in ['open palm thrust', 'open palm strike', 'op']:
                opponent.take_damage(2, attack['direction'])
            elif attack['command'] in ['block', 'blk']:
                # The player should block
                player.block(attack['direction'])
        self.text = ''
        self.cursor_pos = 0

    def move_cursor_left(self):
        '''Moves the current cursor position left one character, if able.'''
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def move_cursor_right(self):
        '''Moves the current cursor position right one character, if able.'''
        if self.text != "":
            if self.cursor_pos < len(self.text):
                self.cursor_pos += 1

    def set_cursor_at_beginning(self):
        '''Moves the cursor all the way back to the start of the text.'''
        self.cursor_pos = 0

    def set_cursor_at_end(self):
        '''Moves the cursor all the way to the end of the text.'''
        if len(self.text) != 0:
            self.cursor_pos = len(self.lines) - 1
        else:
            self.cursor_pos = 0

    def get_cursor_position(self):
        '''Returns the index in the text that the cursor position corresponds to.'''
        return self.cursor_pos

    def backspace_at_cursor(self):
        '''Deletes the character before the cursor position.'''
        if not self.cursor_pos == 0:
            if self.cursor_pos == 1:
                self.text = self.text[1:]
            elif self.cursor_pos == len(self.text) - 1:
                self.text = self.text[:-1]
            else:
                self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
            self.move_cursor_left()

    def delete_at_cursor(self):
        '''Deletes the character at the cursor position.'''
        if self.cursor_pos == 0:
            self.text = self.text[1:]
        elif self.cursor_pos == len(self.text) - 1:
            self.text = self.text[:-1]
        else:
            self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]

    def insert_char_at_cursor(self, character):
        '''Inserts the given character at the cursor position.'''
        if self.cursor_pos == 0:
            self.text = character + self.text
        elif self.cursor_pos == len(self.text):
            self.text = self.text + character
        else:
            self.text = self.text[:self.cursor_pos] + character + self.text[self.cursor_pos:]
        self.move_cursor_right()

    def render(self):
        '''Returns a pygame.Surface containing the rendered command prompt
        window and text.'''
        padding = 10
        self.cursor_fade_phase += (2.0 * math.pi) / 60.0
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        # For text cursor
        cursor_draw_pos = command_font.size('>' + self.text[:self.cursor_pos])[0]
        cursor_color = command_text_color
        cursor_alpha = int(math.floor(math.fabs(255 * math.sin(self.cursor_fade_phase))))
        cursor_alpha =  min(255, max(0, cursor_alpha))
        self.cursor_surface = command_font.render('_', False, cursor_color)
        self.cursor_surface = self.cursor_surface.convert()
        self.cursor_surface.set_alpha(cursor_alpha)

        border_rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, command_bkg_color, border_rect)
        if self.text_surface is not None:
            text_left_align = padding
            text_top_align = padding
            self.surface.blit(self.text_surface, (text_left_align, text_top_align))
            if self.cursor_surface is not None:
                self.surface.blit(self.cursor_surface, (text_left_align + cursor_draw_pos, text_top_align))
        return self.surface
