#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A row of Artificial Neural Network (ANN)
to recognize smiley faces as follow :

 - 1: Happy :)
 - 2: Sad :(
 - 3: Mischievous >)
 - 4: Mad >(

Generate pydoc by running : 
    `$ pydoc -w faces`
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '11 December 2015'
__version__ = '1.0'
__license__ = "GNU GENERAL PUBLIC LICENSE V.2, June 1991"

# useful for stderr output
#from __future__ import print_function
import neuron
from neuron import Neuron
import sys
from random import shuffle

class ANN :
    """
    An Artificial Neuronal Network to recognize faces
    """
    def __init__( self ) :
        self.__ann__ = [Neuron(400) for i in range( 4 )]

    def __perform__( self, image ) :
        """
        Use the ANN to recognize an image
        
        :param image: the image to recognize
        :return: activated neuron
        """
        res = [i for i in range( 4 )]
        for i in range( 4 ) :
            res[i] = self.__ann__[i].g( image )
        return max( enumerate(res), key=( lambda x : x[1] ) )[0]
        
    def train( self, training_set, answers, learning_rate=.005 ) :
        """
        Train an Artificial Neural Network
        
        :param training_set: the inputs for the training
        :param answers: the desired outputs for the training set
        :param learning_rate: Learning rate for the training (default 0.005)
        """
        # for each inputs
        for key in training_set :
            # get the neuron supposed to be activated
            right_neuron = answers[key] - 1
            # get the most activated neuron
            activated_neuron = self.__perform__( training_set[key] )
            # if the right neuron is not activated
            if right_neuron != activated_neuron :
                # for each neuron
                for i in range( 4 ) :
                    # compute the wanted ouput
                    searched_output = 0. + int(i == right_neuron)
                    # adjust ann sensitivity according to the error
                    self.__ann__[i].learn( training_set[key], searched_output, learning_rate )

        
    def recognize( self, faces ) :
        """
        Recognize faces
        
        :param faces: the test set to be used on the ANN
        :return: dictionary containing for each faces name the recognized face
        """
        res = {}
        # for each images
        for face in faces :
            # recognize face and store the result in a dictionary
            res[face] = self.__perform__( faces[face] ) + 1
        # return the result
        return res

def read_images( test_file_name ) :
    """
    Create a dictionary to stored images from a given file
    
    :param test_file_name: File name which stores the images
    :return: dictionary image_name -> image
    """
    # open the files
    faces_f = open( test_file_name, 'r' )
    # start read the file
    line = faces_f.readline()
    # create a dictionary
    images = {}
    # initiate a name for the first image
    #img_name = "imageX"
    # while where is lines in the file
    while line:
        # skip comments
        if line.startswith( "#" ) :
            line = faces_f.readline()
        # if the line starts by a capital I
        if line.startswith( 'I' ) :
            # create a new entry for the dictionary
            img_name = line.replace( '\n', '' )
            # then the next lines are the image grey pixels value
            line = faces_f.readline()
            # convert string values on the line to integers
            image_row = [int( x ) for x in line.split()]
            # initiate an matrix in a vector to put the image in
            img = [0 for i in range( len( image_row ) * len( image_row ) )]
            # for each row of the image
            for row in range( len( image_row ) ) :
                # convert string values on the line to integers
                image_row = [int( x ) for x in line.split()]
                # for each pixels on the row
                for colum in range( len( image_row ) ) :
                    # convert the value to float and divide it to make suitable
                    # and store it in the matrix
                    img[row * len( image_row ) + colum] = float(image_row[colum])/32.
                # the next line is the next row of the image
                line = faces_f.readline()
            # then link the read image name with the image itself
            images[img_name] = img
        # read the next image
        line = faces_f.readline()
    # return the dictionary containing images name and they representation
    return images

def read_facit( facit_file_name ) :
    """
    Get the answer of a test from a file and store it in a dictionary
    
    :param facit_file_name: name of the file containing answer of the training set
    :return: dictionary storing for each images the answer
    """
    # open the file
    facit_f = open( facit_file_name, 'r' )
    # initiate a dictionary
    facit = {}
    # for each line
    for line in facit_f :
        # if the line contains a image name and the answer
        if line.startswith( "I" ) :
            # get the words on the line
            words = line.split()
            # create an entry in the dictionary with the image name
            # and convert to integer the answer associated
            facit[words[0]] = int( words[1] )
    # return the dictionary
    return facit
    
def compare_images_key( key1, key2 ) :
    """
    Sort the key for the image sets
    :param key1: first key to compare
    :param key2: second key to compare
    :return: integer regarding the range between key1 and key2
    """
    return int( key1[5:] ) - int( key2[5:] )
    
def cmp_to_key( comparator ):
    """
    Convert a cmp= function into a key= function
    :param comparator: function to compare keys
    """
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return comparator(self.obj, other.obj) < 0
        def __gt__(self, other):
            return comparator(self.obj, other.obj) > 0
        def __eq__(self, other):
            return comparator(self.obj, other.obj) == 0
        def __le__(self, other):
            return comparator(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return comparator(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return comparator(self.obj, other.obj) != 0
    return K

if __name__ == "__main__" :
    # define a help message
    help = "\nUsage :\n $ python faces.py train facit test\n train: the training set\n facit: the training solution\n test : file for test\n"
    # require 3 arguments
    if 4 == len( sys.argv ) :
        # get the images for the training set
        training_images = read_images( sys.argv[1] )
        
        # get the answers for the training set
        facit = read_facit( sys.argv[2] )
        
        training_keys = [key for key in training_images]
        
        # compute size of training subsets
        tst_end = len( training_keys )
        # run traing for approx. 80% of the images and test on the 30% remaining
        tst_start = int( tst_end * .80 )
        
        # put training subsets in an array
        training_subset = [{}, {}]
        training_subset[0] = { key : training_images[key] for key in training_keys[:tst_start] }
        training_subset[1] = { key : training_images[key] for key in training_keys[tst_start:tst_end] }
        # create the ANN
        ann = ANN()
        
        error_rate = 100.
        prev_error = 0.
        print( "# training phase" )
        # while the error rate is high
        while error_rate > 20. :
            # train the network for a subset
            ann.train( training_subset[0], facit )
            sum_error, sum_total = 0., 0.
            # test the performance
            res_test = ann.recognize( training_subset[1] )
            for face in res_test :
                sum_total += 1.
                if int(facit[face]) != int(res_test[face]) :
                    sum_error += 1.
            # update error rate
            if sum_total > 0. :
                error = (sum_error / sum_total) * 100
            else :
                error = 0
                print( "# Should never happen" )
            if prev_error != error :
                prev_error = error
            res_test = ann.recognize( training_subset[1] )
            sum_error, sum_total = 0., 0.
            for face in res_test :
                sum_total += 1.
                if int(facit[face]) != int(res_test[face]) :
                    sum_error += 1.
            error_rate = (sum_error / sum_total) * 100.
            print( str( "# error rate : " + str(error_rate) ) )
            # shuffle the training sets
            shuffle( training_keys )
            training_subset[0] = {key : training_images[key] for key in training_keys[:tst_start]}
            training_subset[1] = {key : training_images[key] for key in training_keys[tst_start:tst_end]}
        
         # get the images for the test
        test_images = read_images( sys.argv[3] )
        # cognize faces
        print( "# recognize phase" )
        final = ann.recognize( test_images )
        sorted_keys = sorted( final, key=cmp_to_key( compare_images_key ) )
        # display the res, in the order as the input
        for key in sorted_keys :
            print( str( key + '  \t' + str(final[key]) ) )
    else :
        print( help )
