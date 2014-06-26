#!/usr/bin/env python

#To Do
# Add Legends
# Fix labels
# Apply ATLAS styles


import code

import numpy as np
import matplotlib as mpl
from matplotlib import ticker
import matplotlib.colors
from basic_units import radians
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

from rootpy.io import root_open
import root_numpy as rnp
from array import *
import rootpy.ROOT
import pylab

from rootpy.plotting import root2matplotlib as rplt
from rootpy.plotting import *
from matplotlib.patches import Rectangle

#For correlation plot / DataFrame
from pandas import *

from ATLASStyle import *

import util
import copy
import scipy
import os

rootpy.R.gROOT.SetBatch()

# mpl.rcParams.update(style_mpl() )
# activate latex text rendering
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
mpl.rc('text', usetex=True)

# mpl.use('Agg')


# definitions for the axes
left, width = 0.15, 0.45
bottom, height = 0.15, 0.45
bottom_h = bottom+height
left_h = left+width

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.35]
rect_histy = [left_h, bottom, 0.35, height]

from math import log10, floor
def round_to_1(x):
	return round(x, -int(floor(log10(x))))

# Define a class that forces representation of float to look a certain way
# This remove trailing zero so '1.0' becomes '1'
class nf(float):
     def __repr__(self):
         str = '%.1f' % (self.__float__(),)
         if str[-1]=='0':
             return '%.0f' % self.__float__()
         else:
             return '%.1f' % self.__float__()


InterestingPlots = [

	('RJVars_M_1_0_0','RJVars_M_2_0_0'),
	('RJVars_M_1_0_1','RJVars_M_2_0_1'),

	('RJVars_M_1_0_0','RJVars_M_1_1_0'),
	('RJVars_M_1_0_1','RJVars_M_1_1_1'),

	('RJVars_M_2_0_0','RJVars_M_2_1_0'),
	('RJVars_M_2_0_1','RJVars_M_2_1_1'),

	('RJVars_M_1_1_0/RJVars_M_1_0_0','RJVars_M_2_1_0/RJVars_M_2_0_0'),
	('RJVars_M_1_1_1/RJVars_M_1_0_1','RJVars_M_2_1_1/RJVars_M_2_0_1'),

	('RJVars_M_1_1_0/RJVars_M_1_0_0','RJVars_dPhi_0_0_0'),

	('RJVars_M_0_0_0','RJVars_dPhiVis_0_0_0'),
	('RJVars_M_0_0_1','RJVars_dPhiVis_0_0_1'),

	('RJVars_cosTheta_0_0_0','RJVars_M_0_0_0'),

	('RJVars_cosTheta_1_0_0','RJVars_M_1_0_0'),
	('RJVars_cosTheta_1_0_1','RJVars_M_1_0_1'),

	('RJVars_gamma_0_0_0','RJVars_M_0_0_0'),

	('RJVars_cosTheta_1_1_0','RJVars_cosTheta_2_1_0'),
	('RJVars_cosTheta_1_1_1','RJVars_cosTheta_2_1_1'),

	('RJVars_dPhi_1_1_1','RJVars_dPhi_2_1_1'),
	('RJVars_dPhi_1_0_1','RJVars_dPhi_2_0_1'),

	('RJVars_dPhiDecay_1_0_1','RJVars_dPhiDecay_2_0_1'),

	#cross terms in mass
	# ('RJVars_M_1_1_0','RJVars_M_2_0_0'),
	# ('RJVars_M_1_1_1','RJVars_M_2_0_1'),
	# ('RJVars_M_1_0_0','RJVars_M_2_1_0'),
	# ('RJVars_M_1_0_1','RJVars_M_2_1_1'),


]

NEventHists = {}
NEvent = {}


dataPeriods = [ 'Egamma.periodA',
				'Egamma.periodB',
				'Egamma.periodC',
				'Egamma.periodD',
				'Egamma.periodE',
				'Egamma.periodG',
				'Egamma.periodH',
				'Egamma.periodI',
				'Egamma.periodJ',
				'Egamma.periodL',
				'Muons.periodA',
				'Muons.periodB',
				'Muons.periodC',
				'Muons.periodD',
				'Muons.periodE',
				'Muons.periodG',
				'Muons.periodH',
				'Muons.periodI',
				'Muons.periodJ',
				'Muons.periodL']

dataFiles = {}

