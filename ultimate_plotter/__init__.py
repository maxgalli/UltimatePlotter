from .plots import BasicPlot
from .plots import DataSimulationPlot
from .parser import universal_parser

import logging

def setup_logging(level=logging.INFO):
    from rich.logging import RichHandler
    from rich.console import Console

    logger = logging.getLogger()

    logger.setLevel(level)
    formatter = logging.Formatter("%(message)s")

    stream_handler = RichHandler(show_time=False, rich_tracebacks=True)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
