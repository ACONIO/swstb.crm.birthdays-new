"""Robot test cases."""

import os
import jinja2 as j2
import faulthandler
import functools

from bot import _items

from aconio import outlook, db
from aconio.core import errors

from robocorp import tasks


@functools.lru_cache
def jinja_env() -> j2.Environment:
    return j2.Environment()


@functools.lru_cache
def bmd_db() -> db.MSSQLConnection:
    conn = db.MSSQLConnection().configure_from_vault("bmd_db_credentials")
    return conn


faulthandler.disable()


@tasks.task
def test_generic() -> None:
    """Template for quickly testing throughout the development process."""
    pass


@tasks.task
def test_create_email() -> None:
    """Create e-mail with mock template and save as draft.

    Useful to verify how a rendered mail template looks in Outlook.
    """

    outlook.start()

    outlook.send_email(
        to="dummy@aconio.net",
        subject="Mock E-Mail",
        body=_render_template(),
        html_body=True,
        draft=True,
    )


def _render_template() -> str:
    templates = os.path.join(os.environ.get("ROBOT_ROOT"), "templates")

    jinja_env().loader = j2.FileSystemLoader(templates)

    template = jinja_env().get_template("mail.j2")

    return template.render()