for dataPeriod in dataPeriods:
	dataFiles[dataPeriod] = root_open("RecursiveJigsawNtuples/%s.root"%(dataPeriod)  )
	NEventHists[dataPeriod] = dataFiles[dataPeriod].hist_entries_slim
	NEvent[dataPeriod] = 	NEventHists[dataPeriod].Integral()
	print "Sample Egamma %s with %d events" % (dataPeriod,NEvent[dataPeriod])


from variableConfig import *

# DSID/Filename, lumi*XS, Sample Label, firstInCombinedSample

MCSamples = [
			('105861', 21000*129.26658*1      , r"ttbar"          , 1  ),#  //ttbar
			("119353", 21000*0.1041*1.175     , r"ttbar+V"        , 1  ),#  //ttbar+W
			("119354", 21000*0.093317*1.175   , r""               , 0  ),#  //ttbar+Wj
			("119355", 21000*0.06769*1.3      , r""               , 0  ),#  //ttbar+Z
			("119356", 21000*0.087339*1.3     , r""               , 0  ),#  //ttbar+Zj
			("126892", 21000*5.4982*1.07      , r"WW"             , 1  ),#  //WW (SHERPA ALL LEPTONIC)
			("126893", 21000*9.7534*1.06      , r"WZ"             , 1  ),#  //WZ
			("126894", 21000*8.7356*1.11      , r"ZZ"             , 1  ),#  //ZZ
			("108346", 21000*20.658*1.083     , r"Single t"       , 1  ),#  //single top
			("107660", 21000*712.11*1.2303    , r"Z+Jets"         , 1  ),#  //z + jets 
			("107661", 21000*154.77*1.2303    , r""               , 0  ),#
			("107662", 21000*48.912*1.2303    , r""               , 0  ),#
			("107663", 21000*14.226*1.2303    , r""               , 0  ),#
			("107664", 21000*3.7838*1.2303    , r""               , 0  ),#
			("107665", 21000*1.1148*1.2303    , r""               , 0  ),#
			("107650", 21000*712.11*1.2303    , r""               , 0  ),#
			("107651", 21000*154.77*1.2303    , r""               , 0  ),#
			("107652", 21000*48.912*1.2303    , r""               , 0  ),#
			("107653", 21000*14.226*1.2303    , r""               , 0  ),#
			("107654", 21000*3.7838*1.2303    , r""               , 0  ),#
			("107655", 21000*1.1148*1.2303    , r""               , 0  ),#
			("172728", 21000*1.9985*0.65482   , r"stop 300 150 100"  , 1  ),#  //more signal
			("166438", 21000*1*1              , r"stop 300 100 50"   , 1  ),#  //signal 
			("172660", 21000*1*1              , r"stop 300 100 1"    , 1  ),#  //signal 
]

MCFiles = {}

MCScales = {}

for (MCSample,norm, label, tmp) in MCSamples:
	MCFiles[MCSample] = root_open("RecursiveJigsawNtuples/%s.root"%(MCSample) ) 
	NEventHists[MCSample] = MCFiles[MCSample].Get("hist_entries_slim")
	NEvent[MCSample] = 	NEventHists[MCSample].Integral()
	MCScales[MCSample] = norm / NEvent[MCSample]


	print "Sample %s with %d events with scale %f" % (MCSample,NEvent[MCSample], MCScales[MCSample])

	# print norm
	# print MCScales[MCSample]

NPArrays = {}

samplestodraw = [ y for y in MCSamples if y[3]==1 ]

samplestooverlay = [
	MCSamples[-3],
]

colorpal = sns.color_palette("husl", len(samplestodraw) )

writeAuxPlots = 1
writeCorrPlots = 1

radianTickLocations = [0, 
						np.pi/4., 
						np.pi/2.,
						3*np.pi/4., 
						np.pi]
radianTickLabels = 	['0',
					r'$\frac{\pi}{4}$',
					r'$\frac{\pi}{2}$',
					r'$\frac{3\pi}{4}$', 
					r'$\pi$']

