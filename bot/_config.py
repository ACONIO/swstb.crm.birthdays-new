"""Robot configuration management."""

import os
import pydantic


class BaseConfig(pydantic.BaseModel):
    """Shared configuration."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class ProducerConfig(BaseConfig):
    """Producer configuration."""

    pass


class ConsumerConfig(BaseConfig):
    """Consumer configuration."""

    # The != "false" condition prevents the test mode from accidentally being
    # turned off, for example through a typo. Everything which is not
    # "false" will resolve to "true" and thus enable the test mode.
    test_mode: bool = os.environ.get("TEST_MODE", "true").lower() != "false"
    """
    If enabled, the bot does not perform any "critical" actions, such as
    sending e-mails, or inserting data in applications.
    Per default, test mode is enabled.
    """

    subject: str = os.environ.get("SUBJECT")
    """
    The subject of the birthday congratulations e-mail to send.
    """
