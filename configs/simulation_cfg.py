import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

import argparse

parser = argparse.ArgumentParser(description='AOD2NanoTool')
parser.add_argument(
    '--numEvents',
    action="store",
    type=int,
    help="Number of events to process",
    default=-1,
)
args = parser.parse_args(sys.argv[1:])



process = cms.Process("AOD2NanoAOD")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = "WARNING"
process.MessageLogger.categories.append("AOD2NanoAOD")
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit=cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

# Set the maximum number of events to be processed (-1 processes all events)
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(args.numEvents))

# Define files of dataset
files = FileUtils.loadListFromFile("data/CMS_MonteCarlo2012_Summer12_DR53X_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_AODSIM_PU_RD1_START53_V7N-v1_20000_file_index.txt")
#files.extend(FileUtils.loadListFromFile("data/CMS_MonteCarlo2012_Summer12_DR53X_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_AODSIM_PU_RD1_START53_V7N-v1_20001_file_index.txt"))
#files.extend(FileUtils.loadListFromFile("data/CMS_MonteCarlo2012_Summer12_DR53X_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_AODSIM_PU_RD1_START53_V7N-v1_20002_file_index.txt"))


process.source = cms.Source(
    "PoolSource", fileNames=cms.untracked.vstring(*files))

# Set global tag
# We don't have set the global tag for the educational samples. This simplifies running the code since we don't have to access the database.
#process.GlobalTag.globaltag = "START53_V27::All"

# Number of events to be skipped (0 by default)
process.source.skipEvents = cms.untracked.uint32(0)

# Register fileservice for output file
process.aod2nanoaod = cms.EDAnalyzer("AOD2NanoAOD", isData = cms.bool(False))
process.TFileService = cms.Service(
    "TFileService", fileName=cms.string("output.root"))

process.p = cms.Path(process.aod2nanoaod)
