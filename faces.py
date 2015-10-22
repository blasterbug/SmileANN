#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A row of Artificial Neural Network (ANN)
to recognize smiley faces as follow :
 * 1: Happy :)
 * 2: Sad :(
 * 3: Mischievous >)
 * 4: Mad >(
The files containing images *must* use the given format, the name
of the image follow by the pixel grey-scale value for each pixels.

Generate pydoc by running : 
    $ pydoc -w faces
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '22 October 2015'
__version__ = '0.1'

# useful for stderr output
#from __future__ import print_function
import neuron
from neuron import Neuron
import sys
import operator


"""
define a help message
"""
help = "\nUsage :\n $ python faces.py train facit test\n train: the training set\n facit: the training solution\n test : file for test\n"

class ANN :
    """
    An Artificial Neuronal Network to recognize faces
    """
    def __init__( self ):
        self.__ann__ = [Neuron(400) for i in range( 4 )]

    def __perform__( self, image ):
        """
        Use the ANN to recognize an image
        
        :param image: the image to recognize
        :return: activated neuron
        """
        res = [i for i in range( 4 )]
        for i in range( 4 ):
            res[i] = self.__ann__[i].g( image )
        return max( enumerate(res), key=( lambda x : x[1] ) )[0]
        
    def train( self, training_set, answers, error_level=20, learning_rate=.005 ) :
        """
        Train an Artificial Neural Network
        
        :param training_set: List containing inputs for the training
        :param answers: list containing the desired outputs for the training set
        :param error_level: The error tolerance in percent (default 20)
        :param learning_rate: Learning rate for the training (default 0.005)
        """
        error_rate, prev_error = 100, 0
        sum_error,sum_test = 0., 0.
        # while the error is "too huge"
        while error_rate > error_level :
            # for each inputs
            for key in training_set :
                sum_test = sum_test + 1
                # index of the neuron supposed to be activated
                right_neuron = answers[key] - 1
                # get the most activated neuron
                activated_neuron = self.__perform__( training_set[key] )
                # compute the error
                error = 1. - self.__ann__[right_neuron].g( training_set[key] )
                # if the right neuron is not activated
                if right_neuron != activated_neuron : 
                    # adjust ann sensitivity according to the error
                    self.__ann__[right_neuron].learn( training_set[key], error, learning_rate )
                    sum_error = sum_error + 1
                #print( str(key + '  \t' + str(answers[key]) + '\t' + str(activated_neuron+1)) )
            error_rate = int((sum_error / sum_test)*100)
            if prev_error != error_rate :
                prev_error = error_rate
                print( error_rate )
        
    def recognize( self, faces ) :
        """
        Recognize faces
        
        :param faces: the test set to be used on the ANN
        :return: dictionnary containing for each faces name the recognized face
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
    img_name = "image unknown"
    # while where is lines in the file
    while line:
        # if the line starts by a capital I
        if line.startswith( 'I' ):
            # create a new entry for the dictionary
            img_name = line.replace( '\n', '' )
            # then the next lines are the image grey pixels value
            line = faces_f.readline()
            # convert string values on the line to integers
            image_row = [int( x ) for x in line.split()]
            # initiate an matrix in a vector to put the image in
            img = [0 for i in range( len( image_row ) * len( image_row ) )]
            # for each row of the image
            for row in range( len( image_row ) ):
                # convert string values on the line to integers
                image_row = [int( x ) for x in line.split()]
                # for each pixels on the row
                for colum in range( len( image_row ) ):
                    # convert the value to integer and put it in the matrix
                    img[row * len( image_row ) + colum] = int(image_row[colum])
                # the next line is the next row of the image
                line = faces_f.readline()
            # then link the read image name with the image itself
            images[img_name] = img
        # read the next image
        line = faces_f.readline()
    # return the dictionary containing images name and they representation
    return images

def read_facit( facit_file_name ):
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
        if line.startswith( "I" ):
            # get the words on the line
            words = line.split()
            # create an entry in the dictionary with the image name
            # and convert to integer the answer associated
            facit[words[0]] = int( words[1] )
    # return the dictionary
    return facit

if __name__ == "__main__" :
    # require 3 arguments
    if 4 == len( sys.argv ) :
        # get the images for the training set
        training_images = read_images( sys.argv[1] )
        
        # get the answers for the training set
        facit = read_facit( sys.argv[2] )
        
        training_keys = [key for key in training_images]
        
        # put training subsets in an array
        training_subset = [{}, {}]
        training_subset[0] = {key : training_images[key] for key in training_keys[:200]}
        training_subset[1] = {key : training_images[key] for key in training_keys[200:300]}
        # create the ANN
        ann = ANN()
        # train the network for a subset
        ann.train( training_subset[0], facit, error_level=72 )
        
        # cognize faces
        #final = ann.recognize( test )
        # display the res
        #for face in res :
        #   print( str( face + '  \t' + str(final[face]) ) )
        
        # get the images for the test
        #test = read_images( sys.argv[3] )
        test = read_images( sys.argv[3] )
        res_test = ann.recognize( test )
        sum_error, sum_total = 0, 0
        for face in res_test :
            sum_total += 1
            if int(facit[face]) != int(res_test[face]) :
                sum_error += 1
            print( str( face + '  \t' + str(facit[face]) + '\t' + str(res_test[face]) ) )
        print( sum_error , sum_total )
        
    else :
        print( help )
