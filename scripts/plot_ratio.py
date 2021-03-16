#!/usr/bin/env python3
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Plot Data vs Simulation shapes and ratio plot"
            )

    parser.add_argument(
            "--config",
            required=True,
            type=str,
            help="JSON file with the configurations for each variable"
            )

    parser.add_argument(
            "--data_file",
            required=True,
            type=str,
            help="ROOT file containing data TTree"
            )

    parser.add_argument(
            "--data_tree",
            required=True,
            type=str,
            help="Name of TTree in data_file"
            )

    parser.add_argument(
            "--sim_file",
            required=True,
            type=str,
            help="ROOT file containing simulation TTree"
            )

    parser.add_argument(
            "--sim_tree",
            required=True,
            type=str,
            help="Name of TTree in sim_file"
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
    output_dir = args.output_dir

    with open(config) as input_file:
        config = json.load(input_file)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
