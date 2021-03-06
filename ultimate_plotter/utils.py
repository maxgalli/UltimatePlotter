import uproot
import awkward as ak
from rich.logging import RichHandler
from rich.console import Console

import logging
logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()

    logger.setLevel(level)
    formatter = logging.Formatter("%(message)s")

    stream_handler = RichHandler(show_time=False, rich_tracebacks=True)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def extract(input_file, tree_name, variables=None):
    logger.info("Extracting dataframe from {}:{}".format(input_file, tree_name))

    f = uproot.open(input_file)
    tree = f[tree_name]
    df = tree.arrays(variables)

    return df


def extract_batches(input_files, tree_name, variables=None):
    logger.info("Creating generator using uproot.iterate for input files {}".format(input_files))

    inputs = ["{}:{}".format(fl, tree_name) for fl in input_files]
    generator = uproot.iterate(inputs, expressions=variables)

    return generator
