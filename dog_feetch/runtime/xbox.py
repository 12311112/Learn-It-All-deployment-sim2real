#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import select
import sys
import termios
import threading
import time
import tty
from dataclasses import dataclass

# ==========================================
# This module provides a keyboard-backed controller interface.
# ==========================================
@dataclass
class _Button:
    """This module provides a keyboard-backed controller interface."""
    triggered: bool = False


class _Buttons:
    """This module provides a keyboard-backed controller interface."""
    def __init__(self, a_triggered=False):
        self.A = _Button(False)
        self.A.triggered = a_triggered


class XBoxController:
    """
    This module provides a keyboard-backed controller interface.

    This module provides a keyboard-backed controller interface.
    This module provides a keyboard-backed controller interface.
    This module provides a keyboard-backed controller interface.
    This module provides a keyboard-backed controller interface.
    This module provides a keyboard-backed controller interface.
    """

    def __init__(self, command_freq=20):
        """
        This module provides a keyboard-backed controller interface.
        """
        self.command_freq = float(command_freq)

        # This module provides a keyboard-backed controller interface.
        # This module provides a keyboard-backed controller interface.
        # This module provides a keyboard-backed controller interface.
        self._key_hold_s = 0.18
        self._cmd_scale =1

        self.buttons = _Buttons()
        self._lock = threading.Lock()
        self._running = True

        # This module provides a keyboard-backed controller interface.
        self._last_press = {
            "w": 0.0, "s": 0.0,
            "a": 0.0, "d": 0.0,
            "q": 0.0, "e": 0.0,
        }

        # ==========================================
        # This module provides a keyboard-backed controller interface.
        # ==========================================
        self._stdin_fd = None
        self._stdin_settings = None

        # This module provides a keyboard-backed controller interface.
        if sys.stdin.isatty():
            self._stdin_fd = sys.stdin.fileno()
            # This module provides a keyboard-backed controller interface.
            self._stdin_settings = termios.tcgetattr(self._stdin_fd)

            # This module provides a keyboard-backed controller interface.
            # This module provides a keyboard-backed controller interface.
            tty.setcbreak(self._stdin_fd)

            # This module provides a keyboard-backed controller interface.
            atexit.register(self.close)
            print("[keyboard] : W/S , A/D , Q/E ,  ")
        else:
            print("[keyboard] stdin  TTY ")

        # This module provides a keyboard-backed controller interface.
        self._thread = threading.Thread(target=self._keyboard_worker, daemon=True)
        self._thread.start()

    def close(self):
        """This module provides a keyboard-backed controller interface."""
        self._running = False
        if self._stdin_fd is not None and self._stdin_settings is not None:
            try:
                # This module provides a keyboard-backed controller interface.
                termios.tcsetattr(
                    self._stdin_fd, termios.TCSADRAIN, self._stdin_settings
                )
            except Exception:
                pass

    def _keyboard_worker(self):
        """This module provides a keyboard-backed controller interface."""
        dt = 1.0 / max(self.command_freq, 1.0)
        while self._running:
            if self._stdin_fd is None:
                time.sleep(dt)
                continue

            # This module provides a keyboard-backed controller interface.
            # This module provides a keyboard-backed controller interface.
            readable, _, _ = select.select([sys.stdin], [], [], dt)
            if not readable:
                continue

            try:
                # This module provides a keyboard-backed controller interface.
                ch = sys.stdin.read(1)
            except Exception:
                continue

            now = time.time()
            ch = ch.lower()

            # This module provides a keyboard-backed controller interface.
            with self._lock:
                if ch in self._last_press:
                    self._last_press[ch] = now
                elif ch == " ":
                    self.buttons.A.triggered = True #  A

    def _active(self, key, now):
        """This module provides a keyboard-backed controller interface."""
        return (now - self._last_press[key]) <= self._key_hold_s

    def _compute_commands(self):
        """
        This module provides a keyboard-backed controller interface.
        """
        now = time.time()

        # This module provides a keyboard-backed controller interface.
        forward = float(self._active("w", now)) - float(self._active("s", now))
        # This module provides a keyboard-backed controller interface.
        lateral = float(self._active("a", now)) - float(self._active("d", now))
        # This module provides a keyboard-backed controller interface.
        yaw = float(self._active("q", now)) - float(self._active("e", now))

        return [
            self._cmd_scale * forward,
            self._cmd_scale * lateral,
            self._cmd_scale * yaw,
        ]

    def get_last_command(self):
        """
        This module provides a keyboard-backed controller interface.
        This module provides a keyboard-backed controller interface.
        This module provides a keyboard-backed controller interface.
        """
        with self._lock:
            # This module provides a keyboard-backed controller interface.
            cmds = self._compute_commands()

            # This module provides a keyboard-backed controller interface.
            a_triggered = self.buttons.A.triggered
            buttons = _Buttons(a_triggered=a_triggered)

            # This module provides a keyboard-backed controller interface.
            left_trigger = 0.0
            right_trigger = 0.0

            # This module provides a keyboard-backed controller interface.
            # This module provides a keyboard-backed controller interface.
            # This module provides a keyboard-backed controller interface.
            self.buttons.A.triggered = False

        return cmds, buttons, left_trigger, right_trigger
