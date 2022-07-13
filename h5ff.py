#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import h5py
import json
import gmsh
import argparse
import numpy as np
import matplotlib.pylab as plt
import sys

def sph2cart(phi, theta, r):
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def viewff(aPhi,aTheta,FF,name):
    gmsh.initialize()
    ff = gmsh.view.add(name)
    nPhi,nTheta = aPhi.shape
    v= FF
    v0 = v/np.max(v)
    rr = []
    for i in range(nPhi-1):
        for j in range(nTheta-1):
            p1 = sph2cart(aPhi[i,j],aTheta[i,j],v0[i,j])
            p2 = sph2cart(aPhi[i+1,j],aTheta[i+1,j],v0[i+1,j])
            p3 = sph2cart(aPhi[i+1,j+1],aTheta[i+1,j+1],v0[i+1,j+1])
            p4 = sph2cart(aPhi[i,j+1],aTheta[i,j+1],v0[i,j+1])
            
            rr += (p1[0],p2[0],p3[0],p4[0])
            rr += (p1[1],p2[1],p3[1],p4[1])
            rr += (p1[2],p2[2],p3[2],p4[2])
            rr += (v[i,j],v[i+1,j],v[i+1,j+1],v[i,j+1])
    n = (nPhi-1)*(nTheta-1)
    gmsh.view.addListData(ff, "SQ", n, rr)
    gmsh.fltk.run()

    gmsh.finalize()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help="input file")
    args = parser.parse_args()
    inpfile = args.i
    farField = "/output/requests/FarField"
    h5 = h5py.File(inpfile, 'r')
    infos = []
    dsInfos = h5["{0}/infos".format(farField)]
    infos = []
    for inf in dsInfos:
        infos.append(json.loads(inf.decode("utf-8")))
    print (infos[0]["freq"])

    for i,f in enumerate(infos):
        nPhi = f["nPhi"]
        nTheta = f["nTheta"]
        ds = np.array(h5[("{0}/ds_{1}".format(farField,i))][:])
        aPhi = np.reshape(np.deg2rad(ds[:,0]),(nTheta,nPhi))
        aTheta = np.reshape(np.deg2rad(ds[:,1]),(nTheta,nPhi))
        ETheta = np.reshape(ds[:,2]+1j*ds[:,3],(nTheta,nPhi))
        EPhi = np.reshape(ds[:,4]+1j*ds[:,5],(nTheta,nPhi))
        ff = np.abs(ETheta)
        name = "FarField {0} Hz".format(f["freq"])
        viewff(aPhi,aTheta,ff,name)
        # print (nPhi)    


if __name__ == '__main__':
    main()