import os
import ROOT
from ROOT import TGraphErrors, TGraph, gStyle, kOcean
from lxml import html
from array import array 

#get mainfolder
dir_path = os.path.dirname(os.path.realpath(__file__))
#madgraph folder relative to the mainfolder
madfolder="../MG5_aMC_v2_9_4/bin/mg5_aMC"
#==================================================
#Mass Range, from 250GeV to 3.00 TeV, in steps of
#250.geV. Using 24 cores to calculate
Mmin = 250.#GeV
Mmax = 3500.#GeV
Mstep = 12.5#GeV
Nsteps=(Mmax-Mmin)/Mstep
ncores =24
nevents=1000
KappaZp=2.42
runmg5=False
#==================================================
#Function to read the cross section table from HTML
#crossxhtml inside the output folder
def read_HTML(route_HTML):
	data_Xpath = '//tr/td/center/a/text()'
	parsed_HTML = html.parse(route_HTML).getroot()
	data_HTML = parsed_HTML.xpath(data_Xpath)
	mass = []
	errorMass = []
	dato = []
	error = []
	data_HTML = [float(x) for x in data_HTML]
	for i in range(int(len(data_HTML)/2)):
		mass.append(Mmin + i*Mstep)
		errorMass.append(0)
		dato.append(data_HTML[i*2])
		error.append(data_HTML[(i*2)+1])
	x  = array( 'f', mass )
	ex = array( 'f', errorMass )
	y  = array( 'f', dato )
	ey = array( 'f', error)
	n=len(dato)
	graph=TGraph(n, x, y)
	return graph
#==================================================
#---
#==================================================
#Import Madgraph Model to *.mg5 files
def header(f):
	f.write("import model Mod_VLQ_UFO/") 
	f.write("\ndefine ta = ta+ ta-") 
	f.write("\ndefine qb = b b~") 
	f.write("\ndefine lq = vlq vlq~") 
#==================================================
#---
#==================================================
#Print events generator to *.mg5 files
def events(f, outputName, useBR,kappa):
	f.write("\noutput d"+outputName + " -nojpeg")
	for i in range(int(Nsteps)+1):
		f.write("\nlaunch -m d" + outputName)
		f.write("\n" + str(ncores))
		f.write("\n0\nset nevents "+str(nevents))
		if useBR:
			f.write("\n"+dir_path+"/BR_LQ/Events/run_")
			if i<9: 
				f.write("0"+str(i+1))
			else: 
				f.write(str(i+1))
			f.write("/param_card.dat")
		else:
			Mass= Mmin + i*Mstep
			f.write("\nset MVLQ "+str(Mass))		
			f.write("\nset MZP "+str(Mass))
		f.write("\nset KAPPAZP "+str(kappa))
		f.write("\n0\n")
	f.write("\nexit")
#==================================================
#---
#==================================================
#Run mg5 folder and delete the aux files
def execmadgraph(run_mg5, generatOutput):
	if (run_mg5): 
		os.system("./" + madfolder + " " + generatOutput + ".mg5")
		os.system("rm -rf " + generatOutput + "/Events")
		os.system("rm -rf " + generatOutput + "/bin")
		os.system("rm -rf " + generatOutput + "/Source")
		os.system("rm -rf " + generatOutput + "/lib")
#==================================================
#=======Calculating Branching Ratios to LQ=========
#==================================================
#Generating Branching Ratios output with MadGraph
BR_VLQ = open("BR_VLQ.mg5", "w")
BR_VLQ_output="BR_LQ"
header(BR_VLQ)#Import Model to BR
BR_VLQ.write("\ngenerate vlq > all all")
BR_VLQ.write("\nadd process zp > all all")
BR_VLQ.write("\nadd process gp > all all")
BR_VLQ.write("\noutput "+BR_VLQ_output+ " -nojpeg")
BR_VLQ.write("\nexit")
BR_VLQ.close()
#Calculate decay widths with MadEvents
BR_VLQ = open("BR_VLQ.me", "w")
for i in range(int(Nsteps)+1):
	Mass= Mmin + i*Mstep
	BR_VLQ.write("\ncalculate_decay_widths")
	BR_VLQ.write("\n0")
	BR_VLQ.write("\nset MVLQ "+str(Mass))
	BR_VLQ.write("\nset MZP "+str(Mass))
	BR_VLQ.write("\n0\n")
BR_VLQ.write("\nexit")
BR_VLQ.close()
if (runmg5):
	os.system("./" + madfolder + " " + "BR_VLQ.mg5")
	os.system("./BR_LQ/bin/madevent BR_VLQ.me")
dir_name = os.path.dirname(os.path.realpath(__file__)) + "/BR_LQ/Events"
for i in range(int(Nsteps)+1):
	Mass= Mmin + i*Mstep
	paramfolder="paramcards/M"+str(Mass)
	os.system("mkdir -p "+paramfolder)
	os.system("cp "+dir_name+"/run_" + '%02d' % (i+1)+"/param_card.dat "+paramfolder)

