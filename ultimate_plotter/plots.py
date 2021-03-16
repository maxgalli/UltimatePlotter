import uproot
import matplotlib.pyplot as plt

import logging
import logging
logger = logging.getLogger(__name__)


class BasicPlot:
    def __init__(self, config, input_file, tree_name):
        self.config = config
        self.df = self.extract(input_file, tree_name)

    def extract(self, input_file, tree_name):
        logger.info("Extracting dataframe from {}:{}".format(input_file, tree_name))
        variables = [var["name"] for var in self.config["variables"]]
        f = uproot.open(input_file)
        tree = f[tree_name]
        df = tree.arrays(variables, library="pd")
        return df

    def draw(self, output_dir):
        for var in self.config["variables"]:
            name = var["name"]
            bins = var["bins"]
            rng = var["range"]

            output_name = "_".join([name, str(bins), *map(str, rng)])

            logger.info("Drawing plot for variable {}".format(name))

            fig, ax = plt.subplots()

            plt.hist(self.df[name], bins=bins, range=rng, density=True)

            fig.savefig("{}/{}.pdf".format(output_dir, output_name))
            fig.savefig("{}/{}.png".format(output_dir, output_name))

        logger.info("Output saved in {}".format(output_dir))


class RatioPlot(BasicPlot):
    def __init__(self, ):
        pass
