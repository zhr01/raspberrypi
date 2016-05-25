# -*- coding: utf-8 -*-
"""
#!/usr/local/bin/python2.7
#python search.py -i dataset/train/ukbench00000.jpg
"""
import argparse as ap

import cv2
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)
from sklearn.externals import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing

from pylab import *
from PIL import Image

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to query image", required="True")
args = vars(parser.parse_args())

# Get query image path
image_path = args["image"]

# Load the classifier, class names, scaler, number of clusters and vocabulary
im_features, image_paths, idf, numWords, voc = joblib.load("bof.pkl")


orb = cv2.ORB_create(400)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING)


# List where all the descriptors are stored
des_list = []

im = cv2.imread(image_path)
kpts, des = orb.detectAndCompute(im, None)

# rootsift
#rs = RootSIFT()
#des = rs.compute(kpts, des)

des_list.append((image_path, des))

# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]

#
test_features = np.zeros((1, numWords), "float32")
words, distance = vq(descriptors,voc)
for w in words:
    test_features[0][w] += 1

# Perform Tf-Idf vectorization and L2 normalization
test_features = test_features*idf
test_features = preprocessing.normalize(test_features, norm='l2')

score = np.dot(test_features, im_features.T)
rank_ID = np.argsort(-score)

# Visualize the results
#figure('Demo: BoW (bag of words)   ')
gray()
subplot(2,5,3)
title('查询图像',fontproperties = font)
imshow(im[:,:,::-1])
axis('off')
for i, ID in enumerate(rank_ID[0][0:5]):
    img = Image.open(image_paths[ID])
    gray()
    subplot(2,5,i+6)
    title('返回结果',fontproperties = font)
    imshow(img)
    axis('off')

show()