for (var1,var2) in InterestingPlots:

	print (var1, var2)

	try:
		var1unit = 1. if 'M_' in var1 else 1.
		var1label = RJVarsLabelDict[var1]
		var1limits = RJVarsLimitsDict[var1]
		var1numpyexp = "numpytree.%s/%s"%(var1,var1unit) 
	except:
		if "/" in var1:
			var1a = var1.split('/')[0]
			var1b = var1.split('/')[1]
			var1label = RJVarsLabelDict[ var1a] + r' / ' + RJVarsLabelDict[ var1b] 
			var1limits = (0.,2.,50)
			var1aunit = 1. if 'M_' in var1a else 1.
			var1bunit = 1. if 'M_' in var1b else 1.
			var1numpyexp = "(numpytree.%s/%s) / (numpytree.%s/%s)"%(var1a,var1aunit, var1b, var1bunit)  

	try:
		var2unit = 1. if 'M_' in var2 else 1.
		var2label = RJVarsLabelDict[var2]
		var2limits = RJVarsLimitsDict[var2]
		var2numpyexp = "numpytree.%s/%s"%(var2,var2unit) 
	except:
		if "/" in var2:
			var2a = var2.split('/')[0]
			var2b = var2.split('/')[1]
			var2label = RJVarsLabelDict[ var2a] + r' / ' + RJVarsLabelDict[ var2b] 
			var2limits = (0.,2.,50)
			var2aunit = 1. if 'M_' in var2a else 1.
			var2bunit = 1. if 'M_' in var2b else 1.
			var2numpyexp = "(numpytree.%s/%s) / (numpytree.%s/%s)"%(var2a,var2aunit, var2b, var2bunit)  

	vartreeexp = var1numpyexp.replace("numpytree.","") + ":" + var2numpyexp.replace("numpytree.","") 
	vartreeexp1 = var1numpyexp.replace("numpytree.","") 
	vartreeexp2 = var2numpyexp.replace("numpytree.","") 

	OverlayFig = plt.figure(figsize=(6, 6), dpi=100, facecolor='white')
	OverlayAxes = OverlayFig.add_axes([0.15,0.15,0.8,0.8])


	colornorm = 0

	ims = {}
	ctr = {}

	backgroundcorr = 0

	directory = "./plots/%s_vs_%s/"%(var1.replace("/","Over") ,var2.replace("/","Over") ) 
	if not os.path.exists(directory):
	    os.makedirs(directory)


	for jSample, (MCSample,norm, label, firstInCombinedSample) in enumerate(MCSamples) :

		if (MCSample,norm, label, firstInCombinedSample) in samplestodraw:
		    iSample = samplestodraw.index((MCSample,norm, label, firstInCombinedSample)  )
		else:
			continue

		print MCSample

		if writeAuxPlots:

			c = rootpy.R.TCanvas("test","test",600,600)

			for iplot in ['h_met',
							'h_mll',
							'h_mjj',
							'h_mlj1',
							'h_mlj2',
							'h_met',
							'h_met_mag',
							'h_met_mll',
							'h_met_mjj',
							'h_met_mlj1',
							'h_met_mlj2',
							'h_njet_jetpt1',
							'h_njet_jetpt2',
							'h_jetpt2_jetpt1',
							'h_leppt2_leppt1',
							'h_dphilep1jet1_dphilep1jet2',
							'h_dphilep2jet1_dphilep2jet2',
							]:
				exec("%s = MCFiles[MCSample].%s"%(iplot,iplot)  )
				exec("%s.Draw('colz')"%(iplot)  )
				c.SaveAs("plots/%s_%s.eps"%(iplot,label) )

		mytree = MCFiles[MCSample].SR


		if writeCorrPlots:

			CorrelationFig = plt.figure(figsize=(6, 6), dpi=100, facecolor='white')
			CorrelationAxes = CorrelationFig.add_axes([0.15,0.15,0.8,0.8])
			# print "Drawing variable correlation matrix -----"
			arr = rnp.tree2rec(mytree)[:1000]
			branches = mytree.branchnames
			sns.corrplot(arr,names=branches, ax=CorrelationAxes, annot=False, diag_names=False)
			CorrelationAxes.tick_params(axis='both', labelsize=4)

			CorrelationAxes.set_xticklabels( [branchname.replace("_"," ") for branchname in branches] )
			CorrelationAxes.set_yticklabels( [branchname.replace("_"," ") for branchname in branches] )

			CorrelationAxes.annotate("Correlation Matrix: "+label, xy=(0.5, 0.95), xycoords='axes fraction', fontweight='bold', fontsize=10)
			CorrelationAxes.annotate(r"\textbf{\textit{ATLAS}} Internal", xy=(0.6, 0.05), xycoords='axes fraction', fontweight='bold', fontsize=10)

			plt.savefig("plots/var_correlation_%s.pdf"%(label)  )
			# code.interact(local=locals())



		tmpcmap = sns.blend_palette([ (1,1,1,0), colorpal[iSample] + (1,) ], 10)
		tmpcmap =  mpl.colors.ListedColormap(tmpcmap)

		OnePlotFig = plt.figure(figsize=(6, 6), dpi=100, facecolor='white')
		OnePlotAxes  = OnePlotFig.add_axes(rect_scatter)
		OnePlotAxesX = OnePlotFig.add_axes(rect_histx)
		OnePlotAxesY = OnePlotFig.add_axes(rect_histy)

		OnePlotAxesX.yaxis.grid()
		OnePlotAxesY.xaxis.grid()
		OnePlotAxesY.set_xticklabels([])
		OnePlotAxesY.set_yticklabels([])
		OnePlotAxesX.set_xticklabels([])
		OnePlotAxesX.set_yticklabels([])
		OnePlotAxesX.spines['top'].set_visible(False)
		OnePlotAxesY.spines['right'].set_visible(False)
		OnePlotAxes.tick_params(axis='y', direction='out')

		OnePlotAxes.set_xlabel(var1label)
		OnePlotAxes.set_ylabel(var2label)

		N = mytree.GetEntries()

		corrhist = mytree.Draw(vartreeexp+">>htemp111%s(%d,%f,%f,%d,%f,%f)"%
								(MCSample,var1limits[2],var1limits[0],var1limits[1],var2limits[2],var2limits[0],var2limits[1]), 
								selection="%f"%(MCScales[MCSample]), create_hist=True, options="goff") 

		# mytree.GetSelectedRows() 
		y = mytree.GetV1()
		y = copy.deepcopy(scipy.frombuffer(buffer=y,dtype='double',count=1000000 ))
		x = mytree.GetV2()
		x = copy.deepcopy(scipy.frombuffer(buffer=x,dtype='double',count=1000000  ))
		w = mytree.GetW()
		w = copy.deepcopy(scipy.frombuffer(buffer=w,dtype='double',count=1000000  ))

		# print w[:100]
		# print w[-100:]

		# plt.show()
		# code.interact(local=locals())

		# Let's add on other samples that are related
		for (tmpMCSample,tmpNorm, tmpLabel, tmpFirstInCombinedSample) in MCSamples[jSample+1:]:

			if tmpFirstInCombinedSample:
				break
			print "Adding %s"%tmpMCSample

			tmpmytree = MCFiles[tmpMCSample].SR
			corrhist.Add(tmpmytree.Draw(vartreeexp+">>htemp%s(%d,%f,%f,%d,%f,%f)"%
								(tmpMCSample,var1limits[2],var1limits[0],var1limits[1],var2limits[2],var2limits[0],var2limits[1]), 
								selection="%f"%(MCScales[tmpMCSample]), create_hist=True, options="goff")  )

			tmpy = tmpmytree.GetV1()
			y = np.concatenate( (y, copy.deepcopy(scipy.frombuffer(buffer=y,dtype='double',count=mytree.GetSelectedRows()  ) ) ) )
			tmpx = tmpmytree.GetV2()
			x = np.concatenate( (x, copy.deepcopy(scipy.frombuffer(buffer=x,dtype='double',count=mytree.GetSelectedRows()  ) ) ) )
			tmpw = tmpmytree.GetW()
			w = np.concatenate( (w, copy.deepcopy(scipy.frombuffer(buffer=w,dtype='double',count=mytree.GetSelectedRows()  ) ) ) )
			#print mytree.GetSelectedRows() 

		if backgroundcorr:
			backgroundcorr.Add(corrhist)
		else:
			backgroundcorr = corrhist

		OnePlotAxes.annotate("Corr Coeff: %.2f"%(corrhist.GetCorrelationFactor() ) , xy=(0.65, 0.95), xycoords='axes fraction', fontweight='bold', fontsize=8)

		corrhist.Smooth(10,"k5b")

		if 'Phi' in var1:
			OnePlotAxes.set_xticks(radianTickLocations)
			OnePlotAxes.set_xticklabels(radianTickLabels)
			OnePlotAxesX.set_xticks(radianTickLocations)
			# OnePlotAxesX.set_xticklabels(radianTickLabels)

		if 'Phi' in var2:
			OnePlotAxes.set_yticks(radianTickLocations)
			OnePlotAxes.set_yticklabels(radianTickLabels)
			OnePlotAxesY.set_yticks(radianTickLocations)
			# OnePlotAxesY.set_yticklabels(radianTickLabels)

		rplt.contourf(corrhist,axes=OnePlotAxes, cmap=tmpcmap, alpha = 0.9)
		OnePlotAxes.grid(True)

		OnePlotAxesX.hist( x ,var1limits[2], weights=w, range=var1limits[:2] , normed=1, color=colorpal[iSample] )
		OnePlotAxesY.hist( y ,var2limits[2], weights=w, range=var2limits[:2] , normed=1, color=colorpal[iSample]  , orientation='horizontal')

		OnePlotAxesX.annotate("Mean: %.2f"%np.average(x,weights=w) , xy=(0.05, 0.95), xycoords='axes fraction', fontweight='bold', fontsize=8)
		OnePlotAxesY.annotate("Mean: %.2f"%np.average(y,weights=w) , xy=(0.05, 0.95), xycoords='axes fraction', fontweight='bold', fontsize=8)


		OnePlotAxesX.set_xlim(var1limits[:2])
		OnePlotAxesY.set_ylim(var2limits[:2])

		OnePlotAxes.annotate(label, xy=(0.05, 0.95), xycoords='axes fraction', fontweight='bold', fontsize=10)
		OnePlotAxes.annotate(r"\textbf{\textit{ATLAS}} Internal", xy=(0.6, 0.05), xycoords='axes fraction', fontweight='bold', fontsize=10)


		plt.savefig('%s/OneSample_%s_%s_%s_vs_%s.pdf'%(directory,MCSample,label,var1.replace("/","Over") ,var2.replace("/","Over") )  )

		plt.clf()
		plt.close('all')

		if (MCSample,norm, label, firstInCombinedSample) in samplestooverlay:

			alpha = 0.7
			linestyle = 'solid'

			levels = [ round_to_1( MCScales[MCSample]*NEvent[MCSample]* tmpfactor )  for tmpfactor in [ 0.0001,0.001,0.01,0.1]   ]
			
			if colornorm==0:
				colornorm = matplotlib.colors.Normalize(vmin = 0 , vmax = 100, clip = False)

			# plt.grid()
			# # ims[MCSample] = rplt.imshow(a,axes=OverlayAxes, norm = colornorm, cmap = sns.blend_palette(["ghostwhite", colorpal[iSample]], as_cmap=True) , alpha=0.25 )
			ims[MCSample] = rplt.imshow (corrhist,axes=OverlayAxes, norm = colornorm, cmap = sns.blend_palette(["ghostwhite", colorpal[iSample]], as_cmap=True) , alpha=0.25 )
			ctr[MCSample] = rplt.contour(corrhist,axes=OverlayAxes,  linewidth=10, alpha=alpha, linestyles=linestyle , colors = matplotlib.colors.rgb2hex(colorpal[iSample]) ) #, locator=ticker.FixedLocator(levels) )
			plt.clabel(ctr[MCSample], inline=0, inline_spacing=-1, fontsize=10,fmt='%1.0f')
			OverlayAxes.annotate(r"\textbf{\textit{ATLAS}} Internal", xy=(0.65, 0.05), xycoords='axes fraction', fontweight='bold', fontsize=10)

			pass

	OverlayAxes.set_xlim(var1limits[:2])
	OverlayAxes.set_ylim(var2limits[:2])


	tmpRectangle = {}
	for iSample, (MCSample,norm, label, tmp) in enumerate(samplestodraw) :
		tmpRectangle[MCSample] = Rectangle((0, 0), 1, 1, fc=matplotlib.colors.rgb2hex(colorpal[iSample]) )
	OverlayAxes.legend([tmpRectangle[x] for  (x,y,z,x1) in samplestooverlay ], [z for (x,y,z,x1) in samplestooverlay],  loc="best" , borderaxespad=3)
	OverlayAxes.set_xlabel(var1label)
	OverlayAxes.set_ylabel(var2label)

	bkgim = rplt.imshow (backgroundcorr,axes=OverlayAxes, norm = colornorm, cmap = sns.blend_palette(["ghostwhite", colorpal[iSample]], as_cmap=True) , alpha=0.25 )
	bkgcont = rplt.contour(backgroundcorr,axes=OverlayAxes,  linewidth=10, alpha=0.5, linestyles=linestyle , colors = "k") 
	plt.clabel(bkgcont, inline=0, inline_spacing=-1, fontsize=10,fmt='%1.0f')


	OverlayFig.savefig('%s/ContourOverlay_%s_vs_%s.png'%(directory,var1.replace("/","_Over_"),var2.replace("/","_Over_")) )
	plt.clf()
	plt.close('all')

	writeAuxPlots = 0
	writeCorrPlots = 0

	# plt.grid()
	# plt.show()
