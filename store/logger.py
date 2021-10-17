import sys
import logging
from pythonjsonlogger import jsonlogger

# logging.basicConfig(
#     stream=sys.stderr,
#     level=logging.getLevelName(logging.DEBUG),
#     format="%(asctime)s\t[%(levelname)s]\t%(message)s")

class AppLogger(logging.Logger):

    def __init__(self, name: str, level = ...) -> None:
        super().__init__(name, level=logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        handler.setFormatter(formatter)
        self.addHandler(handler)
        