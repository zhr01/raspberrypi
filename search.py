# -*- coding: utf-8 -*-
"""
#!/usr/local/bin/python2.7
#python search.py -i dataset/train/ukbench00000.jpg
"""
import heapq
import cv2
from pylab import *
from scipy.cluster.vq import *
from sklearn import preprocessing
from sklearn.externals import joblib
import argparse as ap


def match(image_path):

    imageNumber = 40
    isNotDrinkingBottle = 1
    isPlaticBottle = 2
    isMetalBottle = 3
    threshold = 0.4


    # Load the classifier, class names, scaler, number of clusters and vocabulary
    im_features, image_paths, idf, numWords, voc = joblib.load("bof.pkl")


    orb = cv2.ORB_create(400)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)


    # List where all the descriptors are stored
    des_list = []

    im = cv2.imread(image_path)
    kpts, des = orb.detectAndCompute(im, None)

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
    max_score_list = heapq.nlargest(1, rank_ID)
    max_score_number = max_score_list[0][0]
    max_score = score[0, max_score_number]

    if max_score < threshold:
        print("It is not a Bottle")
        return isNotDrinkingBottle
    else:
        for i, ID in enumerate(rank_ID[0][0:5]):
            if ID > (imageNumber/2):
                print("It is a plastic bottle")
                return isPlaticBottle
            else:
                print("It is a metal bottle")
                return isMetalBottle
            break


if __name__ == "__main__":
    # Get the path of the training set
    parser = ap.ArgumentParser()
    parser.add_argument("-i", "--image", help="Path to query image", required="True")
    args = vars(parser.parse_args())

    # Get query image path
    image_path = args["image"]
    match(image_path)

