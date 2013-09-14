from listener import Listener
from interpreter import *
from commands import Command
from commands.say import SayCommand, sayTime
from commands.open_door import OpenDoorCommand
from commands.set_alarm import AbsoluteAlarmCommand, RelativeAlarmCommand
from commands.activate import ActivateCommand
from commands.deactivate import DeactivateCommand
from commands.account_balance import AccountBalanceCommand, say_balance
from commands.next_bus import NextBusCommand
from commands.dinner import DinnerCommand
from apscheduler.scheduler import Scheduler
import os

def main():
    """
    Allows Winston to be installed as a package and run from the command line
    """

    # This file can be called from the command line, and will run Winston
    # The grammar.fsg is a finite state grammar file generated from jsgf.txt
    # using sphinx_jsgf2fsg. It helps the listener associate words to the correct
    # commands. 
    script_path = os.path.dirname(__file__)
    grammar_file = os.path.join(script_path, "grammar.fsg")
    dict_file = os.path.join(script_path, "dict.dic")

    # The list of commands passed to the interpreter
    commands = [
        # Commands defined by extending the Command object. These are a few examples.
        SayCommand(),  # Simple command to get started
        ActivateCommand(),  # Can activate winston
        DeactivateCommand(),  # Can deactivate winston
        AccountBalanceCommand(),  # Lots of variation, uses regex actions
        OpenDoorCommand(),
        AbsoluteAlarmCommand(),
        RelativeAlarmCommand(),
        NextBusCommand(),
        DinnerCommand(),
    ]

    # A command defined by instanciating the Command object
    commands.append(Command(name='whatTime', actions=('what time is it',), callback=sayTime))

    # Define and start a scheduler. These store tasks that are run at given times
    scheduler = Scheduler()
    scheduler.start()
    scheduler.add_cron_job(say_balance, hour=18, minute=00)  # Reads the account balance at 17:30, daily

    # Load the commands in the interpreter
    interpreter = Interpreter(commands=commands, scheduler=scheduler)

    # Get a listener. The grammar argument is optional, see Listener's doc for details
    listener = Listener(interpreters=[interpreter], fsg_path=grammar_file, dict_path=dict_file)

    # And wait...
    raw_input()

if __name__ == "__main__":
    main()