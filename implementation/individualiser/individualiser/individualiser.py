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

# take in two vectors from frontend, one for the 
# actual sound source, and the other for the user's 
# perceived source, what they "click" on
def individualiser(source_vector, perceived_vector):
    # process the input vectors to determine the 
    # directions that need adjustment (in terms of
    # 0-1249) and by how much (how great the error)
   
    # if no error, put the generalised hrtf in the
    # custom_hrtf key slot of LMDB instance, else:

    # fetch the pca model
    # fetch the HRTF
    
    # transform HRTF to its PCs/PCWs
   
    # make the adjustment, based on *something*

    # transform_inverse on the PCWs, reconstruct 
    # the HRTF, and store it in LMDB under the 
    # custom_hrtf key, moving whatever is there?
