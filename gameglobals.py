#!/bin/python

import pygame

# Global variables and constants
GAME_VERSION = '0.4'
FPS_TARGET = 60
DEFAULT_WINDOW_SIZE = (1080, 911)
DEFAULT_WINDOW_CENTERX = DEFAULT_WINDOW_SIZE[0] / 2
DEFAULT_WINDOW_CENTERY = DEFAULT_WINDOW_SIZE[1] / 2

# Global functions
def scale_rect(rect, scale_x, scale_y):
    '''Scales a Rect object in response to a display size change, and returns
    a new Rect.'''
    # Idea from http://stackoverflow.com/a/20003829/3775798
    new_rect = rect.copy()
    rect.width *= scale_x
    rect.height *= scale_y
    rect.x *= scale_x
    rect.y *= scale_y
    return new_rect

def scale_rect_ip(rect, scale_x, scale_y):
    '''Scales a Rect object in response to a display size change, in place.'''
    # Idea from http://stackoverflow.com/a/20003829/3775798
    rect.width *= scale_x
    rect.height *= scale_y
    rect.x *= scale_x
    rect.y *= scale_y

def calculate_scale_factor(old_size, new_size):
    '''Takes two pairs of width and height values and returns the scaling
    factor as a pair of floats.'''
    return (float(new_size[0]) / float(old_size[0]),
            float(new_size[1]) / float(old_size[1]))

def scale_rects_ip(rect_list, old_size, new_size):
    '''Takes a list of Rects to scale, along with the old and new dimensions
    of the screen. Meant to be used for window resizing, where all the rects
    need to be updated as well. Updates the Rects in the list in place.'''
    scale_factor = calculate_scale_factor(old_size, new_size)
    for rect in rect_list:
        scale_rect_ip(rect, scale_factor[0], scale_factor[1])
