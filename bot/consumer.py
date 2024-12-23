"""Functions utilized by the consumer process."""

import functools
import jinja2 as j2

import aconio.outlook as outlook
import aconio.core.decorators as decorators

import bot._items as _items
import bot._config as _config


@functools.lru_cache
def config() -> _config.ConsumerConfig:
    return _config.ConsumerConfig()


@functools.lru_cache
def jinja() -> j2.Environment:
    return j2.Environment()


def setup() -> None:
    """Setup consumer process."""

    jinja().loader = j2.FileSystemLoader("templates")
    jinja().undefined = j2.StrictUndefined

    outlook.start()


def teardown() -> None:
    """Teardown consumer process."""
    pass


@decorators.attach_reporter
@decorators.run_function
def run(item: _items.Item):
    """Processes a single work item."""

    outlook.send_email(
        to=item.client.emails,
        cc=item.client.employee_emails,
        send_as="office@swstb.at",
        subject=config().subject,
        body=jinja().get_template("mail.j2").render(),
        html_body=True,
        draft=config().test_mode,
    )
