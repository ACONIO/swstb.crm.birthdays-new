"""Functions utilized by the producer process."""

import functools

import aconio.db as db
import aconio.core.errors as errors

import bot._items as _items
import bot._config as _config


@functools.lru_cache
def config() -> _config.ProducerConfig:
    return _config.ProducerConfig()


@functools.lru_cache
def bmd_db() -> db.MSSQLConnection:
    conn = db.MSSQLConnection().configure_from_vault("bmd_db_credentials")
    return conn


def setup() -> None:
    """Setup producer process."""

    bmd_db().connect()
    if not bmd_db().is_connected():
        raise errors.ApplicationError("Failed to connect to BMD database")


def teardown() -> None:
    """Teardown producer process."""
    pass


def run() -> list[_items.Item]:
    """Generate a list of work items."""

    return _items.create_work_items_from_db(bmd_db())
