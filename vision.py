###    Author: Manushaqe Muco (manjola@mit.edu)
###    Date: 2020
###    License: MIT License

import numpy as np
import datetime
import random
from mnistStatistics import *

"""Image is 28x28: 28 rows with 28 elemements each"""

def printImage(image):
    """ used later to visualize orientations and suprise for each layer"""
    for i in image:
        s=""
        for j in i:
            s+=str(j)
        print s

def printImage1(image):
    """ used later to visualize orientations and suprise for each layer"""
    for i in image:
        s=""
        for j in i:
            if j>=1.0:
                s+="X"
            else:
                s+="."
        print s

""" PROCESS IMAGE OF CHARACTER BEFORE THE FORWARD-MACHINE OPERATES
In the spirit of reporting differences, we treat the original image as each pixel having two orientations: LIGHT/DARK.
(biologically if 255==dark, otherwise light cells are on. this detects only contrast?)        
Then it reports differences, upon which the filter cells act. """

def filterLightDark(image):
    light_dark_image = []
    for i in image:
        l = []
        for j in i:
            if j == 255:  #DARK-SENSITIVE CELLS
                l.append("o")
            else:
                l.append("X") #LIGHT-SENSITIVE CELLS
        light_dark_image.append(l)  
    return np.array(light_dark_image)

##for i in range(10):
##    digit, digit_label = first100Training[i]
##    print digit_label
##    print print_MNIST_character(digit)
##    print printImage(filterLightDark(digit))



""" FILTERS"""
center_dot = np.array([[0, 0, 0], [0, 1.0, 0], [0, 0, 0]]) 
vertical = np.array([[0, 1.0, 0], [0, 1.0, 0], [0, 1.0, 0]])
horizontal = np.array([[0, 0, 0], [1.0, 1.0, 1.0], [0, 0, 0]])
diagonal_1 = np.array([[0, 0, 1.0], [0, 1.0, 0], [1.0, 0, 0]])
diagonal_2 = np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])

all_filters = [(center_dot, "."), (vertical, "|"), (horizontal, "-"),
               (diagonal_1, "/"), (diagonal_2, "\\")]

#print center_dot, '\n', vertical, '\n', horizontal, '\n', diagonal_1, '\n', diagonal_2

def produceNeighbors(i,j, dimensions):
    """returns names of neighboring cells for cell (i,j)"""
    possibilities = [(i, j), (i, j+1), (i, j+2),
                     (i+1, j), (i+1, j+1), (i+1, j+2),
                     (i+2, j), (i+2, j+1), (i+2, j+2)]
    l=[]
    ceiling = dimensions - 1 
    for (a,b) in possibilities:
        if a < 0 or b < 0 or a> ceiling or b > ceiling:
            pass
        else:
            l.append((a,b))
    return l

def superposition(a, filter_type):
    x,y = a.shape
    a_pad = np.pad(a, [(0,2), (0,2)], mode='constant') #add background padding if out of bound
    a_new = a_pad[0:3, 0:3]

    if filter_type==".":
        s = a_new + center_dot
    if filter_type=="|":
        s = a_new + vertical
    if filter_type=="-":
        s = a_new + horizontal
    if filter_type=="/":
        s = a_new + diagonal_1
    if filter_type=="\\":
        s = a_new+ diagonal_2

    for i in range(3):
        for j in range(3):
            if s[i][j]>1:
                s[i][j]=1.0 
    return s[0:x, 0:y]

def apply_filter(a, (f, filter_type)):
    a_pad = np.pad(a, [(0,2), (0,2)], mode='constant') #add background padding if out of bound
    a_new = a_pad[0:3, 0:3]
    return [np.sum(np.multiply(a_new, f)), filter_type]

def apply_all_filters(a):
    possibilities = []
    max_val = 2 #activation of at least 2
    
    for f in all_filters:
        val = apply_filter(a, f)[0]
        #print val
        if val>=max_val:
            possibilities.append(f[1])
            #possibilities.append((val, f))
    return possibilities 
    

