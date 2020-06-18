###    Author: Manushaqe Muco (manjola@mit.edu)
###    Date: 2020
###    License: MIT License


import numpy as np
import datetime
import random
from idx2ndarray import train_images_array,test_images_array,train_labels_array,test_labels_array


#begin_time = datetime.datetime.now()


def print_MNIST_character(character): #later use for MNIST + letters
    """prints the MNIST character with . for background and X for image"""
    for i in character:
        s=""
        for j in i:
            if j == 255: #background -- black?
                s+="."
            else:
                s+="X" #foreground -- actual image
                        #values can vary from 1 to 215 for this
        print s
        

def getDigitStats(sample):
    digits_stats = [0 for i in range(10)]
    for i in sample:
        if i==0:
            digits_stats[0]+=1
        if i==1:
            digits_stats[1]+=1
        if i==2:
            digits_stats[2]+=1
        if i==3:
            digits_stats[3]+=1
        if i==4:
            digits_stats[4]+=1
        if i==5:
            digits_stats[5]+=1
        if i==6:
            digits_stats[6]+=1
        if i==7:
            digits_stats[7]+=1
        if i==8:
            digits_stats[8]+=1
        if i==9:
            digits_stats[9]+=1   
    return digits_stats


#print getDigitStats(train_labels_array), sum(getDigitStats(train_labels_array))
#[5923, 6742, 5958, 6131, 5842, 5421, 5918, 6265, 5851, 5949], 60000


def getN(dataset, dataset_labels, n):
    """get first N (data, label) for a dataset"""
    l = []
    for i in range(n):
        l.append((dataset[i], dataset_labels[i]))
        i+=1
    return l


def getRandomN(dataset, dataset_labels, n):
    """get N random (data, label) for a dataset"""
    l=[]
    random.seed()
    for i in range(n):
        j = random.randint(0,n-1)
        l.append((dataset[j], dataset_labels[j]))
        i+=1
    return l
    
 
first100Training = getN(train_images_array, train_labels_array, 100)
first1000Training = getN(train_images_array, train_labels_array, 1000)
first10000Training = getN(train_images_array, train_labels_array, 10000)

#print getDigitStats([i[1] for i in first100Training]), sum(getDigitStats([i[1] for i in first100Training]))
#[13, 14, 6, 11, 11, 5, 11, 10, 8, 11] 100
#print getDigitStats([i[1] for i in first1000Training]), sum(getDigitStats([i[1] for i in first1000Training]))
#[97, 116, 99, 93, 105, 92, 94, 117, 87, 100] 1000
#print getDigitStats([i[1] for i in first10000Training]), sum(getDigitStats([i[1] for i in first10000Training]))
#[1001, 1127, 991, 1032, 980, 863, 1014, 1070, 944, 978] 10000


random100Training = getRandomN(train_images_array, train_labels_array, 100)
random1000Training = getRandomN(train_images_array, train_labels_array, 1000)
random10000Training = getRandomN(train_images_array, train_labels_array, 10000)

#print getDigitStats([i[1] for i in random100Training]), sum(getDigitStats([i[1] for i in random100Training]))
#print getDigitStats([i[1] for i in random1000Training]), sum(getDigitStats([i[1] for i in random1000Training]))
#print getDigitStats([i[1] for i in random10000Training]), sum(getDigitStats([i[1] for i in random10000Training]))


###test that it maps images and labels correctly 
#for i in range(10):
#    digit, digit_label = random100Training[i]
#    print digit_label
#    print print_MNIST_character(digit)
   

#print "time elapsed", datetime.datetime.now() - begin_time



