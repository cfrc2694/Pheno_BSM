from lhereader import readLHEF  
import os
import math
import ROOT
from ROOT import TH1F  
from ROOT import kBlack, kBlue, kRed, kGreen, kViolet

def DeltaR(v1,v2):
	return v1.TLV.DeltaR(v2.TLV)

def DeltaEta(v1,v2):
	return v1.TLV.Eta() - v2.TLV.Eta()

def DeltaPhi(v1,v2):
	return v1.TLV.Phi() - v2.TLV.Phi()

dir_name = os.getcwd() + "/Events"
print(dir_name)
jobs = len(os.walk(dir_name).next()[1])

c=ROOT.TCanvas()
c.SetGrid()

eff=TH1F("eff", "eff", 7, 0, 7)

a=0
b=0

hist_pt_all_jet=TH1F("pt_all_jet", "pt_{Parton}",100,30,800)
hist_pt_all_jet.SetLineColor(kBlack)

hist_pt_lead_jet=TH1F("pt_lead_j", "pt_{j}",100,30,800)
hist_pt_lead_jet.SetLineColor(kBlue)

hist_pt_lead_bjet=TH1F("pt_lead_b", "pt_{b}",100,30,800)
hist_pt_lead_bjet.SetLineColor(kRed)

hist_pt_lead_tau=TH1F("pt_lead_tau", "pt_{#tau}",100,30,800)
hist_pt_lead_tau.SetLineColor(kGreen)

hist_pt_sublead_tau=TH1F("pt_sublead_tau", "pt_{#tau_2}",100,30,800)
hist_pt_sublead_tau.SetLineColor(kViolet)




hist_eta_all_jet=TH1F("eta_all_j", "\eta_{Parton}",100,-5,5) 
hist_eta_all_jet.SetLineColor(kBlack)

hist_eta_lead_jet=TH1F("eta_lead_j", " ",100,-5,5) 
hist_eta_lead_jet.SetLineColor(kBlue)

hist_eta_lead_bjet=TH1F("eta_lead_b", " ",100,-5,5) 
hist_eta_lead_bjet.SetLineColor(kRed)

hist_eta_lead_tau=TH1F("eta_lead_tau", " ",100,-5,5) 
hist_eta_lead_tau.SetLineColor(kGreen)

hist_eta_sublead_tau=TH1F("eta_sublead_tau", " ",100,-5,5) 
hist_eta_sublead_tau.SetLineColor(kViolet)


hist_sdpt_taus=TH1F("sdpt_taus", "#Delta Pt_{#tau_{1}#tau_{2}}",100,0,1000)

hist_deltar_taus=TH1F("deta_taus","#Delta R_{#tau_{1}#tau_{2}}",100,0,8) 
hist_deltar_b_ltau=TH1F("deltar_b_ltau","#Delta R_{b#tau_{1}}",100,0,8) 
hist_deltar_b_sltau=TH1F("deltar_b_sltau","#Delta R_{b#tau_{2}}",100,0,8) 
hist_deltar_j_ltau=TH1F("deltar_j_ltau","#Delta R_{j#tau_{1}}",100,0,8) 
hist_deltar_j_sltau=TH1F("deltar_j_sltau","#Delta R_{j#tau_{2}}",100,0,8) 
hist_deltar_b_j=TH1F("deltar_b_j","#Delta R_{bj}",100,0,8)

hist_deltaEta_taus=TH1F("deltaEta_taus","#Delta #eta_{#tau_{1}#tau_{2}}",100,-5,5) 
hist_deltaEta_b_ltau=TH1F("deltaEta_b_ltau","#Delta #eta_{b#tau_{1}}",100,-5,5) 
hist_deltaEta_b_sltau=TH1F("deltaEta_b_sltau","#Delta #eta_{b#tau_{2}}",100,-5,5) 
hist_deltaEta_j_ltau=TH1F("deltaEta_j_ltau","#Delta #eta_{j#tau_{1}}",100,-5,5) 
hist_deltaEta_j_sltau=TH1F("deltaEta_j_sltau","#Delta #eta_{j#tau_{2}}",100,-5,5) 
hist_deltaEta_b_j=TH1F("deltaEta_b_j","#Delta #eta_{bj}",100,-5,5)

