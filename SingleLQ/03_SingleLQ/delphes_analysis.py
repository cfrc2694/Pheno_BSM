import os   
import ROOT
from ROOT import *

dir_path = os.path.dirname(os.path.realpath(__file__))
fullAnalysis = True

cutJetPT = 30. #GeV
cutTauPT = 30. #GeV
cutQbPT = 30. #GeV
cutTauETA = 2.4 #rad
cutQbETA = 2.4 #rad

def DeltaR(v1,v2):
	return v1.TLV.DeltaR(v2.TLV)

def DeltaEta(v1,v2):
	return v1.TLV.Eta() - v2.TLV.Eta()

def DeltaPhi(v1,v2):
	return v1.TLV.Phi() - v2.TLV.Phi()
	
class JetVector():
    def __init__(self, tFile, i, j):
        self.TLV=TLorentzVector()
        tFile.GetEntry(i) #Select i-event
        self.TLV.SetPtEtaPhiM(#getparameters jet
            tFile.GetLeaf("Jet.PT").GetValue(j), 
            tFile.GetLeaf("Jet.Eta").GetValue(j), 
            tFile.GetLeaf("Jet.Phi").GetValue(j), 
            tFile.GetLeaf("Jet.Mass").GetValue(j)
        )
        self.Q = tFile.GetLeaf("Jet.Charge").GetValue(j)
        self.BTag   = tFile.GetLeaf("Jet.BTag").GetValue(j)
        self.TauTag = tFile.GetLeaf("Jet.TauTag").GetValue(j)

class GenJetVector():
    def __init__(self, tFile, i, j):
        self.TLV=TLorentzVector()
        tFile.GetEntry(i) #Select i-event
        self.TLV.SetPtEtaPhiM(#getparameters GenJet
            tFile.GetLeaf("GenJet.PT").GetValue(j), 
            tFile.GetLeaf("GenJet.Eta").GetValue(j), 
            tFile.GetLeaf("GenJet.Phi").GetValue(j), 
            tFile.GetLeaf("GenJet.Mass").GetValue(j)
        )
        self.Q = tFile.GetLeaf("GenJet.Charge").GetValue(j)
        self.BTag   = tFile.GetLeaf("GenJet.BTag").GetValue(j)
        self.TauTag = tFile.GetLeaf("GenJet.TauTag").GetValue(j)

def PT(jet):
  return jet.TLV.Pt()


