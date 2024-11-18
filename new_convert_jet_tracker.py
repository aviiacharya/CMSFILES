import pyarrow.parquet as pq
import pyarrow as pa
import ROOT
import numpy as np
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', '--input_list', default='NTUPLES1_list.txt', type=str, help='Input list of root filenames.')
parser.add_argument('-o', '--outdir', default='.', type=str, help='Output pq file dir.')
parser.add_argument('-d', '--decay', default='test', type=str, help='Decay name.')
parser.add_argument('-n', '--idx', default=0, type=int, help='Input root file index.')
args = parser.parse_args()

# Function to crop the jet area based on iphi and ieta
def crop_jet(imgECAL, iphi, ieta, jet_shape=125):
    off = jet_shape // 2
    iphi = int(iphi * 5 + 2)  # 5 EB xtals per HB tower
    ieta = int(ieta * 5 + 2)  # 5 EB xtals per HB tower

    if iphi < off:
        diff = off - iphi
        img_crop = np.concatenate((imgECAL[:, ieta - off: ieta + off + 1, -diff:],
                                   imgECAL[:, ieta - off: ieta + off + 1, :iphi + off + 1]), axis=-1)
    elif 360 - iphi < off:
        diff = off - (360 - iphi)
        img_crop = np.concatenate((imgECAL[:, ieta - off: ieta + off + 1, iphi - off:],
                                   imgECAL[:, ieta - off: ieta + off + 1, :diff + 1]), axis=-1)
    else:
        img_crop = imgECAL[:, ieta - off: ieta + off + 1, iphi - off: iphi + off + 1]

    return img_crop

# Read file list
files = []
with open(args.input_list, "r") as filelist:
    filenames = filelist.readlines()
    for filename in filenames:
        files.append(filename.strip())

print(files)

# Open ROOT files
rhTree = ROOT.TChain("fevt/RHTree")
for filename in files:
    rhTree.Add(filename)

nEvts = rhTree.GetEntries()
assert nEvts > 0
print(" >> nEvts:", nEvts)
outStr = '%s/%s.parquet.%d' % (args.outdir, args.decay, args.idx)
print(" >> Output file:", outStr)

##### MAIN #####
iEvtStart = 0
iEvtEnd = nEvts
assert iEvtEnd <= nEvts
print(" >> Processing entries: [", iEvtStart, "->", iEvtEnd, ")")

nJets = 0
data = {}
sw = ROOT.TStopwatch()
sw.Start()

