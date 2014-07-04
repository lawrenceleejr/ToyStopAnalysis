#!/usr/bin/env python

import os,sys,subprocess,datetime,copy,math,array,shutil,ROOT

__author__ = "Renaud Bruneliere <Renaud.Bruneliere@cern.ch>"
__doc__    = """
Python script used to run on SUSY D3PDs. At the moment it mimics cuts from 2010 1-lepton analysis.
Usage: 
chmod u+x susycutflow_1lep.py
./susycutflow_1lep.py --help
./susycutflow_1lep.py
"""
 
fdefault = ['/eos/atlas/user/a/amarzin/p1319/NTUP_SUSY.01085272._000001.root.1']

def parseCmdLine(args): 
	""" Parse input command line to optdict.
	To get the whole list of options type : susycutflow_1lep.py -h"""
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("--infile", dest="infile", help="Input file",default='default') 
	parser.add_option("--isdata", dest="isdata", help="Data or Monte Carlo ?",
					  action='store_true', default=False) 
	parser.add_option("--stream", dest="stream", help="Data stream",default='Muons') 
	parser.add_option("--trgwgt", dest="trgwgt", help="Apply a data-driven weight to emulate trigger in MC ?",
					  action='store_true', default=False)
	parser.add_option("--PUwgt", dest="PUwgt", help="Apply pileup reweighting to MC ?",
					  action='store_true', default=False)
	parser.add_option("--atlfast", dest="atlfast", help="Is Atlfast II?",
					  action='store_true', default=False)
	parser.add_option("--jesup", dest="jesup", help="Rescale jet energy scale by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesdown", dest="jesdown", help="Rescale jet energy scale by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_1_Up", dest="jesEffectiveNP_1_Up", help="Rescale effective JES Uncertainty Component 1 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_1_Down", dest="jesEffectiveNP_1_Down", help="Rescale effective JES Uncertainty Component 1 by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_2_Up", dest="jesEffectiveNP_2_Up", help="Rescale effective JES Uncertainty Component 2 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_2_Down", dest="jesEffectiveNP_2_Down", help="Rescale effective JES Uncertainty Component 2 by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_3_Up", dest="jesEffectiveNP_3_Up", help="Rescale effective JES Uncertainty Component 3 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_3_Down", dest="jesEffectiveNP_3_Down", help="Rescale effective JES Uncertainty Component 3 by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_4_Up", dest="jesEffectiveNP_4_Up", help="Rescale effective JES Uncertainty Component 4 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_4_Down", dest="jesEffectiveNP_4_Down", help="Rescale effective JES Uncertainty Component 4 by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_5_Up", dest="jesEffectiveNP_5_Up", help="Rescale effective JES Uncertainty Component 5 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_5_Down", dest="jesEffectiveNP_5_Down", help="Rescale effective JES Uncertainty Component 5 by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_6_Up", dest="jesEffectiveNP_6_Up", help="Rescale effective JES Uncertainty Component 6 by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEffectiveNP_6_Down", dest="jesEffectiveNP_6_Down", help="Rescale effective JES Uncertainty Component 6 by -1 sigma",
					  action='store_true', default=False)    
	parser.add_option("--jesEtaIntercalibration_Modelling_Up", dest="jesEtaIntercalibration_Modelling_Up", help="Rescale JES MC generator modelling uncertainty by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEtaIntercalibration_Modelling_Down", dest="jesEtaIntercalibration_Modelling_Down", help="Rescale JES MC generator modelling uncertainty by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEtaIntercalibration_StatAndMethod_Up", dest="jesEtaIntercalibration_StatAndMethod_Up", help="Rescale JES statistical and method uncertainty by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesEtaIntercalibration_StatAndMethod_Down", dest="jesEtaIntercalibration_StatAndMethod_Down", help="Rescale JES statistical and method uncertainty by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesSingleParticle_HighPt_Up", dest="jesSingleParticle_HighPt_Up", help="Rescale JES High pT term (2012 version)by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesSingleParticle_HighPt_Down", dest="jesSingleParticle_HighPt_Down", help="Rescale JES High pT term (2012 version) by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesRelativeNonClosure_Pythia8_Up", dest="jesRelativeNonClosure_Pythia8_Up", help="Rescale JES Closure of the calibration, relative to MC12a by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesRelativeNonClosure_Pythia8_Down", dest="jesRelativeNonClosure_Pythia8_Down", help="Rescale JES Closure of the calibration, relative to MC12a by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesPileupOffsetTermMuUp", dest="jesPileupOffsetTermMuUp", help="Rescale JES PileupOffsetTermMu component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesPileupOffsetTermMuDown", dest="jesPileupOffsetTermMuDown", help="Rescale JES PileupOffsetTermMu component by -1 sigma",
					  action='store_true', default=False)    
	parser.add_option("--jesPileupOffsetTermNPVUp", dest="jesPileupOffsetTermNPVUp", help="Rescale JES PileupOffsetTermNPV component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesPileupOffsetTermNPVDown", dest="jesPileupOffsetTermNPVDown", help="Rescale JES PileupOffsetTermNPV component by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--PileupPtTermUp", dest="jesPileupPtTermUp", help="Rescale JES PileupPtTerm component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--PileupPtTermDown", dest="jesPileupPtTermDown", help="Rescale JES PileupPtTerm component by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--PileupRhoTopologyUp", dest="jesPileupRhoTopologyUp", help="Rescale JES PileupRhoTopology component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--PileupRhoTopologyDown", dest="jesPileupRhoTopologyDown", help="Rescale JES PileupRhoTopology component by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesCloseByUp", dest="jesCloseByUp", help="Rescale JES CloseBy component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesCloseByDown", dest="jesCloseByDown", help="Rescale JES CloseBy component by -1 sigma",
					  action='store_true', default=False)    
	parser.add_option("--jesFlavorCompUncertUp", dest="jesFlavorCompUncertUp", help="Rescale JES jesFlavorCompUncert component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesFlavorCompUncertDown", dest="jesFlavorCompUncertDown", help="Rescale JES jesFlavorCompUncert component by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesFlavorResponseUncertUp", dest="jesFlavorResponseUncertUp", help="Rescale JES FlavorResponseUncert component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--jesFlavorResponseUncertDown", dest="jesFlavorResponseUncertDown", help="Rescale JES FlavorResponseUncert component by -1 sigma",
					  action='store_true', default=False)
	parser.add_option("--BJesUp", dest="BJesUp", help="Rescale JES bJes component by +1 sigma",
					  action='store_true', default=False)
	parser.add_option("--BJesDown", dest="BJesDown", help="Rescale JES bJes component by -1 sigma",
					  action='store_true', default=False)    
	parser.add_option("--jer", dest="jer", help="Smear jet energy resolution by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--scalestup", dest="scalestup", help="Shift cellout term up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--scalestdown", dest="scalestdown", help="Shift cellout term down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--resostup", dest="resostup", help="Shift cellout (resolution) term up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--resostdown", dest="resostdown", help="Shift cellout (resolution) term down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MMSLOW", dest="MMSLOW", help="Shift muon MS resolution down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MMSUP", dest="MMSUP", help="Shift muon MS resolution up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MIDLOW", dest="MIDLOW", help="Shift muon ID resolution down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MIDUP", dest="MIDUP", help="Shift muon ID resolution up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MSCALELOW", dest="MSCALELOW", help="Shift muon scale down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MSCALEUP", dest="MSCALEUP", help="Shift muon scale up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MEFFDOWN", dest="MEFFDOWN", help="Shift muon scale factor down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--MEFFUP", dest="MEFFUP", help="Shift muon scale factor up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--EEFFDOWN", dest="EEFFDOWN", help="Shift electron scale factor down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--EEFFUP", dest="EEFFUP", help="Shift electron scale factor up by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--EGZEEDOWN", dest="EGZEEDOWN", help="Shift egamma Zee uncertainty down by 1 sigma",
					  action='store_true', default=False)
	parser.add_option("--EGZEEUP", dest="EGZEEUP", help="Shift egamma Zee uncertainty up by 1 sigma",
					  action='store_true', default=False) 
	parser.add_option("--nevts", type="int", dest="nevts", help="Maximum number of events to process", default=-1)
	parser.add_option("--PUgen", dest="PUgen", help="Generate pileup reweighting file ?",
					  action='store_true', default=False)
	parser.add_option("--debug", dest="debug", help="Print out event informations",
					  action='store_true', default=False)
	(config, args) = parser.parse_args(args)
	return config

