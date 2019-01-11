#!/usr/bin/env python

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Allows visualising a 2D map generated by vehicles.

"""
Welcome to CARLA map visualizer

    ESC         : quit
"""

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================

import glob
import os
import sys

try:
    sys.path.append(glob.glob('**/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import carla

import argparse
import logging

try:
    import pygame
    from pygame.locals import K_DOWN
    from pygame.locals import K_LEFT
    from pygame.locals import K_RIGHT
    from pygame.locals import K_UP
    from pygame.locals import K_ESCAPE
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

# Handles keyboard and mouse input


class KeyboardInput(object):

    def _parse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                # Quick actions
                if event.key == K_ESCAPE:
                    exit_game()

    def _parse_keys(self):
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        # Do something

    def parse_input(self):
        self._parse_events()
        self._parse_keys()


def game_loop(args):

    # Init
    pygame.init()
    keyboard = KeyboardInput()

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(2.0)

        display = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(args.description)

        clock = pygame.time.Clock()
        while True:
            clock.tick_busy_loop(60)
            keyboard.parse_input()

            display.fill((0, 0, 0))
            pygame.display.update()

    finally:
        exit_game()


def main():
    # Parse arguments
    argparser = argparse.ArgumentParser(
        description='CARLA No Rendering Mode Visualizer')
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)'
    )
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720)')

    args = argparser.parse_args()
    args.description = argparser.description
    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    # Call game_loop
    try:
        game_loop(args)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


def exit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()