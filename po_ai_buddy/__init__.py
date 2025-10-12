import sys
from types import TracebackType



__version__: str = "0.1.7"


# Global exception handler to catch KeyboardInterrupt
def my_except_hook(exctype: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
    if exctype == KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    else:
        sys.__excepthook__(exctype, value, traceback)


sys.excepthook = my_except_hook


from .main import main 

