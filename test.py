###    Author: Manushaqe Muco (manjola@mit.edu)
###    Date: 2020
###    License: MIT License

import numpy as np
import random
from vision import *


"""10 x 10 TESTS"""
one = np.pad(np.array([[1.0] for i in range(10)]),
             [(0,0), (2, 7)], 'constant', constant_values = 255)
##[[ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.  255.  255.  255.  255.  255.]]

four = np.full((10, 10), 255)
for i in [(0,2), (0,5), (1,2), (1,5), (2,2), (2,5), (3,2), (3,5), (3,3), (3,4),
          (4,5), (5,5),(6,5)]:
    (x,y) = i
    four[x][y]=1.0
##[[ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.    1.    1.    1.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]]

zero = np.full((10, 10), 255)
for i in [(1,2), (1,3), (1,4), (1,5), (6,2), (6,3), (6,4), (6,5),
          (2,2), (2,5),
          (3,2), (3,5),
          (4,2), (4,5),
          (5,2), (5,5)]:

    (x,y) = i
    zero[x][y]=1.0
##[[ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.    1.    1.    1.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.  255.  255.    1.  255.  255.  255.  255.]
## [ 255.  255.    1.    1.    1.    1.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]
## [ 255.  255.  255.  255.  255.  255.  255.  255.  255.  255.]] 



"""MODULE"""
n0= numerical_layer(10, 0)
w0 = waltz_layer(10, 0)
f0 = filter_layer(0)


def study_input(inp, name):
    print name
    n0.get_input(inp)
    print printImage1(n0.value_layer()), "\n"

    f0.set_orientation("FWD", n0, w0)

    has_changed = True
    while has_changed==True:
        
        snap = w0.get_snapshot()

        f0.set_orientation("BKWD", n0, w0)
        print printImage1(n0.value_layer()), "\n"

        f0.set_orientation("FWD", n0, w0)
        #print w0, "\n"
        has_changed = w0.has_layer_changed(snap)

    
    #n0.reset()
    #w0.reset()
    print "Final"
    print printImage1(n0.value_layer()), "\n"
    print w0, "\n"
    

#study_input(one, "One")
#study_input(four, "Four")




##    
##
#print one, "\n"
#print "One"
n0.get_input(zero)
print printImage1(n0.value_layer()), "\n"
##
f0.set_orientation("FWD", n0, w0)
print w0, "\n"
##snap = w0.get_snapshot()
##
#n0.reset()
#f0.set_orientation("BKWD", n0, w0)
#print printImage1(n0.value_layer()), "\n"
##
##f0.set_orientation("FWD", n0, w0)
##print w0, "\n"
##print w0.has_layer_changed(snap)
##
##
##n0.reset()
##w0.reset()


###print four, "\n"
##print "\n", "Four"
##n0.get_input(four)
##print printImage1(n0.value_layer()), "\n"
##
##f0.set_orientation("FWD", n0, w0)
##print w0, "\n"
##snap = w0.get_snapshot()
##
##f0.set_orientation("BKWD", n0, w0)
##print printImage1(n0.value_layer()), "\n"
##
##f0.set_orientation("FWD", n0, w0)
##print w0, "\n"
##print w0.has_layer_changed(snap)
###n0.reset()
###w0.reset()




###print zero, "\n"
##n0.get_input(zero)
###print n0, "\n"
##print printImage1(n0.value_layer()), "\n"
##f0.set_orientation("FWD", n0, w0)
###print w0, "\n"
###w0.reset()
##n0.reset()
###print n0
##f0.set_orientation("BKWD", n0, w0)
###print n0, "\n"
##print printImage1(n0.value_layer())


