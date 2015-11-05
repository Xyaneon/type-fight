#!/usr/bin/python

import pygame

class CommandEntry:
    '''Class for managing the command entry window.'''
    def __init__(self):
        self.rect = None
        self.surface = None
        self.text = ''
        self.text_surface = None
        self.cursor_pos = 0

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
        else:
            self.insert_char_at_cursor(keyboardentry.GetCharFromKey(event))
        self.redraw()

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
