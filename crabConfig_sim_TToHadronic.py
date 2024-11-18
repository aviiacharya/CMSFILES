from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
config = config()
# See parameter defintions here: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile#CRAB_configuration_parameters

CFG = 'sim_TToHadronic_m170to175_pT100To300_etam2p5To2p5_pythia8'

# To submit to crab:
# crab submit -c crabConfig_data.py
# To check job status:
# crab status -d <config.General.workArea>/<config.General.requestName># To resubmit jobs:
# crab resubmit -d <config.General.workArea>/<config.General.requestName>

# Local job directory will be created in:
# <config.General.workArea>/<config.General.requestName>
config.General.workArea = 'crab_sim'
config.General.requestName = CFG
config.General.transferOutputs = True
config.General.transferLogs = False

# CMS cfg file goes here:
#config.JobType.pluginName = 'PrivateMC'
#config.JobType.psetName = '%s.py'%(CFG) # cms c

# CMS cfg file goes here:
config.JobType.psetName = './sim_TToHadronic_m170to175_pT100To300_etam2p5To2p5_pythia8.py' # analyzer cfg file
#config.JobType.maxMemoryMB = 1250      #1200   #2500
#config.JobType.maxJobRuntimeMin = 500
config.JobType.maxMemoryMB = 5000

# Define input and units per job here:
config.Data.userInputFiles = open('./GEN_list.txt').readlines()
#config.Data.userInputFiles = 'gen_TToHadronic_1000events.root'
config.Data.splitting = 'FileBased'# 'Automatic'
#config.JobType.pluginName  = 'Analysis'
config.Data.unitsPerJob = 1 # units: as defined by config.Data.splitting
config.Data.totalUnits =  -1 # -1: all inputs. total jobs submitted = totalUnits / unitsPerJob. cap of 10k jobs per submission
#config.Data.totalUnits = 10 # test production
config.Data.publication = False

# Output files will be stored in config.Site.storageSite at directory:
# <config.Data.outLFNDirBase>/<config.Data.outputPrimaryDataset>/<config.Data.outputDatasetTag>/
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = '/store/user/abachary' # add your username as subdirectory
config.Data.outputPrimaryDataset = 'sim_TToHadronic_events10k'
config.Data.outputDatasetTag = config.General.requestName