#==================================================
#---
c1 = ROOT.TCanvas("c1", "Titulo")
gStyle.SetPalette(kOcean)
leg=ROOT.TLegend(0.1,0.1,0.42,0.38)
c1.SetLogy()
#c1.SetLogx()
c1.SetGrid()
Graphs = []
Names = []
step=0
#==================================================
#=======Calculating Cross Section to LQ============
#==================================================
#Events to single leptoquark
#include Calculated decay widths
#include Calculated Zp coupling
#dont Decay leptoquark
generatOutput= '%02d' % step + "_SingleLQ"#name of output
generator=open(generatOutput+".mg5","w")
header(generator)#import model
generator.write("\ngenerate p p > j ta lq QCD=0")#add process
events(generator, generatOutput, True,KappaZp)#set run instructions
generator.close()
execmadgraph(runmg5, generatOutput)#execute Madgraph iif runmg5=True
#read  cross section from crossx.html retirning a TGraph
routeHTML = dir_path+"/d"+generatOutput+"/crossx.html"
Graphs.append(read_HTML( routeHTML )) #save the TGraph
#setting the TGraph plot
Graphs[step].GetYaxis().SetRangeUser(1e-9,2e3)
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetMarkerColor( 4 )
Graphs[step].SetLineColor( 4 )
Graphs[step].SetLineStyle(1)
Graphs[step].SetLineWidth(2)
Graphs[step].SetMarkerStyle( 20 )
Graphs[step].Draw("al")
leg.AddEntry(Names[step], "j ta lq QCD=0", "l")
#==================================================
#Events to single leptoquark
#include Calculated decay widths
#dont include Calculated Zp coupling
step+=1
generatOutput= '%02d' % step + "_SingleLQ_notZP"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > j ta lq QCD=0")
events(generator, generatOutput, True,0*KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineColor(4)
Graphs[step].SetLineStyle(8)
Graphs[step].SetMarkerStyle(1)
Graphs[step].SetLineWidth(2)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "j ta lq QCD=0, Kz=0", "l")
#==================================================
#Events to Double leptoquark
#include Calculated decay widths
#include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > lq lq QCD=0")
events(generator, generatOutput, True,KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineColor(8)
Graphs[step].SetLineWidth(2)
Graphs[step].SetLineStyle(1)
Graphs[step].SetMarkerStyle(22)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "lq lq QCD=0", "l")
#==================================================
#Events to Double leptoquark
#include Calculated decay widths
#dont include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ_notZP"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > lq lq QCD=0")
events(generator, generatOutput, True,0*KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineColor(8)
Graphs[step].SetLineWidth(2)
Graphs[step].SetLineStyle(8)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "lq lq QCD=0, Kz=0", "l")
#==================================================
#Events to Double leptoquark vbf
#include Calculated decay widths
#include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ_VBF"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ndefine j = j ta") 
generator.write("\ngenerate p p > j j lq lq QCD=0")
events(generator, generatOutput, True,KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineStyle(1)
Graphs[step].SetMarkerStyle(23)
Graphs[step].SetMarkerColor(6)
Graphs[step].SetLineWidth(2)
Graphs[step].SetLineColor(6)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "j j lq lq QCD=0", "l")
#==================================================
#Events to Double leptoquark vfb
#include Calculated decay widths
#dont include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ_VBF_notZP"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > j j lq lq QCD=0")
events(generator, generatOutput, True,0*KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineColor(6)
Graphs[step].SetLineWidth(2)
Graphs[step].SetLineStyle(8)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "j j lq lq QCD=0, Kz=0", "l")
#==================================================
#Events to Double leptoquark
#include Calculated decay widths
#include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ_IncludeGluons"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > lq lq")
events(generator, generatOutput, True,KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineStyle(1)
Graphs[step].SetLineWidth(2)
Graphs[step].SetMarkerStyle(33)
Graphs[step].SetMarkerColor(46)
Graphs[step].SetLineColor(46)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "lq lq", "l")
#==================================================
#Events to Double leptoquark
#include Calculated decay widths
#dont include Zp coupling
step+=1
generatOutput= '%02d' % step + "_DoubleLQ_notZP_IncludeGluons"
generator=open(generatOutput+".mg5","w")
header(generator)
generator.write("\ngenerate p p > lq lq")
events(generator, generatOutput, True,0*KappaZp)
generator.close()
execmadgraph(runmg5, generatOutput)
Graphs.append(read_HTML(dir_path+"/d"+generatOutput+"/crossx.html"))
Names.append(generatOutput)
Graphs[step].SetName( Names[step])
Graphs[step].SetTitle( generatOutput )
Graphs[step].SetLineColor(46)
Graphs[step].SetLineWidth(2)
Graphs[step].SetLineStyle(8)
Graphs[step].Draw("l")
leg.AddEntry(Names[step], "lq lq, Kz=0", "l")
leg.Draw()
c1.Update()
c1.SaveAs("cross.pdf")
raw_input("Press Enter to finish...")