hist_deltaPhi_taus=TH1F("deltaPhi_taus","#Delta #phi_{#tau_{1}#tau_{2}}",100,-5,5) 
hist_deltaPhi_b_ltau=TH1F("deltaPhi_b_ltau","#Delta #phi_{b#tau_{1}}",100,-5,5) 
hist_deltaPhi_b_sltau=TH1F("deltaPhi_b_sltau","#Delta #phi_{b#tau_{2}}",100,-5,5) 
hist_deltaPhi_j_ltau=TH1F("deltaPhi_j_ltau","#Delta #phi_{j#tau_{1}}",100,-5,5) 
hist_deltaPhi_j_sltau=TH1F("deltaPhi_j_sltau","#Delta #phi_{j#tau_{2}}",100,-5,5) 
hist_deltaPhi_b_j=TH1F("deltaPhi_b_j","#Delta #phi_{bj}",100,-5,5)

for ind in range(1,jobs+1):
	os.system("gzip -d Events/run_" + '%02d' % ind + "/unweighted_events.lhe.gz")
	data=readLHEF( "Events/run_" + '%02d' % ind + "/unweighted_events.lhe")

	for event in data.events:
		bjets=event.getParticlesByIDs([-5,5])
		jets=event.getParticlesByIDs([-4,-3,-2,-1,1,2,3,4,21])
		taus=event.getParticlesByIDs([-15,15])
		a+=1
		eff.Fill(0)
		if len(jets)==1 :
			if(jets[0].pt>30 and abs(jets[0].eta)>0.0):
				eff.Fill(1)
				if len(bjets)==1:
						eff.Fill(2)
						if( bjets[0].pt >30 and abs(bjets[0].eta)<2.4 ):
							eff.Fill(3)
							if len(taus)==2 :
								if taus[0].pt <  taus[1].pt :
									taus[0] , taus[1] = taus[1] , taus[0]
								eff.Fill(4)
								if(abs(taus[0].eta)<2.4 and abs(taus[1].eta) < 2.4):
									if (abs(taus[0].pt)>30. and taus[1].pt > 30. ):				
										eff.Fill(5)
										b+=1
										
										hist_pt_all_jet.Fill(bjets[0].pt)
										hist_pt_lead_bjet.Fill(bjets[0].pt)
										
										hist_pt_all_jet.Fill(jets[0].pt)
										hist_pt_lead_jet.Fill(jets[0].pt)
										
										hist_pt_all_jet.Fill(taus[0].pt)
										hist_pt_lead_tau.Fill(taus[0].pt)
								
										hist_pt_all_jet.Fill(taus[1].pt)
										hist_pt_sublead_tau.Fill(taus[1].pt)
								
										hist_sdpt_taus.Fill(taus[0].pt-taus[1].pt)

										hist_eta_all_jet.Fill(bjets[0].eta)
										hist_eta_lead_bjet.Fill(bjets[0].eta)

										hist_eta_all_jet.Fill(jets[0].eta)
										hist_eta_lead_jet.Fill(jets[0].eta)

										hist_eta_all_jet.Fill(taus[0].eta)
										hist_eta_lead_tau.Fill(taus[0].eta)

										hist_eta_all_jet.Fill(taus[1].eta)
										hist_eta_sublead_tau.Fill(taus[1].eta)
										
										hist_deltar_taus.Fill(DeltaR(taus[0],taus[1]))
										hist_deltar_b_ltau.Fill(DeltaR(taus[0],bjets[0]))
										hist_deltar_b_sltau.Fill(DeltaR(taus[1],bjets[0]))
										hist_deltar_j_ltau.Fill(DeltaR(taus[0],jets[0]))
										hist_deltar_j_sltau.Fill(DeltaR(taus[1],jets[0]))
										hist_deltar_b_j.Fill(DeltaR(bjets[0],jets[0]))

										hist_deltaEta_taus.Fill(DeltaEta(taus[0],taus[1]))
										hist_deltaEta_b_ltau.Fill(DeltaEta(taus[0],bjets[0]))
										hist_deltaEta_b_sltau.Fill(DeltaEta(taus[1],bjets[0]))
										hist_deltaEta_j_ltau.Fill(DeltaEta(taus[0],jets[0]))
										hist_deltaEta_j_sltau.Fill(DeltaEta(taus[1],jets[0]))
										hist_deltaEta_b_j.Fill(DeltaEta(bjets[0],jets[0]))

										hist_deltaPhi_taus.Fill(DeltaPhi(taus[0],taus[1]))
										hist_deltaPhi_b_ltau.Fill(DeltaPhi(taus[0],bjets[0]))
										hist_deltaPhi_b_sltau.Fill(DeltaPhi(taus[1],bjets[0]))
										hist_deltaPhi_j_ltau.Fill(DeltaPhi(taus[0],jets[0]))
										hist_deltaPhi_j_sltau.Fill(DeltaPhi(taus[1],jets[0]))
										hist_deltaPhi_b_j.Fill(DeltaPhi(bjets[0],jets[0]))										

