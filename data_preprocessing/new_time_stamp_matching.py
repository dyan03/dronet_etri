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
#folder = None #"training"  or "testing"
#folder = "/home/bj/rpg_public_dronet/data/extracted/training"
#folder = "/home/bj/rpg_public_dronet/data/extracted/validation"
folder = sys.argv[1]
#folder = "/home/bj/rpg_public_dronet/data/extracted/testing"
#assert folder, "You should provide the dataset folder"
experiments = glob.glob(folder + "/*")

print(experiments)

def extractInfoFromFile(file_name):
    steer_stamps = []
    # Read file and extract time stamp
#    print ("file_name : ", file_name)

    try:
       steer_stamps = np.loadtxt(file_name, usecols=1, delimiter=',', skiprows=1, dtype=int)
    except:
        print(file_name)
    return steer_stamps


def getMatching(array1, array2):
    match_stamps = []
    match_idx = []
    for i in array1:
        dist = abs(i - array2)
        idx = np.where(dist == 0)[0]
        match_stamps.append(array2[idx])
        match_idx.append(idx)
    return match_stamps, match_idx


def getSyncSteering(fname, idx):
    mat = []
    try:
        mat = np.loadtxt(fname, usecols=(2,3,4,5,6), skiprows=1, delimiter=',')
        mat = mat[idx,:]
    except:
        print(fname)
    return mat



# For every bag...
#print("experiments : ", experiments)

for exp in experiments:
    
    #print("exp : ", exp)

    # Read images
    #images = [os.path.basename(x) for x in glob.glob(exp + "/images/*.png")]
    images = [os.path.basename(x) for x in glob.glob(exp + "/images/*.jpg")]

    im_stamps = []
    for im in images:
        #stamp = int(re.sub(r'\.png$', '', im))
        stamp = int(re.sub(r'\.jpg$', '', im))
        im_stamps.append(stamp)
    im_stamps = np.array(sorted(im_stamps))

    # Extract time stamps from steerings
    file_name = exp + "/interpolated.csv"
    steer_stamps = extractInfoFromFile(file_name)

    # Time-stamp matching between images and steerings
    print("debug -------- ", exp)
    match_stamp, match_idx = getMatching(im_stamps, steer_stamps)
    match_idx = np.array(match_idx)
    match_idx = match_idx[:,0]

    # Get matched commands
    original_fname = exp + "/interpolated.csv"
    sync_steer = getSyncSteering(original_fname, match_idx)
#    print("match idx : ", match_idx)

    new_fname = exp + "/sync_steering.txt"
    np.savetxt(new_fname, sync_steer, delimiter=',',
               header="angular.z, linear.x,linear.y,linear.z,angular.x,angular.y")
#               header="linear.x,linear.y,linear.z,angular.x,angular.y,angular.z")