def getinfiles(config):
	""" Get input files from castor directory.
	Remember to never run directly on castor"""
	infile = config.infile
	if config.infile == 'default':
		if config.isdata and config.stream == 'Egamma':
			infile = fdefault[1]
		elif config.isdata and config.stream == 'Muons':
			infile = fdefault[2]
		else:
			infile = fdefault[0]
	ret = subprocess.call('xrdcp root://eosatlas/%s $TMPDIR/' % infile,shell=True)
	if ret != 0: print "getinfiles: could not copy",infile,"\nEXIT"
	newfile = '$TMPDIR/%s' % infile.split('/')[len(infile.split('/'))-1]
	return newfile

## Recommended trigger chains can be found on:
## https://twiki.cern.ch/twiki/bin/viewauth/Atlas/LowestUnprescaled
## For MC, two menus were used for mc11b:
## https://atlas-trigconf.cern.ch/mc/smkey/310/l1key/139/hltkey/252/ and
## https://atlas-trigconf.cern.ch/mc/smkey/308/l1key/134/hltkey/246/
## with the following setup
## {180164:"MCRECO:DB:TRIGGERDBMC:308,134,246",183003:"MCRECO:DB:TRIGGERDBMC:308,134,246",186169:"MCRECO:DB:TRIGGERDBMC:308,134,246",189751:"MCRECO:DB:TRIGGERDBMC:310,139,252"}
def getElTriggerSetup(RunNumber,isdata):
	lname = [['EF_e24vhi_medium1'],10]
	return lname

def getMuTriggerSetup(RunNumber,isdata):
	lname = ['EF_mu24_j65_a4tchad_EFxe60_tclcw']
	return lname

def main():

	o_file = ROOT.TFile("check_histograms.root","recreate")

	h_diff_jet = ROOT.TH2F("h_diff_jet","",50,0,500000,20,-1,1)

	print "susycutflow_1lep.py: starting",datetime.datetime.now()
	config = parseCmdLine(sys.argv[1:])

	## Read input file
	os.environ['TMPDIR'] = os.getenv('TMPDIR', '.')
	infile = config.infile
	if '/castor/cern.ch' in config.infile or config.infile == 'default': infile = getinfiles(config)
	t = ROOT.TChain("susy")
	t.Add(infile)

	## Fixes for vectors
	ROOT.gInterpreter.GenerateDictionary("vector<vector<float> >","vector")
	ROOT.gInterpreter.GenerateDictionary("vector<vector<int> >","vector")
	ROOT.gInterpreter.GenerateDictionary("vector<vector<unsigned int> >","vector")

	## Load RootCore libs
	#ROOT.gSystem.Load(".x %s/scripts/load_packages.C" % os.environ['ROOTCOREDIR'])
	from ROOT import gROOT
	gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");


	#ROOT.load_packages()
	
#    ROOT.gSystem.Load("%s/" % os.environ['ROOTCOREDIR'])

#    if os.path.exists("%s/preload" % os.environ['ROOTCOREDIR']):
#        fpreload = open("%s/preload" % os.environ['ROOTCOREDIR'],"r")
#        for line in fpreload:
#            line = line.split('\n')[0]
#            if line == "": continue
#            ROOT.gSystem.Load(line)
#    for libname in os.listdir("%s/lib/" % os.environ['ROOTCOREDIR']):
#        if not (libname.startswith("lib") and libname.endswith(".so")): continue
#        if 'ZeroLepton' in libname: continue
#        ROOT.gSystem.Load("%s/lib/%s" % (os.environ['ROOTCOREDIR'],libname))

	## Initialize tools
	susyObjDef = ROOT.SUSYObjDef()
	useLeptonTrigger = True
	isMC12b = True
	susyObjDef.initialize(config.isdata, config.atlfast, isMC12b,useLeptonTrigger)

	#Set jet calibration on by default in 2012
