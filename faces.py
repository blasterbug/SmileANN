#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Benjamin Sientzoff
 2015/10/08
 A row of Artificial Neuronal Network (ANN)
 to recognize smiley faces as follow :
  * 1: Happy :) 
  * 2: Sad :(
  * 3: Mischievous >)
  * 4: Mad >(
 The files containing images ***must*** use the given format, the name of the 
 image follow by the pixel grey-scale value for each pixels.
"""

# useful for stderr output
#from __future__ import print_function
import sys
from math import sqrt
 
# define a manual message
manual = "Usage :\n\t$ python faces.py train facit test\n train : training files,\n facit : the training solution\n test : file for test\n"

"""
    Create a dictionary of the stored images in a given file
    :param test_file_name: File name which stores the images
    :return: dictionary image_name -> image
"""
def create_images( test_file_name ) :
    try :
        # open the files
        faces_f = open( test_file_name, 'r' )
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
                pixels = [ int( x ) for x in line.split() ]
                # the image is a array in a vector
                img = [ 0 for i in range( len( pixels) * len( pixels ) )]
                # while the line contains digits 
                for row in range( len( pixels ) ):
                    # matrix in a vector
                    for colum in range( len( pixels ) ):
                        # put the raw of the image in an array
                        img[row * len( pixels ) + colum ] = pixels[colum]
                    line = faces_f.readline()
                # then link the read image name with the image itself
                images[ img_name ] = img
                print( img_name, ":" )
                idx = int(sqrt( len(img) ))
                for i in range( idx ):
                    line = str( img[ i * idx ] )
                    for j in range( idx ):
                        line += ', ' + str( img[ i * idx + j] )
                    print( line, '\n' )
            line = faces_f.readline()
        #print( images )
    except OSError:
        print( "Can't open ", test_file_name, file=sys.stderr )

def create_facit( facit_file_name ):
    try :
        facit_f = open( fl, 'r' )
    except OSError:
        print( "Can't open ", fl, file=sys.stderr )

def main( argv ) :
    create_images( argv[1] )

if __name__ == "__main__" :
    # require 3 arguments
    if len( sys.argv ) == 4 :
        main( sys.argv )
    else :
        #sys.stderr.write('Bad call\n' + manual)
        print( "Bad call\n", manual, file=sys.stderr )

