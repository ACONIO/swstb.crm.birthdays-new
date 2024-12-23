"""Handle UI interactions with the Advokat application."""

import subprocess
import faulthandler

from robocorp import windows, log

from aconio.core import utils

from aconio.advokat.ui import erv
from aconio.advokat.ui import act_mgmt
from aconio.advokat.ui import ds_assistant

faulthandler.disable()


def window(**kwargs) -> windows.WindowElement:
    """Return the main Advokat window."""
    return windows.find_window(
        'name:"ADVOKAT - [Herzlich willkommen]"', **kwargs
    )


def is_open(timeout: int = 10) -> bool:
    """Return whether the Advokat window is open."""
    return window(raise_error=False, timeout=timeout) is not None


def open_application(exe_path: str) -> None:
    """Open the Advokat application."""
    subprocess.run([exe_path], check=True)

    _wait_for_advokat_window(retries=5)


def _wait_for_advokat_window(retries: int, timeout: int = 10) -> None:
    for _ in range(retries):
        if is_open(timeout):
            return

    raise RuntimeError("Failed to open Advokat application.")


def close_application() -> None:
    """Close the Advokat application."""

    try:
        _close_advokat_window()
    except Exception as exc:  # pylint: disable=broad-except
        log.debug(f"Failed to close Advokat window: {exc}")

    if is_open(timeout=2):
        subprocess.run(["taskkill", "/f", "/im", "Advokat3.exe"], check=True)


def _close_advokat_window() -> None:
    """Close the Advokat window."""
    menu = window().find('name:"Anwendungsmenü"').find('name:"Programme"')
    menu.click()

    menu.find('control:MenuItemControl and subname:"Beenden"').click()


def start_program(name: str) -> None:
    """Start one of the Advokat programs from the main menu.

    Args:
        name:
            Name of the program, e.g. "ERV". The name must be equivalent to
            an item from the Advokat "Programme" menu bar.
    """

    menu = window().find('name:"Anwendungsmenü"').find('name:"Programme"')
    menu.click()

    menu.find(f'control:MenuItemControl and name:"{name}"').click()
