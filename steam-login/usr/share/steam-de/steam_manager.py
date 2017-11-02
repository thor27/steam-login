# STEAM DE - Steam Manager
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

from focus_listener import XWindowFocusListener
import subprocess
from time import sleep
from log import get_logger

logger = get_logger(__name__)


class SteamManager(XWindowFocusListener):
    def start(self):
        self.steam_process = subprocess.Popen(['$PREFIX $PROGRAM $STEAM_ARGS'], shell=True)
        self.steamWindow = None
        self.steamWait = True
        super().start()

    def stop(self, *args, **kwargs):
        if not self.running:
            return
        super().stop()
        if self.steam_process.poll() is None:
            self.stop_steam()
        logger.info('Steam is not running anymore, exiting...')

    def stop_steam(self):
        steps = [
            ('shutdown', lambda: subprocess.Popen(['$STEAM -shutdown'], shell=True)),
            ('TERM signal', self.steam_process.terminate),
            ('KILL signal', self.steam_process.kill)
        ]

        for step, func in steps:
            logger.info('Waiting for {}...'.format(step))
            func()
            try:
                self.steam_process.wait(10)
                return
            except subprocess.TimeoutExpired:
                logger.error('{} failed!'.format(step))

        raise Exception('Problem when trying to stop Steam. Process may remaing running...')

    def handle_ping(self):
        if self.steam_process.poll() is not None:
            self.stop()

    def handle_change(self, xid, title):
        if not self.steamWindow:
            logger.info('Waiting for Steam Window...')
            if title == "Steam":
                self.steamWindow = xid
            return

        if xid != 0:
            logger.info('Another window is focused')
            return

        logger.info('No window is focused, wait two seconds if a window shows up...')

        for x in range(20):
            xid = self.get_active_window()[0]
            if xid != 0:
                logger.info('Another window is focused now, no need to raise steam window')
                return
            sleep(0.1)

        if self.steamWindow in self.get_windows_list():
            logger.info('Steam window exists but is not focused, try to focus it')
            with self.window_obj(self.steamWindow) as window:
                self.set_focus(window)
            return

        logger.info('Steam window does not exists anymore! Shutting down!')
        self.stop()
