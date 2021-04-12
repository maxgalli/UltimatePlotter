import ROOT
from ROOT import TFile, TTree
from array import array

data_file = TFile( 'data.root', 'recreate' )
data_tree = TTree( 'Events', 'Events' )

mass = array( 'd', [ 0. ] )
pt = array( 'd', [ 0. ] )
data_tree.Branch( 'mass', mass, 'mass/D' )
data_tree.Branch( 'pt', pt, 'pt/D' )

for i in range(100000):
   mass[0] = ROOT.gRandom.Gaus(60,10)
   pt[0] = ROOT.gRandom.Exp(2)
   data_tree.Fill()

data_file.Write()
data_file.Close()


mc1_file = TFile( 'mc1.root', 'recreate' )
mc1_tree = TTree( 'Events', 'Events' )

mass = array( 'd', [ 0. ] )
pt = array( 'd', [ 0. ] )
mc1_tree.Branch( 'mass', mass, 'mass/D' )
mc1_tree.Branch( 'pt', pt, 'pt/D' )

for i in range(50000):
   mass[0] = ROOT.gRandom.Gaus(58,15)
   pt[0] = ROOT.gRandom.Exp(2.4)
   mc1_tree.Fill()

mc1_file.Write()
mc1_file.Close()


mc2_file = TFile( 'mc2.root', 'recreate' )
mc2_tree = TTree( 'Events', 'Events' )

mass = array( 'd', [ 0. ] )
pt = array( 'd', [ 0. ] )
mc2_tree.Branch( 'mass', mass, 'mass/D' )
mc2_tree.Branch( 'pt', pt, 'pt/D' )

for i in range(30000):
   mass[0] = ROOT.gRandom.Gaus(59.4,17)
   pt[0] = ROOT.gRandom.Exp(2.1)
   mc2_tree.Fill()

mc2_file.Write()
mc2_file.Close()
