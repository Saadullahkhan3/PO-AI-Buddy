import sys

__version__ = "0.1.4"


# Global exception handler to catch KeyboardInterrupt
def my_except_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    else:
        sys.__excepthook__(exctype, value, traceback)

sys.excepthook = my_except_hook


from .main import main 

