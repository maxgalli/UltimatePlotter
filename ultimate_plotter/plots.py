import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import pickle

hep.set_style("CMS")

import logging
import logging
logger = logging.getLogger(__name__)



class BasicPlot:
    """Configure a plotter that dumps one single shape per variable.
    The method 'draw_single_variable' produces histograms for only one variable, while
    'draw' produces histograms for all the variables specified in variables_specs

    Attributes:
        input_file (string): ROOT file storing the TTree containing the variables we want to print
        tree_name (string): name of the TTree containing the variables we are interested in
        variables_specs (list of dictionaries): every dictionary in the list contains the configuration
            for a variable that we want to show; the main keys are the following:
                name: name of the variable in the TTree
                bins: number of bins
                range: list containing min and max
                plot_name: variable name we want to show in the plot
        cuts (list): list of cuts we want to apply to all the variables
    """
    def __init__(self, input_file, tree_name, variables_specs=None, cuts=None):
        self.input_file = input_file
        self.tree_name = tree_name
        if not variables_specs:
            self.variables_specs = []
        else:
            self.variables_specs = variables_specs
        if not cuts:
            self.cuts = []
        else:
            self.cuts = cuts
        self.df = self.extract(self.input_file, self.tree_name)
        self.df = self.apply_cuts(self.df, self.cuts)


    def extract(self, input_file, tree_name, variables=None):
        logger.info("Extracting dataframe from {}:{}".format(input_file, tree_name))
        if self.variables_specs:
            variables = [var["name"] for var in self.variables_specs]
        f = uproot.open(input_file)
        tree = f[tree_name]
        df = tree.arrays(variables, library="pd")
        return df


    def apply_cuts(self, df, cuts):
        for cut in cuts:
            df = df.query(cut)
        return df


    def draw_single_variable(self, output_dir, name, bins=None, range=None, plot_name=None, color=None):
        # 'name' is the name of the variable found in the TTree
        # 'plot_name' is the name we want to plot on the axis and in the title
        if not plot_name:
            plot_name = name

        if bins and range:
            output_name = "_".join([name, "{}bins".format(str(bins)), *map(str, range)])
        else:
            output_name = name

        if not color:
            color = "deepskyblue"

        logger.info("Drawing plot for variable {}".format(name))

        fig, ax = plt.subplots()

        plt.hist(self.df[name], bins=bins, range=range, density=True, label=plot_name, histtype="stepfilled", color=color, edgecolor="black")

        hep.cms.label(loc=0, data=True, llabel="Work in Progress", rlabel="")
        ax.set_xlabel(plot_name, loc="center")
        ax.legend(fontsize=16)

        fig.savefig("{}/{}.pdf".format(output_dir, output_name), bbox_inches='tight')
        fig.savefig("{}/{}.png".format(output_dir, output_name), bbox_inches='tight')


    def draw(self, output_dir):
        for var_spec in self.variables_specs:
            self.draw_single_variable(output_dir, **var_spec)

        logger.info("Output saved in {}".format(output_dir))


    def dump_info(self, output_dir, pkl_output):
        output_name = '/'.join([output_dir, "{}.pkl".format(pkl_output)])
        logger.info("Dumping config information to {}".format(output_name))

        to_dump = {}
        to_dump["plot_type"] = self.__class__.__name__
        to_dump["variables_specs"] = self.variables_specs
        to_dump["cuts"] = self.cuts
        to_dump["source_file"] = self.input_file
        to_dump["source_tree"] = self.tree_name

        with open(output_name, "wb") as f:
            pickle.dump(to_dump, f)



class DataSimulationPlot(BasicPlot):
    def __init__(self, data_file, data_tree, sim_file, sim_tree, variables_specs=None, cuts=None):
        self.data_file = data_file
        self.data_tree = data_tree
        self.sim_file = sim_file
        self.sim_tree = sim_tree

        if not variables_specs:
            self.variables_specs = []
        else:
            self.variables_specs = variables_specs
        if not cuts:
            self.cuts = []
        else:
            self.cuts = cuts

        self.df_data = self.extract(self.data_file, self.data_tree)
        self.df_data = self.apply_cuts(self.df_data, self.cuts)
        self.df_sim = self.extract(self.sim_file, self.sim_tree)
        self.df_sim = self.apply_cuts(self.df_sim, self.cuts)


    def draw_single_variable(self, output_dir, name, bins=None, range=None, plot_name=None, color=None):
        # 'name' is the name of the variable found in the TTree
        # 'plot_name' is the name we want to plot on the axis and in the title
        if not plot_name:
            plot_name = name

        if bins and range:
            output_name = "_".join([name, "{}bins".format(str(bins)), *map(str, range)])
        else:
            output_name = name

        if not color:
            color = "deepskyblue"

        logger.info("Drawing plot for variable {}".format(name))

        fig, ax = plt.subplots()

        # Plot data
        # Data is always plot as black dots
        dcentres, dcounts = self._histo_to_dots(self.df_data, name, bins, range)
        plt.plot(dcentres, dcounts, "k.")

        # Plot sim
        plt.hist(self.df_sim[name], bins=bins, range=range, density=True, label=plot_name, histtype="step", edgecolor=color, linewidth=2.)

        hep.cms.label(loc=0, data=True, llabel="Work in Progress", rlabel="")
        ax.set_xlabel(plot_name, loc="center")
        ax.legend(fontsize=16)

        fig.savefig("{}/{}.pdf".format(output_dir, output_name), bbox_inches='tight')
        fig.savefig("{}/{}.png".format(output_dir, output_name), bbox_inches='tight')


    def dump_info(self, output_dir, pkl_output):
        output_name = '/'.join([output_dir, "{}.pkl".format(pkl_output)])
        logger.info("Dumping config information to {}".format(output_name))

        to_dump = {}
        to_dump["plot_type"] = self.__class__.__name__
        to_dump["variables_specs"] = self.variables_specs
        to_dump["cuts"] = self.cuts
        to_dump["data_source_file"] = self.data_file
        to_dump["data_source_tree"] = self.data_tree
        to_dump["simulation_source_file"] = self.sim_file
        to_dump["simulation_source_tree"] = self.sim_tree

        with open(output_name, "wb") as f:
            pickle.dump(to_dump, f)


    def _histo_to_dots(self, dataframe, var, bins, range):
        dcounts, dedges, patch = plt.hist(dataframe[var], bins=bins, range=range, density=True, alpha=0.0, histtype="step", edgecolor="black")
        dcentres = (dedges[:-1] + dedges[1:]) / 2.
        return dcentres, dcounts
