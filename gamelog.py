#!/bin/python

import datetime, logging, platform, pygame, os
from gameglobals import *

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
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)

# Write initial info to log
logging.info('TypeFight! version ' + GAME_VERSION)
logging.info('Platform: ' + platform.system())
logging.info('FPS target: ' + str(FPS_TARGET))
logging.info('Logging further messages at log level ' + \
             str(logging.getLogger().getEffectiveLevel()))

def log_display_info():
    '''Records some display information to the log, which could be useful if
    graphics issues arise.'''
    logging.info('Display driver: ' + pygame.display.get_driver())
    logging.info('Display info: ' + str(pygame.display.Info()))
    wm_info = pygame.display.get_wm_info()
    wm_info_string = ''
    for key in wm_info:
        wm_info_string += '\n\t' + key + ':\t' + str(wm_info[key])
    logging.info('Window manager info:' + wm_info_string)
