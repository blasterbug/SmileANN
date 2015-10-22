# -*- coding: utf-8 -*-

"""
Define an Artificial Neuron based on the McCulloch–Pitts (MCP) neuron model.

Generate pydoc by running : 
    $ pydoc -w faces
"""

__author__ = 'Benjamin Sientzoff'
__date__ = '20 October 2015'
__version__ = '0.1b'


from random import uniform
from math import exp
#from math import tanh

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
        
        :param size: Size of the inputs i.e. the number of synapses, weights
        are randomly choosen
        """
        # randomly give weight to each synapses
        self.__synapses__ = [uniform( 0., 1. ) for i in range( size )]
        self.__bias__ = 1
        

    def g( self, inputs ) :
        """
        activation function
        
        :param inputs: the inputs to process
        :return: activation state of the neuron
        """
        # first compute the sum of the input, regarding weight of synapses
        for i in range( len( self.__synapses__ ) ) :
            sum_input = inputs[i] * self.__synapses__[i]
        sum_input += self.__bias__
        return sigmoid( sum_input )
        #return tanh( sum_input)
    
    def learn( self, inputs, error, learning_rate ) :
        """
        define a function to set the synapses weight
        
        :param value: proportional offset to use to set inputs sensitivity
        :param error: the error regarding inputs and desired ouput
        :param learning_rate: learning rate
        """
        # for each synapses
        for i in range( len( self.__synapses__ ) ) :
            # set the sensitivity according to the input, the error 
            # and the learning rate
            self.__synapses__[i] += learning_rate * error * inputs[i]
        # update bias as well
        self.__bias__ += learning_rate * error