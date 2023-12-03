from telegram.ext import CommandHandler

from .core import commands as core_commands

core_handlers = [CommandHandler(c.__name__, c) for c in core_commands]

command_handlers: list[CommandHandler] = [
    *core_handlers,
]

__all__ = ['command_handlers']
