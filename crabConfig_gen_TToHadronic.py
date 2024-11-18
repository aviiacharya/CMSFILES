from CRABClient.UserUtilities import config
config = config()
# See parameter defintions here: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile#CRAB_configuration_parameters

CFG = 'gen_TToHadronic_m172To175_pT100To300_etam2p5To2p5_local'

# To submit to crab:
# crab submit -c crabConfig_data.py
# To check job status:
# crab status -d <config.General.workArea>/<config.General.requestName>
# To resubmit jobs:
# crab resubmit -d <config.General.workArea>/<config.General.requestName>

# Local job directory will be created in:
# <config.General.workArea>/<config.General.requestName>
config.General.workArea = 'Gen_TToHadronic_10M'
config.General.requestName = 'gen_TToHadronic_m172To175_pT100To300_etam2p5To2p5_local'
config.General.transferOutputs = True
config.General.transferLogs = False

# CMS cfg file goes here:
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%s.py'%(CFG) # cms cfg file for generating events
#config.JobType.maxMemoryMB = 1000

# Define units per job here:
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000   # units: as defined by config.Data.splitting
NJOBS = 10000
config.Data.totalUnits  = config.Data.unitsPerJob * NJOBS   # total jobs submitted = totalUnits / unitsPerJob. cap of 10k jobs per submission
config.Data.publication = True #Check the link

# Output files will be stored in config.Site.storageSite at directory:
# <config.Data.outLFNDirBase>/<config.Data.outputPrimaryDataset>/<config.Data.outputDatasetTag>/
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.storageSite = 'T2_CH_CERN'
config.Data.outLFNDirBase = '/store/user/abachary' # add your username as subdirectory
config.Data.outputPrimaryDataset = 'gen_TToHadronic_10Mevents'
config.Data.outputDatasetTag = config.General.requestName
