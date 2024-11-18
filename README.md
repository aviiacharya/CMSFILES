## The process as follows.
- - To generate the data sample, I use ![this](https://github.com/aviiacharya/CMSFiles/blob/main/gen_TToHadronic_m172To175_pT100To300_etam2p5To2p5_local.py) script and use ![these](https://github.com/aviiacharya/CMSFiles/blob/main/GeneratorInterface/GenFilters/plugins/GenTToHadronicFilter.cc) ![2](https://github.com/aviiacharya/CMSFiles/blob/main/GeneratorInterface/Pythia8Interface/plugins/Py8PtGunV3.cc) plugin files as a filter and generator . Respective changes needed as per requirement of your data generation.
- - Next is to take the root file and process them through the ![simulation script](https://github.com/aviiacharya/CMSFiles/blob/main/sim_TToHadronic_m170to175_pT100To300_etam2p5To2p5_pythia8.py).
  - 
