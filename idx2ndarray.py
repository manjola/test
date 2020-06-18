### modified as allowed by original license. 
### 

###    Title: Converting MNIST from IDX Format to Python Numpy Array
###    Author: Siladittya Manna
###    Date: 2017
###    License: MIT License
###    Availability: https://github.com/sadimanna/idx2numpy_array


#If no. of images is not a integer multiple of nBatch
#Uncomment "try-except" part
#This may increase the execution time by less than 1 sec

import time,math
import struct as st
import numpy as np

trainingfilenames = {'images' : 'training_set/train-images.idx3-ubyte' ,'labels' : 'training_set/train-labels.idx1-ubyte'}
testfilenames = {'images' : 'test_set/t10k-images.idx3-ubyte' ,'labels' : 'test_set/t10k-labels.idx1-ubyte'}

data_types = {
        0x08: ('ubyte', 'B', 1),
        0x09: ('byte', 'b', 1),
        0x0B: ('>i2', 'h', 2),
        0x0C: ('>i4', 'i', 4),
        0x0D: ('>f4', 'f', 4),
        0x0E: ('>f8', 'd', 8)}

#..........................................................For training dataset..............................................................
print "Training Dataset......."
stime = time.time()
for name in trainingfilenames.keys():
	if name == 'images':
		train_imagesfile = open(trainingfilenames[name],'r+')
	if name == 'labels':
		train_labelsfile = open(trainingfilenames[name],'r+')

train_imagesfile.seek(0)
magic = st.unpack('>4B',train_imagesfile.read(4))
if(magic[0] and magic[1])or(magic[2] not in data_types):
	raise ValueError("File Format not correct")

#Information
nDim = magic[3]
print "Data is "+str(nDim)+"-D"
dataType = data_types[magic[2]][0]
print "Data Type :: ",dataType
dataFormat = data_types[magic[2]][1]
print "Data Format :: ",dataFormat
dataSize = data_types[magic[2]][2]
print "Data Size :: "+str(dataSize)+" byte\n"

#offset = 0004 for number of images
#offset = 0008 for number of rows
#offset = 0012 for number of columns
#32-bit integer (32 bits = 4 bytes)
train_imagesfile.seek(4)
nImg = st.unpack('>I',train_imagesfile.read(4))[0] #num of images/labels
nR = st.unpack('>I',train_imagesfile.read(4))[0] #num of rows
nC = st.unpack('>I',train_imagesfile.read(4))[0] #num of columns

train_labelsfile.seek(8) #Since no. of items = no. of images and is already read
print "no. of images :: ",nImg
print "no. of rows :: ",nR
print "no. of columns :: ",nC
print
#Training set
#Reading the labels
train_labels_array = np.asarray(st.unpack('>'+dataFormat*nImg,train_labelsfile.read(nImg*dataSize))).reshape((nImg,1))
#Reading the Image data
nBatch = 10000
nIter = int(math.ceil(nImg/nBatch))
nBytes = nBatch*nR*nC*dataSize
nBytesTot = nImg*nR*nC*dataSize
train_images_array = np.array([])
for i in xrange(0,nIter):
	#try:
	temp_images_array = 255 - np.asarray(st.unpack('>'+dataFormat*nBytes,train_imagesfile.read(nBytes))).reshape((nBatch,nR,nC))
	'''except:
		nbytes = nBytesTot - (nIter-1)*nBytes
		temp_images_array = 255 - np.asarray(st.unpack('>'+'B'*nbytes,train_imagesfile.read(nbytes))).reshape((nBatch,nR,nC))'''
	#Stacking each nBatch block to form a larger block
	if train_images_array.size == 0:
		train_images_array = temp_images_array
	else:
		train_images_array = np.vstack((train_images_array,temp_images_array))
	temp_images_array = np.array([])
	print "Time taken :: "+str(time.time()-stime)+" seconds\n"
	print str((float(i+1)/nIter)*100)+"% complete...\n"


print "Training Set Labels shape ::",train_labels_array.shape
print "Training Set Image shape ::",train_images_array.shape

print "Time of execution :: "+str(time.time()-stime)+" seconds\n"
#..........................................................For test dataset..................................................................
print "Test Dataset......."
stime = time.time()
for name in testfilenames.keys():
	if name == 'images':
		test_imagesfile = open(testfilenames[name],'r+')
	if name == 'labels':
		test_labelsfile = open(testfilenames[name],'r+')
test_imagesfile.seek(0)
magic = st.unpack('>4B',test_imagesfile.read(4))
if(magic[0] and magic[1])or(magic[2] not in data_types):
	raise ValueError("File Format not correct")

nDim = magic[3]
print "Data is ",nDim,"-D"
print
#offset = 0004 for number of images
#offset = 0008 for number of rows
#offset = 0012 for number of columns
#32-bit integer (32 bits = 4 bytes)
test_imagesfile.seek(4)
nImg = st.unpack('>I',test_imagesfile.read(4))[0] #num of images/labels
nR = st.unpack('>I',test_imagesfile.read(4))[0] #num of rows
nC = st.unpack('>I',test_imagesfile.read(4))[0] #num of columns

test_labelsfile.seek(8) #Since no. of items = no. of images and is already read
print "no. of images :: ",nImg
print "no. of rows :: ",nR
print "no. of columns :: ",nC
print
#Test set
#Reading the labels
test_labels_array = np.asarray(st.unpack('>'+dataFormat*nImg,test_labelsfile.read(nImg*dataSize))).reshape((nImg,1))
#Reading the Image data
nBatch = 10000
nIter = int(math.ceil(nImg/nBatch))
nBytes = nBatch*nR*nC*dataSize
nBytesTot = nImg*nR*nC*dataSize
test_images_array = np.array([])
for i in xrange(0,nIter):
	#try:
	temp_images_array = 255 - np.asarray(st.unpack('>'+dataFormat*nBytes,test_imagesfile.read(nBytes))).reshape((nBatch,nR,nC))
	'''except:
		nbytes = nBytesTot - (nIter-1)*nBytes
		temp_images_array = 255 - np.asarray(st.unpack('>'+'B'*nbytes,test_imagesfile.read(nbytes))).reshape((nBatch,nR,nC))'''
	#Stacking each nBatch block to form a larger block
	if test_images_array.size == 0:
		test_images_array = temp_images_array
	else:
		test_images_array = np.vstack((test_images_array,temp_images_array))
	temp_images_array = np.array([])
	print "Time taken :: "+str(time.time()-stime)+" seconds\n"
	print str((float(i+1)/nIter)*100)+"% complete...\n"


print "Test Set Labels shape ::",test_labels_array.shape
print "Test Set Image shape ::",test_images_array.shape

print "Time of execution : %s seconds" % str(time.time()-stime)