#    if config.nojetcalib: susyObjDef.SetJetCalib(False)
	susyObjDef.SetJetCalib(True)

	
	have_grl = False
	if config.isdata and (os.path.exists("%s/lib/libGoodRunsLists.so" % os.environ['ROOTCOREDIR']) or (('ROOTCORECONFIG' in os.environ) and os.path.exists("%s/lib/%s/libGoodRunsLists.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCORECONFIG']))) or (('ROOTCOREARCH' in os.environ) and os.path.exists("%s/lib/%s/libGoodRunsLists.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCOREARCH'])))):
		have_grl = True
		grl_reader = ROOT.Root.TGoodRunsListReader('data12_8TeV.periodAllYear_DetStatus-v42-pro13_CoolRunQuery-00-04-08_Susy.xml')
		grl_reader.AddXMLFile("data12_8TeV.periodAllYear_DetStatus-v42-pro13_CoolRunQuery-00-04-08_Susy.xml");
		grl_reader.Interpret()
		goodrunslist = grl_reader.GetMergedGRLCollection()
		goodrunslist.Summary(True) # Print out a list of all good runs and lbns
	have_pileuptool = False
	if config.PUgen and (os.path.exists("%s/lib/libPileupReweighting.so" % os.environ['ROOTCOREDIR']) or  (('ROOTCORECONFIG' in os.environ) and os.path.exists("%s/lib/%s/libPileupReweighting.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCORECONFIG']))) or (('ROOTCOREARCH' in os.environ) and os.path.exists("%s/lib/%s/libPileupReweighting.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCOREARCH'])))):
		genPileUpTool = ROOT.Root.TPileupReweighting("genPileUpTool")
		genPileUpTool.UsePeriodConfig("MC12a")
		genPileUpTool.Initialize()
	if config.PUwgt and (os.path.exists("%s/lib/libPileupReweighting.so" % os.environ['ROOTCOREDIR']) or (('ROOTCORECONFIG' in os.environ) and os.path.exists("%s/lib/%s/libPileupReweighting.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCORECONFIG']))) or (('ROOTCOREARCH' in os.environ) and os.path.exists("%s/lib/%s/libPileupReweighting.so" % (os.environ['ROOTCOREDIR'], os.environ['ROOTCOREARCH'])))):
		have_pileuptool = True
		elPileUpTool = ROOT.Root.TPileupReweighting("elPileUpTool")
		if os.path.isfile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/mc12a_generated.root"):
			print "using generated PU file for electrons"
			elPileUpTool.AddConfigFile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/mc12a_generated.root")
		else:
			print "using default PU file for electrons"
			elPileUpTool.AddConfigFile(os.environ['ROOTCOREDIR'] + "/../PileupReweighting/share/mc12ab_defaults.prw.root")
		elPileUpTool.SetDataScaleFactors(1/1.11) # You can apply this command by default or to study pileup unc.
		elPileUpTool.AddLumiCalcFile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/susy_data12_avgintperbx.root")
		elPileUpTool.SetUnrepresentedDataAction(2) # Action needs investigation
		tool_failure = elPileUpTool.Initialize()
		if tool_failure: print("El PileUpTool failed to initialise with code: %d" %tool_failure)
		muPileUpTool = ROOT.Root.TPileupReweighting("muPileUpTool")
		if os.path.isfile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/mc12a_generated.root"):
			print "using generated PU file for muons"
			muPileUpTool.AddConfigFile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/mc12a_generated.root")
		else:
			print "using default PU file for muons"
			muPileUpTool.AddConfigFile(os.environ['ROOTCOREDIR'] + "/../PileupReweighting/share/mc12ab_defaults.prw.root")
		muPileUpTool.SetDataScaleFactors(1/1.11) # You can apply this command by default or to study pileup unc.
		muPileUpTool.AddLumiCalcFile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/susy_data12_avgintperbx.root")            
		muPileUpTool.SetUnrepresentedDataAction(2) # Action needs investigation
		tool_failure = muPileUpTool.Initialize()
		if tool_failure: print("Mu PileUpTool failed to initialise with code: %d" %tool_failure)
		#print("Pileup weights:")
		#for i in range(25):
		#    print("weight(mu = %4.1f) = %13.10f(EL) %13.10f(MU)" %(float(i), elPileUpTool.getPileupWeight(i), muPileUpTool.getPileupWeight(i) ) )

	myBtagger = ROOT.SUSYBTagger.MV1
	useJVF = True
	BTagCalibTool = ROOT.BTagCalib("MV1",os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/BTagCalibration.env",os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/","0_7892",useJVF,0.7892) 
	
	myLeptonIso = ROOT.SignalIsoExp.TightIso 
 
	## Treatment of jet/Etmiss uncertainties
	whichsyste = ROOT.SystErr.NONE
	if config.jesdown:
		whichsyste = ROOT.SystErr.JESDOWN
	elif config.jesup:
		whichsyste = ROOT.SystErr.JESUP
	elif config.jesEffectiveNP_1_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_1_Down        
	elif config.jesEffectiveNP_1_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_1_Up
	elif config.jesEffectiveNP_2_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_2_Down        
	elif config.jesEffectiveNP_2_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_2_Up   
	elif config.jesEffectiveNP_3_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_3_Down        
	elif config.jesEffectiveNP_3_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_3_Up
	elif config.jesEffectiveNP_4_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_4_Down        
	elif config.jesEffectiveNP_4_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_4_Up        
	elif config.jesEffectiveNP_5_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_5_Down        
	elif config.jesEffectiveNP_5_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_5_Up
	elif config.jesEffectiveNP_6_Down:
		whichsyste = ROOT.SystErr.EffectiveNP_6_Down        
	elif config.jesEffectiveNP_6_Up:
		whichsyste = ROOT.SystErr.EffectiveNP_6_Up
	elif config.jesEtaIntercalibration_Modelling_Down:
		whichsyste = ROOT.SystErr.EtaIntercalibration_Modelling_Down        
	elif config.jesEtaIntercalibration_Modelling_Up:
		whichsyste = ROOT.SystErr.EtaIntercalibration_Modelling_Up
	elif config.jesEtaIntercalibration_StatAndMethod_Down:
		whichsyste = ROOT.SystErr.EtaIntercalibration_StatAndMethod_Down        
	elif config.jesEtaIntercalibration_StatAndMethod_Up:
		whichsyste = ROOT.SystErr.EtaIntercalibration_StatAndMethod_Up
	elif config.jesSingleParticle_HighPt_Down:
		whichsyste = ROOT.SystErr.SingleParticle_HighPt_Down        
	elif config.jesSingleParticle_HighPt_Up:
		whichsyste = ROOT.SystErr.SingleParticle_HighPt_Up
	elif config.jesRelativeNonClosure_Pythia8_Down:
		whichsyste = ROOT.SystErr.RelativeNonClosure_Pythia8_Down        
	elif config.jesRelativeNonClosure_Pythia8_Up:
		whichsyste = ROOT.SystErr.RelativeNonClosure_Pythia8_Up  
	elif config.jesPileupOffsetTermMuDown:
		whichsyste = ROOT.SystErr.PileupOffsetTermMuDown        
	elif config.jesPileupOffsetTermMuUp:
		whichsyste = ROOT.SystErr.PileupOffsetTermMuUp   
	elif config.jesPileupOffsetTermNPVDown:
		whichsyste = ROOT.SystErr.PileupOffsetTermNPVDown        
	elif config.jesPileupOffsetTermNPVUp:
		whichsyste = ROOT.SystErr.PileupOffsetTermNPVUp
	elif config.jesPileupPtTermDown:
		whichsyste = ROOT.SystErr.PileupPtTermDown        
	elif config.jesPileupPtTermUp:
		whichsyste = ROOT.SystErr.PileupPtTermUp
	elif config.jesPileupRhoTopologyDown:
		whichsyste = ROOT.SystErr.PileupRhoTopologyDown        
	elif config.jesPileupRhoTopologyUp:
		whichsyste = ROOT.SystErr.PileupRhoTopologyUp              
	elif config.jesCloseByDown:     
		whichsyste = ROOT.SystErr.CloseByDown        
	elif config.jesCloseByUp:
		whichsyste = ROOT.SystErr.CloseByUp   
	elif config.jesFlavorCompUncertDown:
		whichsyste = ROOT.SystErr.FlavorCompUncertDown        
	elif config.jesFlavorCompUncertUp:
		whichsyste = ROOT.SystErr.FlavorCompUncertUp
	elif config.jesFlavorResponseUncertDown:
		whichsyste = ROOT.SystErr.FlavorResponseUncertDown        
	elif config.jesFlavorResponseUncertUp:
		whichsyste = ROOT.SystErr.FlavorResponseUncertUp        
	elif config.BJesDown:
		whichsyste = ROOT.SystErr.BJesDown        
	elif config.BJesUp:
		whichsyste = ROOT.SystErr.BJesUp              
	elif config.jer:
		whichsyste = ROOT.SystErr.JER
	elif config.scalestup:
		whichsyste = ROOT.SystErr.SCALESTUP
	elif config.scalestdown:
		whichsyste = ROOT.SystErr.SCALESTDOWN
	elif config.resostup:
		whichsyste = ROOT.SystErr.RESOSTUP
	elif config.resostdown:
		whichsyste = ROOT.SystErr.RESOSTDOWN
	elif config.MMSLOW:
		whichsyste = ROOT.SystErr.MMSLOW
	elif config.MMSUP:
		whichsyste = ROOT.SystErr.MMSUP
	elif config.MIDLOW:
		whichsyste = ROOT.SystErr.MIDLOW
	elif config.MIDUP:
		whichsyste = ROOT.SystErr.MIDUP
	elif config.MSCALELOW:
		whichsyste = ROOT.SystErr.MSCALELOW
	elif config.MSCALEUP:
		whichsyste = ROOT.SystErr.MSCALEUP
	elif config.MEFFDOWN:
		whichsyste = ROOT.SystErr.MEFFDOWN
	elif config.MEFFUP:
		whichsyste = ROOT.SystErr.MEFFUP        
	elif config.EEFFDOWN:
		whichsyste = ROOT.SystErr.EEFFDOWN
	elif config.EEFFUP:
		whichsyste = ROOT.SystErr.EEFFUP        
	elif config.EGZEEDOWN:
		whichsyste = ROOT.SystErr.EGZEEDOWN
	elif config.EGZEEUP:
		whichsyste = ROOT.SystErr.EGZEEUP  

	## Loop over events (not at all optimized for speed, more for clarity)
	if config.nevts > 0:
		nEvts = config.nevts
	else:
		nEvts = t.GetEntries()
	cuts = [[0,0,0,'No cut'],
			[0,0,0,'GRL'],
			[0,0,0,'Tile Trip'],          
			[0,0,0,'Trigger'],
			[0,0,0,'Jet/MET Cleaning'],
			[0,0,0,'Primary vertex cut'],
			[0,0,0,'Cosmic or Bad muon veto'],
			[0,0,0,'Lepton cut'],
			[0,0,0,'>=2 jets pT>25 GeV'],
			]
	cuts = {}
	cuts["elel"] = copy.deepcopy(cuts)
	cuts["mumu"] = copy.deepcopy(cuts)
	cuts["elmu"] = copy.deepcopy(cuts)

	nevts_LArHole = [[0.,0.],[0.,0.]]

	
	for iEvt in range(nEvts):
		if nEvts < 10 or iEvt%(nEvts/10) == 0: print "Reading event",iEvt,"/",nEvts
		t.GetEntry(iEvt)

		if config.debug:
			print 'Event ' + str(t.EventNumber) + ' Run ' + str(t.RunNumber)

		## If generating pileup MC file don't need to run cutflow
		if config.PUgen:
			averageIntPerXing = t.averageIntPerXing
			if(t.lbn==1 and int(t.averageIntPerXing+0.5)==1):
				averageIntPerXing = 0.
			genPileUpTool.Fill(t.RunNumber,t.mc_channel_number,t.mcevt_weight[0][0],averageIntPerXing)
			continue

		## Do not forget to clear arrays once per event
		susyObjDef.Reset()

		##
		## PART-1 Object selection
		##

		## Get electrons
		##
		el_idx = {'signal':[],'baseline':[],'crack':[],'trgmatch':[],'goodpt':[],'met':ROOT.std.vector(int)()}
		elTrgSetup = getElTriggerSetup(t.RunNumber,config.isdata)
		elTrigCond = False
		itrig = 0
		for itrg,trgName in enumerate(elTrgSetup[0]):
			elTrigCond = elTrigCond or getattr(t,trgName)
		elTrigSet = elTrgSetup[1]

		for iEl in range(t.el_n):
			# Check if offline electron is matched to an EF electron trigger object
			# Be careful, D3PD variables depend on trigger chain used (=> different for various data run nb or mc)
			# Trigger matching is described on https://twiki.cern.ch/twiki/bin/view/AtlasProtected/EgammaTriggerMatching
			EFindex = ROOT.Long(-1)
			for itrg,trgName in enumerate(elTrgSetup[0]):
				trig_EF_el_EF = getattr(t,'trig_EF_el_'+trgName)
				if t.el_trackpt.at(iEl)>0 and ROOT.PassedTriggerEF(t.el_tracketa.at(iEl),t.el_trackphi.at(iEl),trig_EF_el_EF,
																   EFindex,t.trig_EF_el_n,t.trig_EF_el_eta,t.trig_EF_el_phi):
					el_idx['trgmatch'].append(iEl)
					break

			# Apply baseline SUSY electron selection 
			myRunNb = 180614 # This setup is obsolete and harmless cause checkOQ is no more used
#            if t.el_MET_Egamma10NoTau_wpx.at(iEl).at(0) != 0. and not t.el_medium.at(iEl):
#                print t.el_medium.at(iEl),t.el_MET_Egamma10NoTau_wpx.at(iEl).at(0)
			ismediumPP = t.el_mediumPP.at(iEl)

			t_ele_et = t.el_cl_E.at(iEl)/ROOT.TMath.CosH(t.el_etas2.at(iEl))

			t_DEmaxs1 = 0
			t_rHad = 0
			t_rHad1 = 0
			
			if ( t.el_emaxs1.at(iEl) + t.el_Emax2.at(iEl) ) != 0:
				t_DEmaxs1 = ( t.el_emaxs1.at(iEl) - t.el_Emax2.at(iEl) )/ ( t.el_emaxs1.at(iEl) + t.el_Emax2.at(iEl) )

			if t_ele_et != 0:
				t_rHad = t.el_Ethad.at(iEl)/t_ele_et
				t_rHad1 = t.el_Ethad1.at(iEl)/t_ele_et
													  
			if susyObjDef.FillElectron(iEl,
									   t.el_eta.at(iEl),t.el_phi.at(iEl),
									   t.el_cl_eta.at(iEl),t.el_cl_phi.at(iEl),t.el_cl_E.at(iEl),
									   t.el_tracketa.at(iEl),t.el_trackphi.at(iEl),
									   t.el_author.at(iEl),t.el_mediumPP.at(iEl),t.el_OQ.at(iEl),
									   t.el_nPixHits.at(iEl),t.el_nSCTHits.at(iEl),
									   t.el_MET_Egamma10NoTau_wet.at(iEl).at(0),10000.,2.47,whichsyste):
				el_idx['baseline'].append(iEl)
				el_idx['goodpt'].append(susyObjDef.GetElecTLV(iEl).Pt())

			if t.el_MET_Egamma10NoTau_wet.at(iEl).at(0) != 0.:
				el_idx['met'].push_back(iEl)

		## Apply descendent pT sorting of electrons
		ptandidx = zip(el_idx['goodpt'],el_idx['baseline'])
		ptandidx.sort(reverse=True)
		del el_idx['baseline'][:],el_idx['goodpt'][:]
		el_idx['baseline']   = [ x[1] for x in ptandidx ]
		el_idx['goodpt'] = [ x[0] for x in ptandidx ]

		for iEl in el_idx['baseline']:
			# Check whether a baseline electron is within crack region
			if susyObjDef.IsInCrack(t.el_cl_eta.at(iEl)):
				el_idx['crack'].append(iEl)
			# Apply additionnal cuts for signal electrons 
			# lepton pt cut is raised to 25 GeV to match e20_medium trigger
			if susyObjDef.IsSignalElectronExp(iEl, t.el_tightPP.at(iEl), t.vx_nTracks, t.el_ptcone30.at(iEl), t.el_topoEtcone30_corrected.at(iEl), t.el_trackIPEstimate_d0_unbiasedpvunbiased.at(iEl), t.el_trackIPEstimate_z0_unbiasedpvunbiased.at(iEl), t.el_trackIPEstimate_sigd0_unbiasedpvunbiased.at(iEl), myLeptonIso):
				el_idx['signal'].append(iEl)

		if config.debug:
			for el in el_idx['baseline']:
				print 'baseline el pt,eta,phi,E: ' + str(t.el_cl_pt.at(el)) + ' ' +  str(t.el_cl_eta.at(el)) + ' ' + str(t.el_cl_phi.at(el)) + ' '+ str(t.el_cl_E.at(el))
			for el in el_idx['signal']:
				print 'signal el pt,eta,phi,E: '  + str(susyObjDef.GetElecTLV(el).Pt())+ ' ' + str(susyObjDef.GetElecTLV(el).Eta())+ ' ' + str(susyObjDef.GetElecTLV(el).Phi())+ ' ' + str(susyObjDef.GetElecTLV(el).E())

		
		##
		## Get muons
		##
		mu_idx = {'signal':[],'baseline':[],'cosmic':[],'bad':[],'trgmatch':[],'goodpt':[],'met':ROOT.std.vector(int)()}
		muTrgSetup = getMuTriggerSetup(t.RunNumber,config.isdata)
		muTrigCond = False
		for trgName in muTrgSetup:
			muTrigCond = muTrigCond or getattr(t,trgName)
		trig_EF_trigmuonef_signature = getattr(t,'trig_EF_trigmuonef_'+muTrgSetup[0])
		for iMu in range(t.mu_staco_n):
			# Check if offline muon is matched to a muon trigger object
			EFindex = ROOT.Long(-1) 
			EFtrackindex = ROOT.Long(-1)
			if susyObjDef.MuonHasTriggerMatch(t.mu_staco_eta.at(iMu),t.mu_staco_phi.at(iMu),
											  trig_EF_trigmuonef_signature,EFindex,EFtrackindex,
											  t.trig_EF_trigmuonef_n,t.trig_EF_trigmuonef_track_CB_eta,
											  t.trig_EF_trigmuonef_track_CB_phi,t.trig_EF_trigmuonef_track_CB_hasCB):
				mu_idx['trgmatch'].append(iMu)

			# Baseline muon selection does not include any isolation cut and use muon up to 2.5 => directly used in Etmiss computation
			if susyObjDef.FillMuon(iMu,
								   t.mu_staco_pt.at(iMu),t.mu_staco_eta.at(iMu),t.mu_staco_phi.at(iMu),
								   t.mu_staco_me_qoverp_exPV.at(iMu),t.mu_staco_id_qoverp_exPV.at(iMu),
								   t.mu_staco_me_theta_exPV.at(iMu),t.mu_staco_id_theta_exPV.at(iMu),
								   t.mu_staco_id_theta.at(iMu),t.mu_staco_charge.at(iMu),
								   t.mu_staco_isCombinedMuon.at(iMu),t.mu_staco_isSegmentTaggedMuon.at(iMu),
								   t.mu_staco_loose.at(iMu),
								   t.mu_staco_nPixHits.at(iMu),t.mu_staco_nPixelDeadSensors.at(iMu),
								   t.mu_staco_nPixHoles.at(iMu),t.mu_staco_nSCTHits.at(iMu),
								   t.mu_staco_nSCTDeadSensors.at(iMu),t.mu_staco_nSCTHoles.at(iMu),
								   t.mu_staco_nTRTHits.at(iMu),t.mu_staco_nTRTOutliers.at(iMu),
								   10000.,2.5, whichsyste):
				mu_idx['met'].push_back(iMu)
				mu_idx['baseline'].append(iMu)
				mu_idx['goodpt'].append(susyObjDef.GetMuonTLV(iMu).Pt())

		## Apply descendent pT sorting of muons
		ptandidx = zip(mu_idx['goodpt'],mu_idx['baseline'])
		ptandidx.sort(reverse=True)
		del mu_idx['baseline'][:],mu_idx['goodpt'][:]
		mu_idx['baseline']   = [ x[1] for x in ptandidx ]
		mu_idx['goodpt'] = [ x[0] for x in ptandidx ]

		for iMu in mu_idx['baseline']:
			# Additionnal cut for signal muons: check whether it also pass isolation cut and if pT>20 GeV
			if susyObjDef.IsSignalMuonExp(iMu, t.vx_nTracks, t.mu_staco_ptcone30_trkelstyle.at(iMu), t.mu_staco_etcone30.at(iMu), t.mu_staco_trackIPEstimate_d0_unbiasedpvunbiased.at(iMu), t.mu_staco_trackIPEstimate_z0_unbiasedpvunbiased.at(iMu), t.mu_staco_trackIPEstimate_sigd0_unbiasedpvunbiased.at(iMu), myLeptonIso):
				mu_idx['signal'].append(iMu)
			# Check whether muon could be a cosmic candidate
			if susyObjDef.IsCosmicMuon(t.mu_staco_z0_exPV.at(iMu),t.mu_staco_d0_exPV.at(iMu),1.,0.2):
				mu_idx['cosmic'].append(iMu)
			# Check whether muon is badly reconstructed
			if susyObjDef.IsBadMuon(t.mu_staco_qoverp_exPV.at(iMu),t.mu_staco_cov_qoverp_exPV.at(iMu)):
				mu_idx['bad'].append(iMu)
				
		if config.debug:
			for mu in mu_idx['baseline']:
				print 'baseline mu pt,eta,phi,E: ' + str(t.mu_staco_pt.at(mu)) + ' ' +  str(t.mu_staco_eta.at(mu)) + ' ' + str(t.mu_staco_phi.at(mu)) + ' '+ str(t.mu_staco_E.at(mu))
			for mu in mu_idx['signal']:
				print 'signal mu pt,eta,phi,E: '  + str(susyObjDef.GetMuonTLV(mu).Pt())+ ' ' + str(susyObjDef.GetMuonTLV(mu).Eta())+ ' ' + str(susyObjDef.GetMuonTLV(mu).Phi())+ ' ' + str(susyObjDef.GetMuonTLV(mu).E())

		##
		## Get jets
		##
		## It is assumed that no sorting of jets as function of jet pT is necessary with AntiKt4LCTopo jets
		jet_idx = {'signal':[],'good':[],'bad':[],'LArHoleVeto':[],'goodpt':[],'btagged':[]}

		for iJet in range(t.jet_AntiKt4LCTopo_n):
			## Basic LAr hole veto applies to any jet (before overlap removal)
			if config.debug:
				print 'Jet ' + str(iJet) + ' pt,eta,phi,E= ' + str(t.jet_AntiKt4LCTopo_pt.at(iJet)) + ',' + str(t.jet_AntiKt4LCTopo_eta.at(iJet)) + ',' + str(t.jet_AntiKt4LCTopo_phi.at(iJet)) + ',' + str(t.jet_AntiKt4LCTopo_E.at(iJet))

			susyObjDef.FillJet(iJet,t.jet_AntiKt4LCTopo_pt.at(iJet),t.jet_AntiKt4LCTopo_eta.at(iJet),
								  t.jet_AntiKt4LCTopo_phi.at(iJet),t.jet_AntiKt4LCTopo_E.at(iJet),
								  t.jet_AntiKt4LCTopo_constscale_eta.at(iJet),t.jet_AntiKt4LCTopo_constscale_phi.at(iJet),
								  t.jet_AntiKt4LCTopo_constscale_E.at(iJet),t.jet_AntiKt4LCTopo_constscale_m.at(iJet),
								  t.jet_AntiKt4LCTopo_ActiveAreaPx.at(iJet),t.jet_AntiKt4LCTopo_ActiveAreaPy.at(iJet),
								  t.jet_AntiKt4LCTopo_ActiveAreaPz.at(iJet),t.jet_AntiKt4LCTopo_ActiveAreaE.at(iJet),
								  t.Eventshape_rhoKt4LC,  
								  t.averageIntPerXing,
								  t.vx_nTracks)         
								  
			if config.debug:           
				print 'Jet cal ' + str(iJet) + ' pt,eta,phi,E= ' + str(susyObjDef.GetJetTLV(iJet).Pt()) + ',' + str(susyObjDef.GetJetTLV(iJet).Eta()) + ',' + str(susyObjDef.GetJetTLV(iJet).Phi()) + ',' + str(susyObjDef.GetJetTLV(iJet).E())
				h_diff_jet.Fill(t.jet_AntiKt4LCTopo_pt.at(iJet),(susyObjDef.GetJetTLV(iJet).Pt() - t.jet_AntiKt4LCTopo_pt.at(iJet))/t.jet_AntiKt4LCTopo_pt.at(iJet))
				
			if(whichsyste!=ROOT.SystErr.NONE): 
				local_truth_flavor = 0
				if not config.isdata:
					local_truth_flavor = t.jet_AntiKt4LCTopo_flavor_truth_label.at(iJet)           
					susyObjDef.ApplyJetSystematics(iJet,t.jet_AntiKt4LCTopo_constscale_eta.at(iJet),local_truth_flavor,t.averageIntPerXing,t.vx_nTracks,whichsyste)
				if config.debug:           
					print 'Jet cal ' + str(iJet) + ' pt,eta,phi,E= ' + str(susyObjDef.GetJetTLV(iJet).Pt()) + ',' + str(susyObjDef.GetJetTLV(iJet).Eta()) + ',' + str(susyObjDef.GetJetTLV(iJet).Phi()) + ',' + str(susyObjDef.GetJetTLV(iJet).E())      
			 
			## Consider only jets with pT > 20 GeV for following
			if susyObjDef.GetJetTLV(iJet).Pt() <= 20000.: continue

			## Check overlap removal with electrons, skip jets overlapping with electrons
			isoverlap = False
			for iEl in el_idx['baseline']:
				if susyObjDef.GetElecTLV(iEl).DeltaR(susyObjDef.GetJetTLV(iJet)) > 0.2: continue
				isoverlap = True
				break
			if isoverlap: continue

			## Do not apply any eta cut for jet cleaning
			## Remember jet cleaning is applied only to data
			isgoodjet = False
			if susyObjDef.IsGoodJet(iJet,t.jet_AntiKt4LCTopo_constscale_eta.at(iJet),
									t.jet_AntiKt4LCTopo_emfrac.at(iJet),t.jet_AntiKt4LCTopo_hecf.at(iJet),
									t.jet_AntiKt4LCTopo_LArQuality.at(iJet),t.jet_AntiKt4LCTopo_HECQuality.at(iJet),
									t.jet_AntiKt4LCTopo_AverageLArQF.at(iJet),
									t.jet_AntiKt4LCTopo_Timing.at(iJet),t.jet_AntiKt4LCTopo_sumPtTrk.at(iJet),
									t.jet_AntiKt4LCTopo_fracSamplingMax.at(iJet),
									t.jet_AntiKt4LCTopo_SamplingMax.at(iJet),
									t.jet_AntiKt4LCTopo_NegativeE.at(iJet),
									t.RunNumber,20000.,10.):
				isgoodjet = True
				
			if config.debug:           
				print 'Jet cal ' + str(iJet) + ' pt,eta,phi,E= ' + str(susyObjDef.GetJetTLV(iJet).Pt()) + ',' + str(susyObjDef.GetJetTLV(iJet).Eta()) + ',' + str(susyObjDef.GetJetTLV(iJet).Phi()) + ',' + str(susyObjDef.GetJetTLV(iJet).E())
					
				h_diff_jet.Fill(t.jet_AntiKt4LCTopo_pt.at(iJet),(susyObjDef.GetJetTLV(iJet).Pt() - t.jet_AntiKt4LCTopo_pt.at(iJet))/t.jet_AntiKt4LCTopo_pt.at(iJet))
	
			## Consider only jets with pT > 20 GeV for following
			if susyObjDef.GetJetTLV(iJet).Pt() <= 20000.: continue
				
			## Check overlap removal with electrons, skip jets overlapping with electrons
			isoverlap = False
			for iEl in el_idx['baseline']:
				if susyObjDef.GetElecTLV(iEl).DeltaR(susyObjDef.GetJetTLV(iJet)) > 0.2: continue
				isoverlap = True
				break
			if isoverlap: continue
			## Flag remaining jets
			if not isgoodjet:
				jet_idx['bad'].append(iJet)
			elif isgoodjet and math.fabs(susyObjDef.GetJetTLV(iJet).Eta()) < 2.8:
				jet_idx['goodpt'].append(susyObjDef.GetJetTLV(iJet).Pt())
				jet_idx['good'].append(iJet)


		## Apply descendent pT sorting of jets
		ptandidx = zip(jet_idx['goodpt'],jet_idx['good'])
		ptandidx.sort(reverse=True)
		del jet_idx['good'][:],jet_idx['goodpt'][:]
		jet_idx['good']   = [ x[1] for x in ptandidx ]
		jet_idx['goodpt'] = [ x[0] for x in ptandidx ]

		## Additonnal eta and JVF requirements used in 1-lepton analysis to define "signal" jets
		## Those cuts are necessary to reduce pileup jets
		for iJet in jet_idx['good']:
			passJVF = t.jet_AntiKt4LCTopo_jvtxf.at(iJet) > 0.5
			if math.fabs(t.jet_AntiKt4LCTopo_eta.at(iJet)) < 2.5 and passJVF:
				jet_idx['signal'].append(iJet)
		
		## Check if one of 3 leading jets (pt>25GeV, |eta|<2.5) is tagged as b-jet
		if not config.isdata:
			pt_btag = ROOT.std.vector(float)()
			eta_btag = ROOT.std.vector(float)()
			val_btag = ROOT.std.vector(float)()
			pdgid_btag = ROOT.std.vector(int)()
		for idx,iJet in enumerate(jet_idx['signal']):
			if idx > 2: break
			if math.fabs(susyObjDef.GetJetTLV(iJet).Eta()) < 2.5 and susyObjDef.GetJetTLV(iJet).Pt() > 25000.:
				if susyObjDef.IsBJet(t.jet_AntiKt4LCTopo_flavor_weight_MV1.at(iJet),0.7892):
					jet_idx['btagged'].append(iJet)
				## Fill information to compute b-tagging weight
				if not config.isdata:
					pt_btag.push_back(susyObjDef.GetJetTLV(iJet).Pt())
					eta_btag.push_back(t.jet_AntiKt4LCTopo_eta.at(iJet))
					val_btag.push_back(t.jet_AntiKt4LCTopo_flavor_weight_MV1.at(iJet))
					pdgid_btag.push_back(t.jet_AntiKt4LCTopo_flavor_truth_label.at(iJet))
		  
		# r17 working points and b-tagging scaling factors are documented on:
		# https://twiki.cern.ch/twiki/bin/view/AtlasProtected/Analysis17
		# This is just an example on how to compute b-tagging weights but it is not used later in this pg

		# Note that the file BTagCalibration.env points to scale factors without the JVF cut. There is a file name BTagCalibration_JVF.env available, pointing to the scale factors for jets with a JVF cut at 0.5
		
		if not config.isdata and pt_btag.size() > 0:
			btagres = BTagCalibTool.BTagCalibrationFunction(pt_btag,eta_btag,val_btag,pdgid_btag)
			wgtbtag = btagres.first
			if config.debug:
				print t.EventNumber,'number of b-tagged jets',len(jet_idx['btagged']),'/',pt_btag.size(),'weight(nominal) = %3.2f' % wgtbtag.at(0),'weight(B_UP) = %3.2f' % wgtbtag.at(4),'weight(B_DOWN) = %3.2f' % wgtbtag.at(1),'weight(C_UP) = %3.2f' % wgtbtag.at(5),'weight(C_DOWN) = %3.2f' % wgtbtag.at(2),'weight(L_UP) = %3.2f' % wgtbtag.at(6),'weight(L_DOWN) = %3.2f' % wgtbtag.at(3)

		##
		## Compute simplified refined Etmiss 
		##
		## (make use of el_idx['met'] and mu_idx['met'] which contain list of electrons/muons to be included in Etmiss)
		whichmet = ROOT.SUSYMet.Default
		doEgammaJetFix = False
		met = susyObjDef.GetMET(t.jet_AntiKt4LCTopo_MET_Egamma10NoTau_wet,
								t.jet_AntiKt4LCTopo_MET_Egamma10NoTau_wpx,
								t.jet_AntiKt4LCTopo_MET_Egamma10NoTau_wpy,
								t.jet_AntiKt4LCTopo_MET_Egamma10NoTau_statusWord,
								el_idx['met'],
								t.el_MET_Egamma10NoTau_wet,
								t.el_MET_Egamma10NoTau_wpx,
								t.el_MET_Egamma10NoTau_wpy,
								t.el_MET_Egamma10NoTau_statusWord,                             
								t.MET_Egamma10NoTau_CellOut_etx, 
								t.MET_Egamma10NoTau_CellOut_ety,
								t.MET_Egamma10NoTau_CellOut_sumet,
								t.MET_Egamma10NoTau_CellOut_Eflow_STVF_etx, 
								t.MET_Egamma10NoTau_CellOut_Eflow_STVF_ety,
								t.MET_Egamma10NoTau_CellOut_Eflow_STVF_sumet,                                
								t.MET_Egamma10NoTau_RefGamma_etx,
								t.MET_Egamma10NoTau_RefGamma_ety,
								t.MET_Egamma10NoTau_RefGamma_sumet,
								mu_idx['met'],
								t.mu_staco_ms_qoverp, 
								t.mu_staco_ms_theta, 
								t.mu_staco_ms_phi, 
								t.mu_staco_charge,
								t.mu_staco_energyLossPar,
								t.averageIntPerXing,
								whichmet,
								whichsyste,
								doEgammaJetFix)


		metUtil = susyObjDef.GetMETUtility()

		if config.debug:
			# print missing et values with the following structure:"
			# MissingEt from ntuple
			# MissingEt muon from ntuple
			# MissingEt recomputed
			# MissingEt muon recomputed
			print 'MissingEt from D3PD ' + str(ROOT.TMath.Sqrt(ROOT.TMath.Power(t.MET_Egamma10NoTau_RefFinal_etx,2) + ROOT.TMath.Power(t.MET_Egamma10NoTau_RefFinal_ety,2))) + ' , from SUSYTools ' + str(met.Mod())
		

		##
		## Apply lepton veto (done on every jet !)
		##
		for iJet in jet_idx['good']:
			mylist = copy.deepcopy(el_idx['baseline'])
			for iEl in mylist:
				if susyObjDef.GetElecTLV(iEl).DeltaR(susyObjDef.GetJetTLV(iJet)) > 0.4: continue
				el_idx['baseline'].remove(iEl)
				if iEl in el_idx['signal']: el_idx['signal'].remove(iEl)
			mylist = copy.deepcopy(mu_idx['baseline'])
			for iMu in mylist:
				if susyObjDef.GetMuonTLV(iMu).DeltaR(susyObjDef.GetJetTLV(iJet)) > 0.4: continue
				mu_idx['baseline'].remove(iMu)
				if iMu in mu_idx['cosmic']: mu_idx['cosmic'].remove(iMu) # Check cosmic cut only if sufficiently away from a jet
				if iMu in mu_idx['signal']: mu_idx['signal'].remove(iMu)


		##
		## PART-2 Event selection - do it only for 1-lepton + 3 jets loose channel
		##
		icut = 0
		wgt = [1.,1.] # el,mu channels respectively

		# No extra period weight with new pileup reweighting
		puwgt = [1.,1.] # el,mu channels respectively

		pass = {}

		pass["elel"] = True
		pass["mumu"] = True
		pass["elmu"] = True

		if not config.isdata and config.PUwgt and have_pileuptool:
			averageIntPerXing = t.averageIntPerXing
			if(t.lbn==1 and int(t.averageIntPerXing+0.5)==1):
				averageIntPerXing = 0.           
			puwgt[0] *= elPileUpTool.GetCombinedWeight(t.RunNumber,t.mc_channel_number,averageIntPerXing)
			puwgt[1] *= muPileUpTool.GetCombinedWeight(t.RunNumber,t.mc_channel_number,averageIntPerXing)
		
		for chan in ["elel","mumu","elmu"]:
			cuts[chan][icut][0] += 1 
			cuts[chan][icut][1] += wgt[0]
			cuts[chan][icut][2] += wgt[0]*puwgt[0] 

		icut += 1

		# Apply GRL selection if we loaded the reader OK
		if not have_grl or not config.isdata or goodrunslist.HasRunLumiBlock(t.RunNumber, t.lbn):			
			for chan in ["elel","mumu","elmu"]:
				cuts[chan][icut][0] += 1 
				cuts[chan][icut][1] += wgt[0]
				cuts[chan][icut][2] += wgt[0]*puwgt[0] 
		else:
			for chan in ["elel","mumu","elmu"]:
				pass[chan] = False
		icut += 1

		# Apply TileTrip 
		if not config.isdata or not susyObjDef.IsTileTrip(t.RunNumber, t.lbn, t.EventNumber):
			for chan in ["elel","mumu","elmu"]:
				cuts[chan][icut][0] += 1 
				cuts[chan][icut][1] += wgt[0]
				cuts[chan][icut][2] += wgt[0]*puwgt[0] 
		else:
			for chan in ["elel","mumu","elmu"]:
				pass[chan] = False
		icut += 1

		# Trigger
		if not config.isdata: # MC treatment, do reweighting or apply scale factors
			if pass["elel"] and elTrigCond: 
				if len(el_idx['baseline']):
					elidx = el_idx['baseline'][0]
				for chan in ["elel"]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 
			else:
				pass["elel"] = False
			if (pass["mumu"] or pass["elmu"]) and config.trgwgt and len(mu_idx['baseline']):
				muidx = mu_idx['baseline'][0]
				value_array = array.array('d',[t.mu_staco_pt.at(muidx),t.mu_staco_eta.at(muidx),t.mu_staco_phi.at(muidx),float(t.mu_staco_isCombinedMuon.at(muidx) == True),t.mu_staco_ptcone20.at(muidx)])
				weight_muon = ROOT.APEvtWeight(ROOT.APEvtWeight.kMuon)
				weight_muon.AddWeightToEvt(trigWeighter.GetWeight(value_array))
				wgt[1] *= weight_muon.GetWeight()
				for chan in ["mumu","elmu"]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 
			elif (pass["mumu"] or pass["elmu"]) and not config.trgwgt and muTrigCond:
				if len(mu_idx['trgmatch']):
					if len(mu_idx['baseline']) and mu_idx['baseline'][0] in mu_idx['trgmatch']:
						muidx = mu_idx['baseline'][0]
					else:
						muidx = mu_idx['trgmatch'][0]
				for chan in [mumu","elmu"]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 
			else:
				pass["mumu"] = False
				pass["elmu"] = False
	

		
		else: # Data
			if pass["elel"] and elTrigCond:
				for chan in ["elel"]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 
			else: pass["elel"] = False
			if (pass["mumu"] or pass["elmu"]) and muTrigCond:
				for chan in ["mumu","elmu"]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 
			else: 
				pass["mumu"] = False
				pass["elmu"] = False
			
		icut += 1

		# Jet/MET cleaning cut
		# larError check is only applied to data
		if len(jet_idx['bad']) == 0 and (not config.isdata or t.larError == 0):

			for chan in ["elel","mumu","elmu"]:
				if pass[chan]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 	
		else:
			for chan in ["elel","mumu","elmu"]:
				pass[chan] = False

		icut += 1


		# Good primary vertex
		if susyObjDef.IsGoodVertex(t.vx_nTracks):
			for chan in ["elel","mumu","elmu"]:
				if pass[chan]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 	
		else:
			for chan in ["elel","mumu","elmu"]:
				pass[chan] = False
		icut += 1

		# Cosmic or Bad muon veto
		if len(mu_idx['cosmic']) == 0 and len(mu_idx['bad']) == 0:
			for chan in ["elel","mumu","elmu"]:
				if pass[chan]:
					cuts[chan][icut][0] += 1 
					cuts[chan][icut][1] += wgt[0]
					cuts[chan][icut][2] += wgt[0]*puwgt[0] 	
		else:
			for chan in ["elel","mumu","elmu"]:
				pass[chan] = False
		icut += 1

		# Lepton cut
		#
		# Compute event weight for Monte Carlo when selecting leptons
		# event weight is computed after overlap removal (could be debated)
		# Still need to figure out whether noniso muons should also be rescaled ? (they are good muons)
		if not config.isdata:
			for iEl in el_idx['signal']:
				pt = susyObjDef.GetElecTLV(iEl).Pt()
				wgt[0] *= susyObjDef.GetSignalElecSF(t.el_cl_eta.at(iEl),pt,True,True,True,200841,whichsyste)       
			for iMu in mu_idx['signal']:
				wgt[1] *= susyObjDef.GetSignalMuonSF(iMu,whichsyste)     
		passel = passel and len(el_idx['signal']) == 1 and len(mu_idx['baseline']) == 0 and len(el_idx['baseline']) == 1
		# For electron, request also that the selected offline electron is matching the electron trigger object
		# Since for MC, SF are used, do the matching both on data and MC
		passel = passel and len(el_idx['trgmatch']) and (el_idx['signal'][0] in el_idx['trgmatch'])
		if passel:
			elcuts[icut][0] += 1 
			elcuts[icut][1] += wgt[0]
			elcuts[icut][2] += wgt[0]*puwgt[0]

		passmu = passmu and len(mu_idx['signal']) == 1 and len(mu_idx['baseline']) == 1 and len(el_idx['baseline']) == 0
			
		if passmu:
			mucuts[icut][0] += 1
			mucuts[icut][1] += wgt[1]
			mucuts[icut][2] += wgt[1]*puwgt[1]
		icut += 1

		# Check if there are >= 2 jets pT > 15 GeV 
		if len(jet_idx['signal']) >= 2 and susyObjDef.GetJetTLV(jet_idx['signal'][1]).Pt() > 15000.:
			if passel:
				elcuts[icut][0] += 1 
				elcuts[icut][1] += wgt[0]
				elcuts[icut][2] += wgt[0]*puwgt[0] 
			if passmu:
				mucuts[icut][0] += 1
				mucuts[icut][1] += wgt[1]
				mucuts[icut][2] += wgt[1]*puwgt[1]
		else:
			passel = passmu = False
		icut += 1



	if not config.PUwgt: print "WARNING: pileup reweighting is off ! To run with it: ./susycutflow_1lep.py --PUwgt"
	print "susycutflow_1lep.py: electron cutflow summary"
	print "%2s %25s %8s %8s %8s" % ("","Cut name","Entries","Evts","Evts(PU)")
	for icut,cut in enumerate(elcuts):
		print "%2d %25s %8d %8.2f %8.2f" % (icut,cut[3],cut[0],cut[1],cut[2])
	print "susycutflow_1lep.py: muon cutflow summary"
	print "%2s %25s %8s %8s %8s" % ("","Cut name","Entries","Evts","Evts(PU)")
	for icut,cut in enumerate(mucuts):
		print "%2d %25s %8d %8.2f %8.2f" % (icut,cut[3],cut[0],cut[1],cut[2])
	print "susycutflow_1lep.py: ending",datetime.datetime.now()

	if config.PUgen: genPileUpTool.WriteToFile(os.environ['ROOTCOREDIR'] + "/../SUSYTools/data/mc12a_generated.root")
	susyObjDef.finalize()

	o_file.Write()
	o_file.Close()

if __name__ == '__main__':
	main()
