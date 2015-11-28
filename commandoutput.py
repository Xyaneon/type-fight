#!/bin/python

import datetime, pygame
from collections import deque

pygame.font.init()
output_font = pygame.font.Font("fonts/Share_Tech_Mono/ShareTechMono-Regular.ttf", 14)
output_bkg_color = pygame.color.Color(0, 255, 255, 255/10)
output_text_color = pygame.color.Color(0, 255, 255, 255/2)

padding = 10
max_output_lines = 8
output_height = output_font.get_linesize() * max_output_lines + padding * 2
output_width = 350 + padding * 2

class CommandOutput():
    '''Class for displaying flavor text feedback to the player in a chat box
    or log format.'''
    def __init__(self):
        self.surface = pygame.Surface((output_width, output_height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.text_lines = deque(['' * max_output_lines], maxlen=max_output_lines)
        self.text_surface = pygame.Surface((output_width, output_height), pygame.SRCALPHA)

    def add_line(self, line_text):
        '''Adds a new line to the output, while staying within the max line
        limit. We use a collections.deque for this.'''
        time_string = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
        self.text_surface.fill(pygame.Color(0, 0, 0, 0))
        self.text_lines.append('[' + time_string + ']: ' + line_text)
        line_surfaces = []
        for line in self.text_lines:
            line_surfaces.append(output_font.render(line, True, output_text_color))
        current_top = 0
        for line_surface in line_surfaces:
            self.text_surface.blit(line_surface, (0, current_top))
            current_top += output_font.get_linesize()

    def render(self):
        '''Returns a pygame.Surface containing the rendered output window and
        text.'''
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        border_rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, output_bkg_color, border_rect)
        if self.text_surface is not None:
            text_left_align = padding
            text_top_align = padding
            self.surface.blit(self.text_surface, (text_left_align, text_top_align))
        return self.surface
