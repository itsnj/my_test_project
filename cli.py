import click
import os
from IPython.terminal.ipapp import load_default_config
import sys
import IPython
# from tortoise import Tortoise
# from tortoise.transactions import in_transaction
# from app.core.database import TORTOISE_ORM  # Your Tortoise ORM configuration
import asyncio

# Helper function to run async commands in Click
def async_command(coro):
    def wrapper(*args, **kwargs):
        return asyncio.run(coro(*args, **kwargs))
    return wrapper

@click.group()
def cli():
    os.environ['PYTHONBREAKPOINT'] = 'IPython.terminal.debugger.set_trace'

@cli.command(name="shell")
@click.argument("ipython_args", nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    """Start an IPython shell with the database initialized."""
    
    # IPython configuration
    profile_name = "test projec"
    config = load_default_config()
    config.TerminalInteractiveShell.banner1 = (
        f"""Python {sys.version} on {sys.platform} IPython: {IPython.__version__}"""
    )
    config.TerminalInteractiveShell.autoindent = True
    config.InteractiveShellApp.exec_lines = [
        "%load_ext autoreload",
        "%autoreload 2",
    ]
    config.TerminalInteractiveShell.autoformatter = "black"
    config.TerminalInteractiveShell.highlighting_style = "paraiso-dark"
    config.TerminalIPythonApp.profile = profile_name

    # Initialize the database connection
    # asyncio.run(Tortoise.init(config=TORTOISE_ORM))
    
    # Create a user namespace with the database connection
    # user_ns = {"Tortoise": Tortoise}
    
    # Start the IPython shell with the custom user namespace
    try:
        # Use async context to ensure proper database transaction handling
        # db = in_transaction()
        # user_ns["db"] = db
        # Initialize the IPython app and run it
        ipython = IPython.terminal.ipapp.TerminalIPythonApp.instance()
        ipython.config = config
        # ipython.user_ns = user_ns
        ipython.initialize(argv=ipython_args)
        ipython.start()
    finally:
        print("Closed")
        # Ensure proper cleanup of database connections
        # asyncio.run(Tortoise.close_connections())



if __name__ == '__main__':
    # Run the Click CLI with asynchronous support
    cli()