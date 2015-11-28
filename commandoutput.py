#!/bin/python

import pygame

pygame.font.init()
output_font = pygame.font.Font("fonts/Share_Tech_Mono/ShareTechMono-Regular.ttf", 16)
output_bkg_color = pygame.color.Color(0, 0, 0, 255/2)
output_text_color = pygame.color.Color(0, 255, 0, 255*3/4)

output_height = 300
output_width = 350
max_output_lines = 5

class CommandOutput():
    '''Class for displaying flavor text feedback to the player in a chat box
    or log format.'''
    def __init__(self):
        self.surface = pygame.Surface((output_width, output_height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.text_lines = []
        self.text_surface = output_font.render('>', True, output_text_color)

    def render(self):
        '''Returns a pygame.Surface containing the rendered output window and
        text.'''
        padding = 10
        self.surface.fill(pygame.Color(0, 0, 0, 0))

        border_rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, output_bkg_color, border_rect)
        if self.text_surface is not None:
            text_left_align = padding
            text_top_align = padding
            self.surface.blit(self.text_surface, (text_left_align, text_top_align))
        return self.surface
