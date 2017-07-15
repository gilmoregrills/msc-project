import utility_functions as util
import numpy as np
import lmdb_interface as lmdb
import pca_functions as pca
import utility_functions as util

# Individualisation Algorithm, implemented

# called by the running __main__ process only
# uses pretty much all of the other modules
# I'm not sure I like this structure but this 
# is how it is  - putting it all in main might
# be too insane

# takes in two vectors as a string from VR end
def individualiser(vector_string):
    print "vector string: ", vector_string
    # process input vectors into CIPIC directions
    vectors = util.parse_vector(vector_string)
    print "vectors: \n", vectors
    angles = util.find_angles(vectors)
    print "angles: \n", angles
    indexes = util.cipic_indexes(angles)
    print "indexes: \n", indexes
   
    # if no error, put the generalised hrtf in the
    # custom_hrtf key slot of LMDB instance, else:

    # fetch the pca model
    # fetch the HRTF
    
    # transform HRTF to its PCs/PCWs
   
    # make the adjustment, based on *something*

    # transform_inverse on the PCWs, reconstruct 
    # the HRTF, and store it in LMDB under the 
    # custom_hrtf key, moving whatever is there?
    return
