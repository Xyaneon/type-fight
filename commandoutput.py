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
        self.text_surface = pygame.Surface((output_width - padding * 2,
                                            output_height - padding),
                                           pygame.SRCALPHA)

    def add_line(self, line_text):
        '''Adds a new line to the output, while staying within the max line
        limit. We use a collections.deque for this.'''
        self.text_surface.fill(pygame.Color(0, 0, 0, 0))
        self.text_lines.append(line_text)
        line_surfaces = []
        for line in self.text_lines:
            line_surfaces.append(output_font.render(line, True, output_text_color))
        current_top = 0
        for line_surface in line_surfaces:
            self.text_surface.blit(line_surface, (0, current_top))
            current_top += output_font.get_linesize()
        # Transparent text using RGBA multiplication
        # Based on code from http://stackoverflow.com/a/32933420
        alpha_surf = pygame.Surface(self.text_surface.get_rect().size, pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, 200))
        self.text_surface.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

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
