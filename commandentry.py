#!/bin/python

import logging, math, os, platform, pygame, random, sys, webbrowser

# Logging setup
if platform.system() == 'Windows':
    # Logging on Windows
    logdir = os.path.join(os.getenv('APPDATA'), 'typefight')
else:
    # Assume Linux
    logdir = os.path.join(os.path.expanduser('~'), '.typefight')
try:
    os.makedirs(logdir)
except OSError:
    if not os.path.isdir(logdir):
        raise
logname = os.path.join(logdir, 'typefight.log')
logging.basicConfig(filename=logname, filemode='w',
                    format='%(levelname)s:%(message)s',
                    level=logging.DEBUG)

prompt_width = 450
prompt_height = 55
pygame.font.init()
command_font = pygame.font.Font("fonts/Share_Tech_Mono/ShareTechMono-Regular.ttf", 32)
command_bkg_color = pygame.color.Color(0, 0, 0)
command_text_color = pygame.color.Color(0, 255, 0)

class CommandEntry:
    '''Class for managing the command entry window.'''
    def __init__(self):
        self.surface = pygame.Surface((prompt_width, prompt_height), pygame.SRCALPHA)
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

    def handle_keydown_event(self, event, player, opponent, c_output):
        '''Handles a KEYDOWN event, which is very important for this particular
        class since it handles text input from the keyboard.
        Also takes the Player, Opponent and CommandOutput objects for
        modification.'''

        # Don't allow the player to keep entering commands after they win
        if opponent.state == 'defeated':
            return
        if player.health_percent <= 0:
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
            output_line = self.process_command(player, opponent)
            # Update output window if needed
            c_output.add_line(output_line)
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
        except:
            logging.exception('Error in attack parsing')
            raise
        return {'command': command, 'direction': direction}

    def process_command(self, player, opponent):
        '''Processes the entered command and modifies Player and Opponent if
        needed. Returns a String to display as feedback.'''
        output_string = 'ERROR: No command found.'
        txt = self.text.strip()
        if txt == '':
            return output_string

        self.text = ''
        self.cursor_pos = 0

        # Check for "special commands" first which are not attacks or blocks
        # Could be debug commands, cheat codes, Easter eggs or other things
        if txt == 'exit':
            # Temporary debug command to quit the game
            output_string = 'System shutdown.'
            pygame.quit()
            sys.exit()
        elif txt == 'help':
            # Show the game help file in the browser
            output_string = 'INFO: Displaying manual.'
            webbrowser.open_new('help/typefight.html')
        elif txt in ['forfeit', 'suicide', 'give up', 'you win', 'seppuku', 'hara kiri']:
            # Temporary debug command to kill yourself
            output_string = 'Self-destruct activated.'
            player.take_damage(100, 'both')
        elif txt in ['fatality', 'obliterate', 'instakill', 'I win', 'murderize']:
            # Temporary debug command to defeat your opponent instantly
            output_string = 'Opponent obliterated.'
            opponent.take_damage(100, 'center')
        elif txt in ['kick', 'jump', 'knee']:
            # Easter egg
            output_string = '404: legs not found.'
        elif txt == 'kamehameha':
            # Easter egg
            output_string = 'Module "dbz" not installed.'
        elif txt in ['head butt', 'headbutt']:
            # Easter egg
            output_string = 'Not trying that one again.'
        elif txt == 'elbow':
            # Easter egg
            output_string = 'Target outside elbow range.'
        elif txt in ['grapple', 'grab']:
            # Easter egg
            output_string = 'Grappling hook malfunction.'
        elif txt in ['magic', 'cast spell', 'avada kedavra', 'hocus pocus']:
            # Easter egg
            output_string = 'Dude... these are robots. :/'
        elif txt in ['gun', 'shoot', 'fire']:
            # Easter egg
            output_string = 'Out of ammo.'
        elif txt == 'tickle':
            # Easter egg
            output_string = 'Target does not look ticklish.'
        else:
            # Treat this as an actual attack command and get the direction
            try:
                attack = self.parse_attack(txt)
            except:
                logging.error('Attack parsing failed with command string \'%s\'', txt)
                # Use generic result instead of crashing
                attack = {'command': 'punch', 'direction': 'center'}

            if attack['command'] in ['punch', 'jab', 'hit', 'strike', 'attack']:
                opponent.take_damage(5, attack['direction'])
                player.unblock(attack['direction'])
                output_string = 'Used ' + attack['direction'] + ' punch'
            elif attack['command'] == 'haymaker':
                # Haymaker can only come from right or left
                if attack['direction'] not in ['left', 'right']:
                    attack['direction'] = random.choice(['left', 'right'])
                opponent.take_damage(8, attack['direction'])
                player.unblock(attack['direction'])
                output_string = 'Used ' + attack['direction'] + ' haymaker'
            elif attack['command'] == 'uppercut':
                # Uppercut can only be aimed at center targets
                opponent.take_damage(8, 'center')
                player.unblock('center')
                output_string = 'Used uppercut'
            elif attack['command'] in ['open palm thrust', 'open palm strike', 'op']:
                opponent.take_damage(2, attack['direction'])
                player.unblock(attack['direction'])
                output_string = 'Used ' + attack['direction'] + ' open palm strike'
            elif attack['command'] in ['block', 'blk']:
                # The player should block
                player.block(attack['direction'])
                output_string = attack['direction'] + ' block activated'
            elif attack['command'] in ['unblock', 'unblk']:
                # The player should unblock
                player.unblock(attack['direction'])
                output_string = attack['direction'] + ' block deactivated'
            else:
                output_string = 'ERROR: Invalid command.'
        return output_string.capitalize()

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
