#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import h5py
import json
import necout
import argparse
import numpy as np
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help="input file")
    parser.add_argument('-o', type=str, help="output file")
    args = parser.parse_args()
    inpfile = args.i
    outfile = args.o
    print (inpfile, outfile)
    farField = "/output/requests/FarField"
    nec = necout.Nec2Out(inpfile)
    nec.parse()
    rez=nec.data
    h5 = h5py.File(outfile, 'w')
    infos = []
    for r in rez:
        inf = json.dumps({
            "freq": r["freq"]*1e6, 
            "nPhi": r["rp"][0], 
            "nTheta": r["rp"][1],
            "PhiBegin": r["rp"][2], 
            "ThetaBegin": r["rp"][3],
            "PhiStep": r["rp"][4], 
            "ThetaStep": r["rp"][5]
            })
        infos.append(inf)
    h5d = h5.create_dataset("{0}/infos".format(farField), data=infos) #np.reshape(a[1],(a[0].size,3)))    
    
    for i,r in enumerate(rez):
        
        Etheta = r["E_Theta_M"]*np.exp(1j*np.deg2rad(r["E_Theta_P"]))
        Ephi = r["E_Phi_M"]*np.exp(1j*np.deg2rad(r["E_Phi_P"]))
        t = np.c_[r["aPhi"],r["aThet"],np.real(Etheta),np.imag(Etheta),np.real(Ephi),np.imag(Ephi)]
        h5d = h5.create_dataset("{0}/ds_{1}".format(farField,i), data=t)
        

if __name__ == '__main__':
    main()
