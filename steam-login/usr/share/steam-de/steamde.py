#!/usr/bin/env python3
# STEAM DE - Steam Manager Startup
#
# Based on code by Stephan Sokolow
# Source: https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8
#
# Copyright (C) 2017  Thomaz de Oliveira dos Reis <thor27@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from steam_manager import SteamManager
from signal import signal, SIGINT, SIGTERM
from log import get_logger

logger = get_logger(__name__)

if __name__ == '__main__':
    logger.info('Starting Steam Manager - Keep it focused and managed!')
    steam_manager = SteamManager()
    signal(SIGINT, steam_manager.stop)
    signal(SIGTERM, steam_manager.stop)
    steam_manager.start()
    logger.info('Closing Steam Manager. Good Bye!')
