# STEAM DE - Focus Listener
#
# Adapted from
# https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8
#
# Copyright (C) 2017  Thomaz de Oliveira dos Reis <thor27@gmail.com>
# Copyright (C) 2017  Stephan Sokolow <http://blog.ssokolow.com/contact/>
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
#
# Design:
# -------
#
# Any modern window manager that isn't horrendously broken maintains an X11
# property on the root window named _NET_ACTIVE_WINDOW.
#
# Any modern application toolkit presents the window title via a property
# named _NET_WM_NAME.
#
# This listens for changes to both of them and then hides duplicate events
# so it only reacts to title changes once.

import Xlib
import Xlib.display
import select
from contextlib import contextmanager
from log import get_logger

logger = get_logger(__name__)


class XWindowFocusListener(object):
    def __init__(self):
        # Connect to the X server and get the self.root window
        self.disp = Xlib.display.Display()
        self.root = self.disp.screen().root
        # Prepare the property names we use so they can be fed into X11 APIs
        self.net_active_window = self.disp.intern_atom('_NET_ACTIVE_WINDOW')
        self.net_wm_name = self.disp.intern_atom('_NET_WM_NAME')  # UTF-8
        self.wm_name = self.disp.intern_atom('WM_NAME')           # Legacy encoding
        self.running = False
        self.last_seen = {'xid': None, 'title': None}

    @contextmanager
    def window_obj(self, win_id):
        """Simplify dealing with BadWindow (make it either valid or None)"""
        window_obj = None
        if win_id:
            try:
                window_obj = self.disp.create_resource_object('window', win_id)
            except Xlib.error.XError:
                pass
        yield window_obj

    def get_active_window(self):
        """Return a (window_obj, focus_has_changed) tuple for the active window."""
        win_id = self.root.get_full_property(
            self.net_active_window,
            Xlib.X.AnyPropertyType
        ).value[0]

        focus_changed = (win_id != self.last_seen['xid'])
        if focus_changed:
            with self.window_obj(self.last_seen['xid']) as old_win:
                if old_win:
                    old_win.change_attributes(event_mask=Xlib.X.NoEventMask)

            self.last_seen['xid'] = win_id
            with self.window_obj(win_id) as new_win:
                if new_win:
                    new_win.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

        return win_id, focus_changed

    def _get_window_name_inner(self, win_obj, no_xid=False):
        """Simplify dealing with _self.net_wm_name (UTF-8) vs. self.wm_name (legacy)"""
        for atom in (self.net_wm_name, self.wm_name):
            try:
                window_name = win_obj.get_full_property(atom, 0)
            except UnicodeDecodeError:  # Apparently a Debian distro package bug
                title = "<could not decode characters>"
            else:
                if window_name:
                    win_name = window_name.value
                    if isinstance(win_name, bytes):
                        # Apparently COMPOUND_TEXT is so arcane that this is how
                        # tools like xprop deal with receiving it these days
                        win_name = win_name.decode('latin1', 'replace')
                    return win_name
                else:
                    title = ""
        if no_xid:
            return title
        return "{} (XID: {})".format(title, win_obj.id)

    def get_window_name(self, win_id):
        """Look up the window name for a given X11 window ID"""
        if not win_id:
            self.last_seen['title'] = "<no window id>"
            return self.last_seen['title']

        title_changed = False
        with self.window_obj(win_id) as wobj:
            if wobj:
                win_title = self._get_window_name_inner(wobj)
                title_changed = (win_title != self.last_seen['title'])
                self.last_seen['title'] = win_title

        return self.last_seen['title'], title_changed

    def handle_xevent(self, event):
        # Loop through, ignoring events until we're notified of focus/title change
        if event.type != Xlib.X.PropertyNotify:
            return

        changed = False
        if event.atom == self.net_active_window:
            if self.get_active_window()[1]:
                changed = changed or self.get_window_name(self.last_seen['xid'])[1]
        elif event.atom in (self.net_wm_name, self.wm_name):
            changed = changed or self.get_window_name(self.last_seen['xid'])[1]

        if changed:
            return self.handle_change(**self.last_seen)
        return True

    def get_windows_list(self):
        client_list = self.root.get_full_property(
            self.disp.intern_atom('_NET_CLIENT_LIST', False),
            Xlib.X.AnyPropertyType
        )
        return client_list.value if client_list else []

    def set_focus(self, window):
        window.circulate(Xlib.X.RaiseLowest)
        window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
        window.configure(stack_mode=Xlib.X.Above)

    def handle_change(self, xid, title):
        """Replace this with whatever you want to actually do"""
        raise NotImplemented

    def handle_ping(self):
        """This is executed each 1 second """
        raise NotImplemented

    def _wait_display_event(self):
        # Wait for display to send something, or a timeout of one second
        readable, w, e = select.select([self.disp], [], [], 1)
        if readable and self.disp in readable:
            return True
        return False

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        # Listen for _NET_ACTIVE_WINDOW changes
        self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

        # Prime last_seen with whatever window was active when we started this
        self.get_window_name(self.get_active_window()[0])
        self.handle_change(**self.last_seen)

        self.main_loop()

    def main_loop(self):
        while self.running:
            has_event = self._wait_display_event()

            self.handle_ping()

            if not has_event:
                continue

            while self.disp.pending_events():
                event = self.disp.next_event()
                try:
                    self.handle_xevent(event)
                except KeyboardInterrupt:
                    raise
                except Exception as ex:
                    logger.exception("Error handling X-Event!")
