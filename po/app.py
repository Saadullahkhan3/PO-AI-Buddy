import os
import sys
# from .config import config
from ai import AI


AI_IDENTIFIER = "/ai"

if __name__ == "__main__":
    user_input = input("$ ")
    terminal = Terminal()   # Singleton instance
    if user_input.startswith(AI_IDENTIFIER):
        with SmartTerminal() as smart:
            smart.repl()    # REPL, also store context
    else:
        terminal.run_cmd(user_input)
    