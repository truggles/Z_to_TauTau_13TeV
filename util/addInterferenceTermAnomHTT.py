import ROOT
import os

# Script to add the interferance terms for aHTT analysis
# This is based off of email from Yurii July 24, 2017
#
# qqH_htt_0MintP125 and qqH_htt_0MintN125
# 
# The former is a histogram with positive bins in a histogram obtained by subtracting qqH_htt125 
# and qqH_htt_0M125 (negative bins should be set to 0), and the second histogram would 
# contain only negative bins in the histogram obtained by subtracting qqH_htt125 and qqH_htt_0M125. 
# The content of the negative bins should be multiplied by -1, 
# to ensure that every bin in qqH_htt_0MintP125 and qqH_htt_0MintN125 is either positive or zero.
# 
# By construction, qqH_htt_0MintP125 - qqH_htt_0MintN125 = qqH_htt125 - qqH_htt_0M125

# Can use to return all hists in a dir
def get_Keys_Of_Class( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys

# toMatch = previously selected name, SM
#   will inlclude uncertainty names
# sample = BSM sample name
def get_key_matching_inputs( histKeys, baseToMatch, toMatch, sample ) :

    shapeUncert = ''
    if baseToMatch != toMatch : # (shape uncert)
        shapeUncert = toMatch.replace( baseToMatch, '' )

    for k in histKeys :
        hName = k.GetName()
        if baseToMatch == toMatch : # (not shape uncert)
            #print "not shape uncert"
            if hName == sample : return k
        elif baseToMatch != toMatch : # (shape uncert)
            #print "shape uncert hist: %s   uncert tgt: %s  samp: %s" % (hName, shapeUncert, sample)
            if sample in hName and shapeUncert in hName : return k
    print "No matching hist found, baseToMatch: %s toMatch: %s and sample: %s" % (baseToMatch, toMatch, sample)
    return None


if '__main__' in __name__ :
    channels = ['tt',]
    #cats = ['inclusive', '0jet', 'boosted',
    cats = ['0jet', 'boosted',
        'vbf',
        'vbf_DCP_neg1to0',
        'vbf_DCP_0to1',
        'vbf_D0_0to0p2',
        'vbf_D0_0p2to0p4',
        #'vbf_D0_0p4to0p6',
        'vbf_D0_0p4to0p8',
        #'vbf_D0_0p6to0p8',
        'vbf_D0_0p8to1',
    ]
    catBases = []
    for channel in channels :
        for cat in cats :
            catBases.append(channel+'_'+cat)
            catBases.append(channel+'_'+cat+'_qcd_cr')
    

    base = os.getenv('CMSSW_BASE')
    print base
    base += '/src/Z_to_TauTau_13TeV/httShapes/htt/'

    for signal in ['qqH', 'WH', 'ZH'] :

        # More looping
        #smBaseSample =  signal+'_htt125' # standard SM signal
        smBaseSample =  signal+'_htt_0PM125' # SM from aHTT production
        bsmBaseSample = signal+'_htt_0M125'

        for channel in channels :
            fileName = base+'htt_%s.inputs-sm-13TeV-MELA-5040-Tight.root' % channel
            file = ROOT.TFile( fileName, "UPDATE" )
            print file

            for catBase in catBases :
                print "\n === %s ===" % catBase
                histKeys = get_Keys_Of_Class( file, catBase, "TH1D" )
                dir = file.Get( catBase )
                dir.cd()

                for k in histKeys :
                    name = k.GetName()
                    #print name

                    # get SM signal including shape uncertainties
                    if smBaseSample in name :
                        # Find pure BSM signal associated with SM (including uncert)
                        k2 = get_key_matching_inputs( histKeys, smBaseSample, name, bsmBaseSample )
                        name2 = k2.GetName()
                        print name, name2
                        h = k.ReadObj()
                        h2 = k2.ReadObj()
                        hPos = h.Clone()
                        hPos.Add( -1 * h2 )
                        # hNeg is the same here, will be inverted later
                        hNeg = h.Clone()
                        hNeg.Add( -1 * h2 )
                        print h.Integral()
                        print h2.Integral()
                        for b in range( 1, hPos.GetNbinsX()+1 ) :
                            if hPos.GetBinContent( b ) <= 0 :
                                hPos.SetBinContent( b, 0. )
                                hPos.SetBinError( b, 0. )
                            if hNeg.GetBinContent( b ) > 0 :
                                hNeg.SetBinContent( b, 0. )
                                hNeg.SetBinError( b, 0. )
                            #print " * ",hPos.GetBinContent( b )
                            #print " x ",hNeg.GetBinContent( b )
                        print "hPos:",hPos.Integral()
                        # Invert hNeg for Combine
                        hNeg.Scale( -1. )
                        print "hNeg",hNeg.Integral()

                        shapeUncert = ''
                        if smBaseSample != name : # (shape uncert)
                            shapeUncert = name.replace( smBaseSample, '' )

                        hPos.SetName( signal+'_htt_0MintP125'+shapeUncert )
                        hPos.SetTitle( signal+'_htt_0MintP125'+shapeUncert )
                        hPos.Write()
                        hNeg.SetName( signal+'_htt_0MintN125'+shapeUncert )
                        hNeg.SetTitle( signal+'_htt_0MintN125'+shapeUncert )
                        hNeg.Write()
                        print "Combine:",name," and ",name2," --> ",hPos.GetName(),hNeg.GetName()

                        print "Checking %s_htt_0MintP125 - %s_htt_0MintN125 = %s_htt125 - %s_htt_0M125" % (signal, signal, signal, signal)
                        if ((hPos - hNeg).Integral() == (h - h2).Integral()) :
                            print " --- Great Success!"
            file.Close()




