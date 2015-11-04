# -*- coding: utf-8 -*-

"""
Define an Artificial Neuron based on the McCulloch-Pitts (MCP) neuron model.

Generate pydoc by running : 
    `$ pydoc -w neuron`
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '23 October 2015'
__version__ = '0.3'
__license__ = "GNU GENERAL PUBLIC LICENSE V.2, June 1991"

from math import exp
from random import uniform

def sigmoid( t ) :
    """
    the sigmoid function is a mathematical function having an "S" shape 
    (sigmoid curve).
    
    :param t: The parameter of the function
    :return: sigmoid( t )
    """
    return 1. / ( 1. + exp( -t ) )

class Neuron :
    """
    Define an Artificial Neuron also called perceptron based on the 
    McCulloch-Pitts (MCP) neuron model.
    """
    # weight of each input
    def __init__( self, size ) :
        """
        Create a neuron
        
        :param size: Size of the inputs i.e. the number of synapses, weights
        are randomly chosen
        """
        # randomly give weight to each synapses
        self.__synapses__ = [.5 for i in range( size )]
        #self.__synapses__ = [uniform( 0. , 1. ) for i in range( size )]
        self.__bias__ = 1.
        

    def g( self, inputs ) :
        """
        Activation function
        
        :param inputs: the inputs to process
        :return: activation state of the neuron
        """
        # first compute the sum of the input, regarding weight of synapses
        sum_input = 0
        for i in range( len( self.__synapses__ ) ) :
            sum_input += inputs[i] * self.__synapses__[i]
        sum_input += self.__bias__
        return sigmoid( sum_input )
    
    def learn( self, inputs, output, learning_rate ) :
        """
        Update the synapses weight to learn recognizing patterns
        
        :param inputs: the inputs to recognize
        :param output: the desired output regarding the inputs
        :param learning_rate: learning rate
        """
        error = output - self.g( inputs )
        # for each synapses
        for i in range( len( self.__synapses__ ) ) :
            # set the sensitivity according to the input, the error 
            # and the learning rate
            self.__synapses__[i] += learning_rate * error * inputs[i]
        # update bias as well
        self.__bias__ += learning_rate * error
    