for iEvt in range(iEvtStart, iEvtEnd):
    rhTree.GetEntry(iEvt)
    
    if iEvt % 100 == 0:
        print(" .. Processing entry", iEvt)

    # Load ECAL and tracking data as reco-level
    ECAL_energy = np.array(rhTree.ECAL_energy).reshape(280, 360)
    HBHE_energy = np.array(rhTree.HBHE_energy).reshape(56, 72)
    HBHE_energy = np.kron(HBHE_energy, np.ones((5, 5)))
    TracksAtECAL_pt = np.array(rhTree.ECAL_tracksPt_atECALfixIP).reshape(280, 360)
    TracksAtECAL_dZSig = np.array(rhTree.ECAL_tracksDzSig_atECALfixIP).reshape(280, 360)
    TracksAtECAL_d0Sig = np.array(rhTree.ECAL_tracksD0Sig_atECALfixIP).reshape(280, 360)
    PixAtEcal_1 = np.array(rhTree.BPIX_layer1_ECAL_atPV).reshape(280, 360)
    PixAtEcal_2 = np.array(rhTree.BPIX_layer2_ECAL_atPV).reshape(280, 360)
    PixAtEcal_3 = np.array(rhTree.BPIX_layer3_ECAL_atPV).reshape(280, 360)
    PixAtEcal_4 = np.array(rhTree.BPIX_layer4_ECAL_atPV).reshape(280, 360)
    TibAtEcal_1 = np.array(rhTree.TIB_layer1_ECAL_atPV).reshape(280, 360)
    TibAtEcal_2 = np.array(rhTree.TIB_layer2_ECAL_atPV).reshape(280, 360)
    TobAtEcal_1 = np.array(rhTree.TOB_layer1_ECAL_atPV).reshape(280, 360)
    TobAtEcal_2 = np.array(rhTree.TOB_layer2_ECAL_atPV).reshape(280, 360)

    # Stack as a reco-level X_CMSII dataset
    X_CMSII_reco = np.stack([TracksAtECAL_pt, TracksAtECAL_dZSig, TracksAtECAL_d0Sig, ECAL_energy,HBHE_energy,
                             PixAtEcal_1, PixAtEcal_2, PixAtEcal_3, PixAtEcal_4,
                             TibAtEcal_1, TibAtEcal_2, TobAtEcal_1, TobAtEcal_2], axis=0)

    # Load jet attributes
    goodvertices = rhTree.goodvertices
    jet_pt = rhTree.jet_Pt
    #jet_eta = rhTree.jet_Eta
    jet_phi = rhTree.jet_Phi
    jet_energy = rhTree.jet_Energy
    jet_m0 = rhTree.jet_m0
    #jet_dR = rhTree.jet_dR
    #jet_M = rhTree.jet_M

    # Generation-level and reco-level top attributes
    gen_top_mass = rhTree.gen_top_mass
    gen_top_pt = rhTree.gen_top_pt
    gen_top_eta = rhTree.gen_top_eta
    gen_top_phi = rhTree.gen_top_phi
    reco_top_mass = rhTree.reco_top_mass
    reco_top_pt = rhTree.reco_top_pt
    reco_top_eta = rhTree.reco_top_eta
    reco_top_phi = rhTree.reco_top_phi

    njets = len(goodvertices)

    for i in range(njets):
        # Store jet and top-level attributes
        data['goodvertices'] = goodvertices[i]
        data['jet_pt'] = jet_pt[i]
        #data['jet_eta'] = jet_eta[i]
        data['jet_phi'] = jet_phi[i]
        data['jet_energy'] = jet_energy[i]
        data['jet_m0'] = jet_m0[i]
        #data['jet_dR'] = jet_dR[i]
        #data['jet_M'] = jet_M[i]

        # Generation-level top quark properties
        data['gen_top_mass'] = gen_top_mass[i]
        data['gen_top_pt'] = gen_top_pt[i]
        data['gen_top_eta'] = gen_top_eta[i]
        data['gen_top_phi'] = gen_top_phi[i]

        # Reco-level top quark properties
        data['reco_top_mass'] = reco_top_mass[i]
        data['reco_top_pt'] = reco_top_pt[i]
        data['reco_top_eta'] = reco_top_eta[i]
        data['reco_top_phi'] = reco_top_phi[i]

        # Crop jet data based on reco-level phi and eta
        data['X_jet'] = crop_jet(X_CMSII_reco, data['reco_top_phi'], data['reco_top_eta'])#convert to ieta iphi

        # Create pyarrow.Table for each jet entry
        pqdata = [pa.array([d]) if (np.isscalar(d) or isinstance(d, list)) else pa.array([d.tolist()]) for d in data.values()]
        table = pa.Table.from_arrays(pqdata, data.keys())
        
        # Write table to Parquet file
        if nJets == 0:
            writer = pq.ParquetWriter(outStr, table.schema, compression='snappy')
        writer.write_table(table)

        nJets += 1

writer.close()
print(" >> nJets:", nJets)
print(" >> Real time:", sw.RealTime() / 60., "minutes")
print(" >> CPU time: ", sw.CpuTime() / 60., "minutes")
print("========================================================")

# Verify output file
pqIn = pq.ParquetFile(outStr)
print(pqIn.metadata)
print(pqIn.schema)
X = pqIn.read_row_group(0, columns=['goodvertices', 'reco_top_mass', 'reco_top_phi', 'reco_top_eta']).to_pydict()
print(X)
print("Finished conversion")

