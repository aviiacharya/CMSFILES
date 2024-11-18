from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
config = config()
# See parameter defintions here: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile#CRAB_configuration_parameters

#idx = '00000'
CFG = 'RHA_TToHadronic_m100To300_pT170To175_etam2p5To2p5_pythia8'

# To submit to crab:
# crab submit -c crabConfig_data.py
# To check job status:
# crab status -d <config.General.workArea>/<config.General.requestName># To resubmit jobs:
# crab resubmit -d <config.General.workArea>/<config.General.requestName>

# Local job directory will be created in:
# <config.General.workArea>/<config.General.requestName>
config.General.workArea = 'crab_MC'
config.General.requestName = CFG
config.General.transferOutputs = True
config.General.transferLogs = False

# CMS cfg file goes here:
#config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'MLAnalyzer/RecHitAnalyzer/python/ConfFile_cfg.py' # analyzer cfg file
config.JobType.maxMemoryMB = 5000 


# Define input and units per job here:
config.Data.userInputFiles = open('SIM_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1 # units: as defined by config.Data.splitting
config.Data.totalUnits = -1 # -1: all inputs. total jobs submitted = totalUnits / unitsPerJob. cap of 10k jobs per submission
#config.Data.totalUnits = 10 # test production
config.Data.publication = False
#config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'

# Output files will be stored in config.Site.storageSite at directory:
# <config.Data.outLFNDirBase>/<config.Data.outputPrimaryDataset>/<config.Data.outputDatasetTag>/
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = '/store/user/abachary/' # add your username as subdirectory
config.Data.outputPrimaryDataset = 'RHA_TToHadronic_10kevents'
config.Data.outputDatasetTag = config.General.requestName
