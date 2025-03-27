import click
import os
import sys
import logging
import IPython
from IPython.terminal.ipapp import load_default_config
from typing import List
from IPython.core.profiledir import ProfileDir

# Configure which logs to display
LOGGERS_TO_CONFIGURE = ["peewee", "httpx", "transitions", "urllib3"]

class ColoredFormatter(logging.Formatter):
    """Custom logging formatter with colors."""
    COLORS = {
        "DEBUG": "\x1b[38;5;39m",  # Blue
        "INFO": "\x1b[38;5;82m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m",  # Red
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{color}{super().format(record)}{self.COLORS['RESET']}"

def configure_logger(loggers: List[str] = None, level=logging.DEBUG):
    """Sets up logging with color output."""
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))

    if loggers is None:
        loggers = LOGGERS_TO_CONFIGURE

    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        logger.setLevel(level)

@click.group()
def cli():
    """Base CLI command group."""
    os.environ['PYTHONBREAKPOINT'] = 'IPython.terminal.debugger.set_trace'

@cli.command("shell")
@click.argument("ipython_args", nargs=-1, type=click.UNPROCESSED)
@click.option("--nolog", is_flag=True, default=False, help="Disable logging")
def shell(ipython_args, nolog):
    """Starts an interactive IPython shell."""
    profile_name = "cli_profile"
    ProfileDir.create_profile_dir_by_name(name=profile_name, path="./")

    if not nolog:
        configure_logger()

    # Set up IPython configuration
    config = load_default_config()
    config.TerminalInteractiveShell.banner1 = f"Python {sys.version} | IPython {IPython.__version__}"
    config.TerminalInteractiveShell.autoindent = True
    config.InteractiveShellApp.exec_lines = [
        "%load_ext autoreload",
        "%autoreload 2",
    ]
    config.TerminalInteractiveShell.autoformatter = "black"
    config.InteractiveShell.colors = "linux"
    config.TerminalInteractiveShell.highlighting_style = "monokai"  # Safe highlighting style

    # Start IPython shell
    user_ns = {}  # Define a clean namespace
    IPython.start_ipython(argv=ipython_args, user_ns=user_ns, config=config)

if __name__ == "__main__":
    cli()
