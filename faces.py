#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A row of Artificial Neural Network (ANN)
to recognize smiley faces as follow :
 * 1: Happy :)
 * 2: Sad :(
 * 3: Mischievous >)
 * 4: Mad >(
The files containing images ***must*** use the given format, the name
of the image follow by the pixel grey-scale value for each pixels.

Generate pydoc by running : 
    $ pydoc -w faces
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '20 October 2015'
__version__ = '0.1b'


# useful for stderr output
#from __future__ import print_function
import sys
from math import exp, tanh
from random import uniform

"""
define a help message
"""
help = "\nUsage :\n $ python faces.py train facit test\n train: the training set\n facit: the training solution\n test : file for test\n"

def sigmoid( t ) :
    """
    
    """
    return 1. / ( 1. + exp( -t ) )

class Neuron :
    """
        Define neurons for a Artificial Neural Network using  the 
        McCulloch–Pitts (MCP) neuron model.
    """
    # weight of each input
    def __init__( self, size ) :
        """
        Create a neuron
        
        :param size: Size of the inputs i.e. the number of synapses
        """
        # give randomly weight to each synapses
        self.__synapses__ = [uniform( -1., 1. ) for i in range( size )]
        
    def g( self, input_set ) :
        """
        activation function
        
        :param input_set: Input to process
        :return: activation state of the neuron
        """
        # first compute the sum of the input, regarding weight of synapses
        for i in range( len( self.__synapses__ ) ) :
            sum_input = input_set[i] * self.__synapses__[i]
        #return sigmoid( sum_input )
        return tanh( sum_input)
    
    def learn( self, inputs, error, learning_rate ) :
        """
        define a function to set the synapses weight
        
        :param value: proportional offset to use to set inputs sensitivity
        :param error: error makes by the neuron
        :param learning_rate: learning rate
        """
        for i in range( len( self.__synapses__ ) ) :
            self.__synapses__[i] += inputs[i]*error*learning_rate

class ANN :
    """
    Define an Artificial Neuronal Network to recognize faces
    """
    def __init__( self ):
        self.__ann__ = [Neuron(400) for i in range( 4 )]

    def __perform__( self, image ):
        """
        use the ANN to recognize an image
        
        :param image: the image to pass through the network
        :return: enumeration (neuron number, score for the image)
        """
        res = [i for i in range( 4 )]
        for i in range( 4 ):
            res[i] = self.__ann__[i].g( image )
        return enumerate(res)

    def train( self, training_set, answers, error_level=10, learning_rate=1 ) :
        """
        Train an Artificial Neural Network
        
        :param training_set: List containing inputs for the training
        :param answers: list containing the answers for the training set
        :param error_level: Threshold to the error tolerance (default 55%)
        :param learning_rate: Learning rate for the training (default 0.7)
        """
        error_rate = 100
        sum_error,sum_test = 0., 0.
        # while the error is "too huge"
        while error_rate > error_level :
            # for each inputs
            for key in training_set :
                sum_test += 1
                # index of the neuron supposed to be activated
                right_neuron = answers[key] - 1
                res = self.__perform__( training_set[key] )
                # get the highest outputs (neurons number in ann and value)
                better_neuron = max( res, key=( lambda x : x[1] ) )
                # if the right neuron is not activated
                if right_neuron != better_neuron[0] : 
                    # compute the error to the right answer
                    error = better_neuron[1] - answers[key]
                    # adjust ann sensitivity according to the error
                    self.__ann__[ right_neuron ].learn( training_set[key], error, learning_rate )
                    sum_error += 1
                print key, "  \t", answers[key], "\t" , better_neuron[0] + 1, "\t", error
            error_rate = int((sum_error / sum_test)*100)
            print error_rate
        
    def test( self, test_set ) :
        """
        use the ANN
        
        :param test_set: the test set to be used on the ANN
        """
        for img in test_set :
            print( img, perform( self.__ann__, test_set[img] ) )

def read_images( test_file_name ) :
    """
    Create a dictionary to stored images from a given file
    
    :param test_file_name: File name which stores the images
    :return: dictionary image_name -> image
    """
    try :
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
                pixels = [int( x ) for x in line.split()]
                # initiate an array in a vector to put the image in
                img = [0 for i in range( len( pixels) * len( pixels ) )]
                # while the line contains digits
                for row in range( len( pixels ) ):
                    # convert string values on the line to integers
                    pixels = [int( x ) for x in line.split()]
                    # matrix in a vector
                    for colum in range( len( pixels ) ):
                        # put the raw of the image in the array
                        img[row * len( pixels ) + colum] = pixels[colum]
                    # then the next lines are the image grey pixels value
                    line = faces_f.readline()
                line = faces_f.readline()
                # then link the read image name with the image itself
                images[img_name] = img
            line = faces_f.readline()
        return images
    except OSError:
        #print( "Can't open " + test_file_name, sys.stderr )
        print( "Can't open " + test_file_name )

def read_facit( facit_file_name ):
    """
    Get the answer of a test and store it in a dictionary
    
    :param facit_file_name: name of the file containing
        answer of the training set
    :return: dictionary storing for each images the answer
    """
    try :
        # open the file
        facit_f = open( facit_file_name, 'r' )
        # initiate a dictionary
        facit = {}
        # for each line
        for line in facit_f :
            # if the line contains a image name and the answer
            if line.startswith( "I" ):
                words = line.split()
                # create an entry in the dictionary with the image name
                # and convert to integer the answer associated
                facit[words[0]] = int( words[1] )
        return facit
    except OSError:
        #print( "Can't open " + test_file_name, file=sys.stderr )
        print( "Can't open " + test_file_name )

if __name__ == "__main__" :
    # require 3 arguments
    if 4 == len( sys.argv ) :
        # get the images for the training set
        training_set = read_images( sys.argv[1] )
        
        # get the answers for the training set
        facit = read_facit( sys.argv[2] )
        
        train = [training_set[key] for key in training_set]
        
        # get the images for the test
        #test = read_images( sys.argv[3] )
        
        # create the ANN
        ann = ANN()
        # train the network
        ann.train( training_set, facit )
        # perform faces recognition
        #ann.test( test )
        
    else :
        #print( "Bad call\n" + manual, file=sys.stderr )
        print( help )
