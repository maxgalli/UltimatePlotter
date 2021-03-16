#!/usr/bin/env python3
import json
import argparse

from ultimate_plotter import BasicPlot
from ultimate_plotter import setup_logging


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Plot variables distributions from an input file"
            )

    parser.add_argument(
            "--config",
            required=True,
            type=str,
            help="JSON file with the configurations for each variable"
            )

    parser.add_argument(
            "--input_file",
            required=True,
            type=str,
            help="Input ROOT file"
            )

    parser.add_argument(
            "--tree_name",
            required=True,
            type=str,
            help="Name of TTree in input_file"
            )

    parser.add_argument(
            "--output_dir",
            required=True,
            type=str,
            help="Output directory"
            )

    return parser.parse_args()


def main(args):
    config = args.config
    input_file = args.input_file
    tree_name = args.tree_name
    output_dir = args.output_dir

    with open(config) as f:
        config = json.load(f)

    plotter = BasicPlot(config, input_file, tree_name)
    plotter.draw(output_dir)


if __name__ == "__main__":
    logger = setup_logging()
    args = parse_arguments()
    main(args)
