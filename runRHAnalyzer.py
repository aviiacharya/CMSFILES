import os

#cfg='RecHitAnalyzer/python/ConfFile_data_cfg.py'
cfg='/uscms_data/d3/aacharya/CMSSW_10_6_20/src/MLAnalyzer/RecHitAnalyzer/python/ConfFile_cfg.py'
#inputFiles_='file:/eos/uscms/store/group/lpcml/rchudasa/MCGeneration/DYToTauTau_M-50_13TeV-powheg_pythia8/DYToTauTau_M-50_13TeV-powheg_pythia8_DIGI-RECO-v2/230718_043012/0000/digiToReco_GluGluHtoTauTau_100.root' #QCD
#inputFiles_='file:/eos/cms/store/group/phys_heavyions/rchudasa/e2e/officialMC_DYJetsToLL_M-50_TuneCP5_13Tev_RECO/61F13245-CF73-9946-8321-B18051BB8659.root'#official MC
#inputFiles_='file:../PhaseI_TTbar_13TeV_NoPu_RECO_newGT.root'#pixel checks
#inputFiles_='file:/uscms/home/aacharya/nobackup/CMSSW_10_6_20/src/MLAnalyzer/0307C1DA-E49C-AB4B-9179-C70BE232321E.root' #Boosted_top_data_from_ana's_note
#inputFiles = 'file:/0307C1DA-E49C-AB4B-9179-C70BE232321E.root'
#inputFiles_ = 'file:/sim_TToHadronic_1kevents_2.root'
#inputFiles_ = 'file:/sim_TToHadronic_10events.root'
inputFiles_ = 'file:/sim_TToHadronic_1kevents_2.root'

maxEvents_=1000
#maxEvents_=20
#maxEvents_=-1
skipEvents_=0
#outputFile_='GJet.root'
outputFile_='RHA_TToHadronic_1000events.root'


cmd="cmsRun %s inputFiles=%s maxEvents=%d skipEvents=%d outputFile=%s"%(cfg,inputFiles_,maxEvents_,skipEvents_,outputFile_)
print '%s'%cmd
os.system(cmd)
