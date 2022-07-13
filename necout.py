#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

class Nec2Out(object):
    def __init__(self,fname):
        self.fname=fname
        self.fd = open(file=fname,mode='r')
        self.data = []
 
    def parse(self):
        ll="a"
         
        while(len(ll)):
            ll = self.fd.readline()
            if len(ll)==0:
                continue
            isFreq=ll.find("FREQUENCY :")
            if isFreq >-1:
                curFr = float(ll[isFreq+11:isFreq+22])
 
            isRP = ll.find(" RP ")
            if isRP > -1:
                tt=ll[isRP+4:].split()
                curRP=(int(tt[1]),int(tt[2]),int(tt[3]),float(tt[4]),float(tt[5]),float(tt[6]),float(tt[7]))
 
            isRPs = ll.find("RADIATION PATTERNS")
            if isRPs > -1:
                n=curRP[0]*curRP[1]
                dd = {}
                dd["rp"] = curRP
                dd["freq"]=curFr 
                for i in range(4):
                    self.fd.readline()
                aPhi = np.zeros(n)
                aThet = np.zeros(n)
                E_Theta_M = np.zeros(n)
                E_Theta_P = np.zeros(n)
                E_Phi_M = np.zeros(n)
                E_Phi_P = np.zeros(n)
                dg = np.zeros(n)
                dg_hor = np.zeros(n)
                dg_ver = np.zeros(n)
                 
                for i in range(n):
                    ll = self.fd.readline()
                    ll=ll.replace("        ", " NONE   ")
                    q=ll.split()
                    aPhi[i]=float(q[1])
                    aThet[i]=float(q[0])
                    E_Theta_M[i]=float(q[8])
                    E_Theta_P[i]=float(q[9])
                    E_Phi_M[i]=float(q[10])
                    E_Phi_P[i]=float(q[11])
                    dg[i]=float(q[4])
                    dg_hor[i]=float(q[3])
                    dg_ver[i]=float(q[2])
                     
                dd["aPhi"]=aPhi
                dd["aThet"]=aThet
                dd["E_Theta_M"]=E_Theta_M
                dd["E_Theta_P"]=E_Theta_P
                dd["E_Phi_M"]=E_Phi_M
                dd["E_Phi_P"]=E_Phi_P
                dd["DG"]=dg                                    #DG-КНД
                dd["DG_ver"]=dg_ver                            #DG-КНД
                dd["DG_hor"]=dg_hor                            #DG-КНД
                
                self.data.append(dd)
