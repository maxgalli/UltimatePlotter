#!/usr/bin/env python3
import argparse

from ultimate_plotter import BasicPlot
from ultimate_plotter import setup_logging
from ultimate_plotter import universal_parser


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

    parser.add_argument(
            "--pkl_output",
            required=False,
            type=str,
            default="output",
            help="Pickle file in which information used to make the plots are dumped"
            )

    return parser.parse_args()


def main(args):
    config = args.config
    input_file = args.input_file
    tree_name = args.tree_name
    output_dir = args.output_dir
    pkl_output = args.pkl_output

    config = universal_parser(config)

    plotter = BasicPlot(input_file, tree_name, **config)
    plotter.draw(output_dir)
    plotter.dump_info(output_dir, pkl_output)


if __name__ == "__main__":
    logger = setup_logging()
    args = parse_arguments()
    main(args)