def main():
    #READ Folder
    entries = []
    #entries.append("lq_mzp250_mlq250")
    #entries.append("lq_mzp1000_mlq1000" )
    entries.append("lq_mzp2000_mlq2000" ) 
    #entries.append("lq_mzp3000_mlq3000")
    jobs = []
    for folder in entries:
        dir_name = os.getcwd() + "/Events"
        print("runs found in: "+dir_name)
        if (fullAnalysis): jobs.append( len(os.walk(dir_name).next()[1]) )
        else: jobs.append(1)
    print(jobs)


    c1 = ROOT.TCanvas("c1", "Titulo")  
    c1.SetGrid()
    for n_signal, signal in enumerate(entries):
        pt_all_jets=TH1F("pt_all_jets", "Pt_{allj}", 100, 0.0, 1000.0)
        eta_all_jets=TH1F("plot_eta_js", "#eta_{allj}", 100, -5, 5)
        pt_all_jets.SetLineColor(kBlack)
        eta_all_jets.SetLineColor(kBlack)
        
        pt_lead_jets=TH1F("pt_lead_jets", "Pt_{j1}", 100, 0.0, 1000.0)
        eta_lead_jets=TH1F("plot_eta_j1", "#eta_{j1}", 100, -5, 5)
        pt_lead_jets.SetLineColor(kBlue)
        eta_lead_jets.SetLineColor(kBlue)
        pt_lead_bjets=TH1F("pt_lead_bjets", "Pt_{bj1}", 100, 0.0, 1000.0)
        eta_lead_bjets=TH1F("plot_eta_bj", "#eta_{bj2}", 100, -5, 5)
        pt_lead_bjets.SetLineColor(kRed)
        eta_lead_bjets.SetLineColor(kRed)
        pt_lead_taus=TH1F("pt_lead_taus", "Pt_{tau1}", 100, 0.0, 1000.0)
        eta_lead_taus=TH1F("plot_eta_ta1", "#eta_tau1", 100, -5, 5)
        pt_lead_taus.SetLineColor(kGreen)
        eta_lead_taus.SetLineColor(kGreen)
        pt_slead_taus=TH1F("pt_slead_taus", "Pt_tau2", 100, 0.0, 1000.0)
        eta_slead_taus=TH1F("plot_eta_ta2", "#eta_tau2", 100, -5, 5)
        pt_slead_taus.SetLineColor(kViolet)
        eta_slead_taus.SetLineColor(kViolet)
        
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
        
        eff=TH1F("eff", "eff", 6, -1, 5)
        
        signal_entries=0
        Least_One_Jet=0
        Least_Jet_and_BJet=0
        Least_Jet_and_BJet_and_Tau=0
        Least_Jet_and_BJet_and_twoTau=0
        for ind in range(1,jobs[n_signal]+1):
            directory= str("Events/run_" + '%02d' % ind +"/tag_1_delphes_events.root")
            File = ROOT.TChain("Delphes;1")
            File.Add(directory)
            Number = File.GetEntries()
            signal_entries+=Number
            #print("found " + str(Number) + " entries in: " + directory)
            for i in range(Number):
                File.GetEntry(i)#Select i-event
                NumberJets = File.Jet.GetEntries() #Number of GenJets in i-Entry
                eff.Fill(-1)
                if (NumberJets>=4):
                    
                    allJ = []
                    jets = []
                    bjets = []
                    taus = []
                    for j in range(NumberJets):
                        jet=JetVector(File, i, j)
                        if (jet.TLV.Pt()> 20.):
                            allJ.append(jet)
                            if( jet.BTag==0 and jet.TauTag==0):
                                if (abs(jet.TLV.Pt())>20.0 ):
                                    jets.append(jet)
                            elif( jet.BTag==1 and jet.TauTag==0): 
                                if ( abs(jet.TLV.Eta())<2.4 ):
                                    bjets.append(jet)
                            elif( jet.BTag==0 and jet.TauTag==1): 
                                if ( abs(jet.TLV.Eta())<2.4 ):
                                    taus.append(jet)
                    allJ.sort( reverse = True, key=PT)
                    jets.sort( reverse = True, key=PT)
                    bjets.sort(reverse = True, key=PT)
                    taus.sort( reverse = True, key=PT)
                    eff.Fill(0)
                    
                    if (len(jets)>=1):
                        Least_One_Jet+=1
                        eff.Fill(1)
                        if(len(bjets)>=1):
                            Least_Jet_and_BJet+=1
                            eff.Fill(2)
                            if( len(taus)>0 ):
                                Least_Jet_and_BJet_and_Tau+=1
                                eff.Fill(3)
                                if(len(taus)>1):
                                    Least_Jet_and_BJet_and_twoTau+=1
                                    eff.Fill(4)
                                    pt_lead_jets.Fill(jets[0].TLV.Pt())
                                    eta_lead_jets.Fill(jets[0].TLV.Eta())
                                    pt_lead_bjets.Fill(bjets[0].TLV.Pt())
                                    eta_lead_bjets.Fill(bjets[0].TLV.Eta())
                                    pt_lead_taus.Fill(taus[0].TLV.Pt())
                                    eta_lead_taus.Fill(taus[0].TLV.Eta())
                                    pt_slead_taus.Fill(taus[1].TLV.Pt())
                                    eta_slead_taus.Fill(taus[1].TLV.Eta())
                                    #######
                                    pt_all_jets.Fill ( bjets[0].TLV.Pt()  )
                                    eta_all_jets.Fill( bjets[0].TLV.Eta() )
                                    pt_all_jets.Fill ( taus[0].TLV.Pt()  )
                                    eta_all_jets.Fill( taus[0].TLV.Eta() )
                                    pt_all_jets.Fill ( taus[1].TLV.Pt()  )
                                    eta_all_jets.Fill( taus[1].TLV.Eta() )
                                    
                                    pt_all_jets.Fill ( jets[0].TLV.Pt()   )
                                    eta_all_jets.Fill( jets[0].TLV.Eta()  )
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
                    

                if(i%500==0):
                    eta_all_jets.Draw("Hist")
                    eta_lead_jets.Draw("histsame")
                    eta_lead_bjets.Draw("histsame")
                    eta_lead_taus.Draw("histsame")
                    eta_slead_taus.Draw("histsame")
                    gPad.Update()
        print("Rate of events with  with at least one jet\n")    
        print(str(Least_One_Jet*100./signal_entries)+"%")
        print("=============")
        print("Rate of events with  with at least one jet and one bJet\n")    
        print(str(Least_Jet_and_BJet*100./signal_entries)+"%")
        print("=============")
        print("Rate of events with  with at least one jet and one bJet and ONE tau\n")    
        print(str(Least_Jet_and_BJet_and_Tau*100./signal_entries)+"%")        
        print("=============")
        print("Rate of events with  with at least one jet and one bJet and TWO tau\n")    
        print(str(Least_Jet_and_BJet_and_twoTau*100./signal_entries)+"%")       
        

        
        pt_all_jets.Draw("HIST")
        pt_lead_jets.Draw("histsame")
        pt_lead_bjets.Draw("histsame")
        pt_lead_taus.Draw("histsame")
        pt_slead_taus.Draw("histsame")

        leg=ROOT.TLegend(0.9,0.9,0.65,0.70)
        leg.AddEntry("pt_all_jets", "jets+bjets+#tau jets", "l")
        leg.AddEntry("pt_lead_jets", "jet", "l")
        leg.AddEntry("pt_lead_bjets", "bjet", "l")
        leg.AddEntry("pt_lead_taus", "#tau_{1} jet", "l")
        leg.AddEntry("pt_slead_taus", "#tau_{2} jet", "l")
        leg.Draw()
        
        c1.SaveAs(signal+"Hadron_Pt.pdf")
        
        eta_all_jets.Draw("HIST")
        eta_lead_jets.Draw("histsame")
        eta_lead_bjets.Draw("histsame")
        eta_lead_taus.Draw("histsame")
        eta_slead_taus.Draw("histsame")
        leg=ROOT.TLegend(0.9,0.9,0.65,0.70)
        leg.AddEntry("pt_all_jets", "jets+bjets+#tau jets", "l")
        leg.AddEntry("pt_lead_jets", "jet", "l")
        leg.AddEntry("pt_lead_bjets", "bjet", "l")
        leg.AddEntry("pt_lead_taus", "#tau_{1} jet", "l")
        leg.AddEntry("pt_slead_taus", "#tau_{2} jet", "l")
        leg.Draw()
        c1.SaveAs("Hadron_Eta.pdf")
        eff.Draw("HIST")
        c1.SaveAs("Eff_hadron.pdf")
        
        c=c1
        hist_deltar_taus.Draw("hist")
        c.SaveAs("Hadron_deltar_taus.pdf")
        hist_deltar_taus.Draw()
        c.SaveAs("Hadron_deltar_taus.pdf")
        hist_deltar_b_ltau.Draw()
        c.SaveAs("Hadron_deltar_b_ltau.pdf")
        hist_deltar_b_sltau.Draw()
        c.SaveAs("Hadron_deltar_b_sltau.pdf")
        hist_deltar_j_ltau.Draw()
        c.SaveAs("Hadron_deltar_j_ltau.pdf")
        hist_deltar_j_sltau.Draw()
        c.SaveAs("Hadron_deltar_j_sltau.pdf")
        hist_deltar_b_j.Draw()
        c.SaveAs("Hadron_deltar_b_j.pdf")
        
        hist_deltaEta_taus.Draw("hist")
        c.SaveAs("Hadron_deltaEta_taus.pdf")
        hist_deltaEta_taus.Draw()
        c.SaveAs("Hadron_deltaEta_taus.pdf")
        hist_deltaEta_b_ltau.Draw()
        c.SaveAs("Hadron_deltaEta_b_ltau.pdf")
        hist_deltaEta_b_sltau.Draw()
        c.SaveAs("Hadron_deltaEta_b_sltau.pdf")
        hist_deltaEta_j_ltau.Draw()
        c.SaveAs("Hadron_deltaEta_j_ltau.pdf")
        hist_deltaEta_j_sltau.Draw()
        c.SaveAs("Hadron_deltaEta_j_sltau.pdf")
        hist_deltaEta_b_j.Draw()
        c.SaveAs("Hadron_deltaEta_b_j.pdf")

        hist_deltaPhi_taus.Draw("hist")
        c.SaveAs("Hadron_deltaPhi_taus.pdf")
        hist_deltaPhi_taus.Draw()
        c.SaveAs("Hadron_deltaPhi_taus.pdf")
        hist_deltaPhi_b_ltau.Draw()
        c.SaveAs("Hadron_deltaPhi_b_ltau.pdf")
        hist_deltaPhi_b_sltau.Draw()
        c.SaveAs("Hadron_deltaPhi_b_sltau.pdf")
        hist_deltaPhi_j_ltau.Draw()
        c.SaveAs("Hadron_deltaPhi_j_ltau.pdf")
        hist_deltaPhi_j_sltau.Draw()
        c.SaveAs("Hadron_deltaPhi_j_sltau.pdf")
        hist_deltaPhi_b_j.Draw()
        c.SaveAs("Hadron_deltaPhi_b_j.pdf")
        
        print("Total Entries for " + signal + ": " + str(signal_entries)) 
        
if __name__ == '__main__':
    main()