hist_pt_all_jet.Draw("hist")
hist_pt_lead_jet.Draw("histsame")
hist_pt_lead_bjet.Draw("histsame")
hist_pt_lead_tau.Draw("histsame")
hist_pt_sublead_tau.Draw("histsame")

leg=ROOT.TLegend(0.9,0.9,0.65,0.70)
leg.AddEntry("pt_all_jet", "jets+bjets+#tau jets", "l")
leg.AddEntry("pt_lead_j", "jet", "l")
leg.AddEntry("pt_lead_b", "bjet", "l")
leg.AddEntry("pt_lead_tau", "#tau_{1} jet", "l")
leg.AddEntry("pt_sublead_tau", "#tau_{2} jet", "l")
leg.Draw()
c.SaveAs("Parton_pt.pdf")

hist_eta_all_jet.Draw("hist")
hist_eta_lead_jet.Draw("histsame")
hist_eta_lead_bjet.Draw("histsame")
hist_eta_lead_tau.Draw("histsame")
hist_eta_sublead_tau.Draw("histsame")

leg=ROOT.TLegend(0.9,0.9,0.65,0.70)
leg.AddEntry("eta_all_jet", "jets+bjets+#tau", "l")
leg.AddEntry("eta_lead_j", "jets", "l")
leg.AddEntry("eta_lead_b", "bjets", "l")
leg.AddEntry("eta_lead_tau", "#tau1 jet", "l")
leg.AddEntry("eta_sublead_tau", "#tau2 jet", "l")
leg.Draw()
c.SaveAs("Parton_eta.pdf")

hist_sdpt_taus.Draw("hist")
c.SaveAs("Parton_sdpt_taus.pdf")

hist_deltar_taus.Draw("hist")
c.SaveAs("Parton_deltar_taus.pdf")
hist_deltar_taus.Draw()
c.SaveAs("Parton_deltar_taus.pdf")
hist_deltar_b_ltau.Draw()
c.SaveAs("Parton_deltar_b_ltau.pdf")
hist_deltar_b_sltau.Draw()
c.SaveAs("Parton_deltar_b_sltau.pdf")
hist_deltar_j_ltau.Draw()
c.SaveAs("Parton_deltar_j_ltau.pdf")
hist_deltar_j_sltau.Draw()
c.SaveAs("Parton_deltar_j_sltau.pdf")
hist_deltar_b_j.Draw()
c.SaveAs("Parton_deltar_b_j.pdf")

hist_deltaEta_taus.Draw("hist")
c.SaveAs("Parton_deltaEta_taus.pdf")
hist_deltaEta_taus.Draw()
c.SaveAs("Parton_deltaEta_taus.pdf")
hist_deltaEta_b_ltau.Draw()
c.SaveAs("Parton_deltaEta_b_ltau.pdf")
hist_deltaEta_b_sltau.Draw()
c.SaveAs("Parton_deltaEta_b_sltau.pdf")
hist_deltaEta_j_ltau.Draw()
c.SaveAs("Parton_deltaEta_j_ltau.pdf")
hist_deltaEta_j_sltau.Draw()
c.SaveAs("Parton_deltaEta_j_sltau.pdf")
hist_deltaEta_b_j.Draw()
c.SaveAs("Parton_deltaEta_b_j.pdf")

hist_deltaPhi_taus.Draw("hist")
c.SaveAs("Parton_deltaPhi_taus.pdf")
hist_deltaPhi_taus.Draw()
c.SaveAs("Parton_deltaPhi_taus.pdf")
hist_deltaPhi_b_ltau.Draw()
c.SaveAs("Parton_deltaPhi_b_ltau.pdf")
hist_deltaPhi_b_sltau.Draw()
c.SaveAs("Parton_deltaPhi_b_sltau.pdf")
hist_deltaPhi_j_ltau.Draw()
c.SaveAs("Parton_deltaPhi_j_ltau.pdf")
hist_deltaPhi_j_sltau.Draw()
c.SaveAs("Parton_deltaPhi_j_sltau.pdf")
hist_deltaPhi_b_j.Draw()
c.SaveAs("Parton_deltaPhi_b_j.pdf")

scale=eff.Integral()
eff.Scale(100./a)
eff.Draw("hist")
print 100.*b/a
c.SaveAs("eff_parton.pdf")
raw_input("Press Enter to finish...")
