import ROOT

import logging
logger = logging.getLogger(__name__)


class Extractor:
    """Extract histograms from trees or chains (also splitted over multiple files).

    Attributes:
        extracted_histos (list): list of TH1 objects extracted from the source
        tchain (ROOT.TChain): chain built from a list of file containing the
            tree from which we want to extract histograms
        rdf (ROOT.RDataFrame): instance of RDataFrame used to get the results
    """
    def __init__(self):
        self.extracted_histos = []

    def get_histos_from_chain(self,
            path_to_base_dir, file_names, full_tree_name,
            output_file_name = None, variables = None, weights = None,
            normalize = False):
        """Get histograms from a set of files containing the same tree, e.g.:
            File1: path_to_base_dir/file_name_1/full_tree_name
            File2: path_to_base_dir/file_name_2/full_tree_name
            (...)
        The histograms can be generated with different models, depending on the
        arguments that are passed.

        Args:
            path_to_base_dir (str): full path to the directory that hosts the ROOT
                files on which we want to build the chain
            file_names (list): list of files in which the tree is splitted
            full_tree_name (str): full name of the tree contained in all the files
                (N.B.: 'full' mean that it contains also the eventual sub-TDirectoryFiles)
            output_file_name (str): name of the root file in which we want to save
                the extracted histograms
            variables (dict/list):
                dict: dictionary in the form {'var': binning_configuration}, where
                    binning_configuration can be either (nbins, list_of_edges) or
                    (nbins, low, up), a tuple in both cases
                list: list of the variables we want to extract
            weights (str): name of the column containing the weights we want to apply
            normalize (bool): decide if we want to normalize the histogram by dividing
                by the area
        """
        self.tchain = self._fill_and_get_tchain(path_to_base_dir,
                file_names, full_tree_name)
        self.rdf = self._build_rdf_get_results(self.tchain,
                output_file_name, variables, weights, normalize)

    def _fill_and_get_tchain(self,
            path_to_base_dir, file_names, full_tree_name):

        tchain = ROOT.TChain()

        for file_name in file_names:
            tchain.Add('{}/{}/{}'.format(path_to_base_dir,
                file_name, full_tree_name))

        return tchain

    def _build_rdf_get_results(self,
            tchain, output_file_name = None, variables = None,
            weights = None, normalize = False):

        ROOT.EnableImplicitMT()
        rdf = ROOT.RDataFrame(tchain)

        result_ptrs = []
        if isinstance(variables, dict):
            for var, binning in variables.items():
                if len(binning) == 2:
                    nbins, edges = binning
                    l_edges = ROOT.std.vector['double']()
                    for edge in edges:
                        l_edges.push_back(edge)
                    if weights:
                        histo_ptr = rdf.Histo1D((var, var, nbins, l_edges.data()),
                                var, weights)
                    else:
                        histo_ptr = rdf.Histo1D((var, var, nbins, l_edges.data()),
                                var)
                elif len(binning) == 3:
                    nbins, low, up = binning
                    if weights:
                        histo_ptr = rdf.Histo1D((var, var, nbins, low, up),
                                var, weights)
                    else:
                        histo_ptr = rdf.Histo1D((var, var, nbins, low, up),
                                var)
                result_ptrs.append(histo_ptr)

        elif isinstance(variables, list):
            for var in variables:
                histo_ptr = rdf.Histo1D(var)
                result_ptrs.append(histo_ptr)

        else:
            for var in rdf.GetColumnNames():
                histo_ptr = rdf.Histo1D(var)
                result_ptrs.append(histo_ptr)

        # Run event loop
        for ptr in result_ptrs:
            histo = ptr.GetValue()
            if normalize:
                histo.Scale(1 / histo.Integral())
            self.extracted_histos.append(histo)
        logger.info('Run event loop {} times'.format(rdf.GetNRuns()))

        # Write to file
        if output_file_name:
            f = ROOT.TFile(output_file_name, 'RECREATE')
            for histo in self.extracted_histos:
                histo.Write()
            f.Close()

        return rdf
