# -*- coding: utf-8 -*-

"""
Define an Artificial Neuron based on the McCulloch–Pitts (MCP) neuron model.

Generate pydoc by running : 
    $ pydoc -w faces
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '20 October 2015'
__version__ = '0.1b'


from math import exp, tanh
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
            print self.__synapses__[i] , inputs[i]
            self.__synapses__[i] += abs(inputs[i] * error * learning_rate)
            print self.__synapses__[i]