class filter_layer:
    def __init__(self, index):
        #all possible filters
        self.center_dot = center_dot
        self.vertical = vertical 
        self.horizontal = horizontal 
        self.diagonal_1 = diagonal_1
        self.diagonal_2 = diagonal_2
        self.index = index #later for when be build more modules N-W

    def set_orientation(self, flow, numerical, waltz):
        if flow=="FWD":
            for cell in numerical.cells_topology:
                cell_location = cell.name
                
                neighboring_area = produceNeighbors(cell_location[0], cell_location[1],
                                                    numerical.dimensions)
                image_value = numerical.get_sub_image_value(cell_location) 
                possible_filters = set(apply_all_filters(image_value)) 
                
                #for all cells in 3x3 receptive field, add to w what possible filters
                #they could have
                for c in neighboring_area:
                    waltz.cells_dict[c].update(possible_filters)

        if flow=="BKWD":
            for cell in waltz.cells_topology:
                cell_location = cell.name
                filters = cell.value


                neighboring_area = produceNeighbors(cell_location[0], cell_location[1],
                                                    waltz.dimensions)

                
                for f in filters:
                    image_value = numerical.get_sub_image_value(cell_location)
                    new_numbers = superposition(image_value, f).flatten()

                    for i in range(len(neighboring_area)):
                        c = neighboring_area[i]
                        numerical.cells_dict[c].set_value(new_numbers[i])

                    

"""CELLS"""
class numerical_cell:
    def __init__(self, name, value): 
        self.name = name #(a b) coordinate in numerical_layer
        self.value = value
    def reset(self):
        self.value = 0
    def set_value(self, val):
        self.value = val


class waltz_cell:
    def __init__(self, name, partial_info_set):
        self.name = name  #(a b) correspondent to (a b) numerical 
        self.value = partial_info_set #partial info set of possibilities for (a b)
        #self.changed = False    
    def reset(self):
        self.value = set([])
    def update(self, new_partial_info): ###
        if self.value==set([]):
            self.value = new_partial_info
        else:
            self.value = self.value | new_partial_info
            #self.value = self.value & new_partial_info

    def merge(self):
        pass


class numerical_layer:
    def __init__(self, n, index):
        self.dimensions = n
        self.cells_topology = []
        self.cells_dict = {}
        self.index = index
        
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                name = (i, j)
                c = numerical_cell(name, 0)
                self.cells_dict[name] = c
                self.cells_topology.append(c)
        self.layer_array = np.array(self.cells_topology).reshape(self.dimensions, self.dimensions)

    def return_layer(self):
        return self.layer_array

    def reset(self):
        for c in self.cells_topology:
            c.reset()

    def get_sub_image(self, (x,y)):
        return self.layer_array[x:x+3, y:y+3]  #3x3 filter area

    def get_sub_image_value(self, (x,y)):
        #the values of numerical cells for 3x3 area
        image = self.get_sub_image((x,y)) 
        image_value = []
        for i in image:
            l =[]
            for j in i:
                l.append(j.value)
            image_value.append(l)        
        return np.array(image_value)  

    def get_input(self, inp):
        size = inp.shape[0]
        for i in range(size):
            for j in range(size):
                if inp[i][j]==255:
                    self.layer_array[i][j].set_value(0)
                else:
                    self.layer_array[i][j].set_value(1.0)

    def value_layer(self):
        image = []
        for i in self.layer_array:
            l = []
            for j in i:
                l.append(j.value)
            image.append(l)
        return np.array(image)

    def __str__(self):
        return "\n<Numerical_Layer" + str(self.index) + "\n" + str(self.value_layer()) + "\n>"
        

class waltz_layer:
    def __init__(self, n, index):
        self.dimensions = n
        self.cells_topology = []
        self.cells_dict = {}
        self.index = index
        
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                name = (i, j)
                c = waltz_cell(name, set([]))
                self.cells_dict[name] = c
                self.cells_topology.append(c)
        self.layer_array = np.array(self.cells_topology).reshape(self.dimensions, self.dimensions)

    def return_layer(self):
        return self.layer_array

    def reset(self):
        for c in self.cells_topology:
            c.reset()

    def get_snapshot(self):
        return self.value_layer().copy()

    def has_layer_changed(self, snapshot):
        current = self.value_layer()
        changes = (current == snapshot)
        for i in changes:
            for j in i:
                if j==False:
                    return True
        return False

    def get_sub_image(self, (x,y)):
        return self.layer_array[x:x+3, y:y+3]

    def value_layer(self):
        image = []
        for i in self.layer_array:
            l = []
            for j in i:
                l.append(j.value)
            image.append(l)
        return np.array(image)

    def __str__(self):
        return "\n<Waltz_Layer" + str(self.index) + "\n" + str(self.value_layer()) + "\n>"




##
#n0=numerical_layer(28, 0)
#w0=waltz_layer(28, 0)
#f0 = filter_layer(0)
##
###get input from environment
#digit, digit_label = first100Training[0] #digit 5
##print digit_label
#print print_MNIST_character(digit), "\n"
##
##n0.get_input(digit)
##print printImage1(n0.value_layer()), "\n"
##f0.set_orientation("FWD", n0, w0)
##n0.reset()
##print n0
##f0.set_orientation("BKWD", n0, w0)
##print printImage1(n0.value_layer())

#study_input(digit, "5")










