#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:09:02 2017
@author: ana-rpg
"""
import glob
import numpy as np
import re
import os
import sys

# Path to the data extracted from the Udacity dataset
folder = '../data/extracted/training' #"training"  or "testing"
assert folder, "You should provide the dataset folder"
experiments = glob.glob(folder + "/*")

filename=sys.argv[1]

def extractInfoFromFile(file_name):
    steer_stamps = []
    # Read file and extract time stamp
    try:
       steer_stamps = np.loadtxt(file_name, usecols=1, delimiter=',', skiprows=1, dtype=int)
    except:
        print(file_name)

    return steer_stamps


def getMatching(array1, array2):
    match_stamps = []
    match_idx = []

    print(len(array1),len(array2))
    for i in array1:
        dist = abs(i - array2)

        
        idx = np.where(dist == 0)[0]
        if len(idx) is not 0:
        #edited part
        
	        match_stamps.append(array2[idx][0])
	        match_idx.append(idx[0])
	    	

    return match_stamps, match_idx


def getSyncSteering(fname, idx):
    mat = []
    try:
        mat = np.loadtxt(fname, usecols=(6,7,8,9,10,11), skiprows=1, delimiter=',')
        mat = mat[idx,:]
  
    except:
        print(fname)
    print('length of mat >>',len(mat))

    return mat




print(experiments)

# For every bag...


print(exp)

# Read images
	images = [os.path.basename(x) for x in glob.glob(exp + "/images/*png")]
	im_stamps = []
	for im in images:
	    stamp = int(re.sub(r'\.png$', '', im))
	    im_stamps.append(stamp)
	im_stamps = np.array(sorted(im_stamps))


	file_name = exp + "/interpolated.csv"
	steer_stamps = extractInfoFromFile(file_name)


	#edited part

	match_stamp, match_idx = getMatching(im_stamps, steer_stamps)

	match_idx = np.array(match_idx)



	original_fname = exp + "/interpolated.csv"
	sync_steer = getSyncSteering(original_fname, match_idx)
	print(sync_steer)
	new_fname = exp + "/sync_steering.txt"
	print(new_fname)
	np.savetxt(new_fname, sync_steer, delimiter=',',header="angle,torque,speed,lat,long,alt")
