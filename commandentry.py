#!/usr/bin/python

import math, pygame, sys

prompt_height = 64
pygame.font.init()
command_font = pygame.font.Font("fonts/Share_Tech_Mono/ShareTechMono-Regular.ttf", 32)
command_bkg_color = pygame.color.Color(0, 0, 0)
command_text_color = pygame.color.Color(0, 255, 0)

class CommandEntry:
    '''Class for managing the command entry window.'''
    def __init__(self):
        self.rect = None
        self.surface = None
        self.text = ''
        self.text_surface = None
        self.cursor_surface = None
        self.cursor_pos = 0
        self.cursor_fade_phase = 0

    def set_text(self, text):
        '''Sets the text displayed in the command entry window.'''
        self.text = text

    def get_text(self):
        '''Returns the currently displayed text in the command entry window.'''
        return self.text

    def handle_keydown_event(self, event):
        '''Handles a KEYDOWN event, which is very important for this particular
        class since it handles text input from the keyboard.'''
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
            # Process a command
            # Below is temporary debug code
            if self.text == 'exit':
                pygame.quit()
                sys.exit()
        else:
            self.insert_char_at_cursor(event.unicode)
        self.render()

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
        padding = 4
        self.cursor_fade_phase += (2.0 * math.pi) / 60.0
        self.surface = pygame.Surface((385, 55), pygame.SRCALPHA).copy()

        self.text_surface = command_font.render('>' + self.text, True, command_text_color)
        # For text cursor
        cursor_draw_pos = command_font.size('>' + self.text[:self.cursor_pos])[0]
        cursor_color = command_text_color
        cursor_alpha = int(math.floor(math.fabs(255 * math.sin(self.cursor_fade_phase))))
        cursor_alpha =  min(255, max(0, cursor_alpha))
        self.cursor_surface = command_font.render('_', False, cursor_color)
        self.cursor_surface = self.cursor_surface.convert()
        self.cursor_surface.set_alpha(cursor_alpha)

        border_rect = self.surface.get_rect().inflate(-padding, -padding).move(padding / 2, padding / 2)
        pygame.draw.rect(self.surface, command_bkg_color, border_rect)
        if self.text_surface is not None:
            text_left_align = padding
            text_top_align = padding
            self.surface.blit(self.text_surface, (text_left_align, text_top_align))
            self.surface.blit(self.cursor_surface, (text_left_align + cursor_draw_pos, text_top_align))
        return self.surface
