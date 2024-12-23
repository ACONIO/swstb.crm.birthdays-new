"""Task definitions and setup/teardown handling."""

import faulthandler

import robocorp.workitems as workitems
import robocorp.tasks as tasks

import bot.consumer
import bot.producer

import bot._items as _items

faulthandler.disable()


@tasks.setup(scope="task")
def before_each(tsk):

    match tsk.name:
        case "producer":
            bot.producer.setup()
        case "consumer":
            bot.consumer.setup()
        case "reporter":
            bot.reporter.setup()


@tasks.teardown(scope="task")
def after_each(tsk):
    match tsk.name:
        case "producer":
            bot.producer.teardown()
        case "consumer":
            bot.consumer.teardown()
        case "reporter":
            bot.reporter.teardown()


@tasks.task
def producer():
    """Create output work items for the consumer."""

    for wi in bot.producer.run():
        workitems.outputs.create(wi.model_dump())


@tasks.task
def consumer():
    """Process all the work items created by the producer."""

    for item in workitems.inputs:
        with item:
            bot.consumer.run(_items.Item.model_validate(item.payload))
