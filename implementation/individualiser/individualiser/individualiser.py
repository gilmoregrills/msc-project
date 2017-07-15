import utility_functions as util
import numpy as np
import lmdb_interface as lmdb
import pca_functions as pca
import utility_functions as util
import simplejson as json
import time
import os
import sys

# Individualisation Algorithm, implemented

# called by the running __main__ process only
# uses pretty much all of the other modules
# I'm not sure I like this structure but this 
# is how it is  - putting it all in main might
# be too insane

# takes in two vectors as a string from VR end
def individualiser(vector_string):
    # declare my log data dict
    log_data = {
        'src_loc' : None,
        'prcv_loc' : None,
        'error' : None,
        'pcs' : [],
        'pcws' : [],
        'updates' : {},
        'timestamp' : time.strftime("%H-%M-%S")
    }
    # process input vectors into CIPIC directions
    vectors = util.parse_vector(vector_string)
    angles = util.find_angles(vectors)
    log_data['src_loc'] = angles[0]
    log_data['prcv_loc'] = angles[1]
    hrtf_indexes = util.cipic_indexes(angles)
    pca_indexes = 
   
    # if no error, put the generalised hrtf in the
    # custom_hrtf key slot of LMDB instance, else:

    # fetch the pca model
    # fetch the HRTF
    
    # transform HRTF to its PCs/PCWs
   
    # make the adjustment, based on *something*

    # transform_inverse on the PCWs, reconstruct 
    # the HRTF, and store it in LMDB under the 
    # custom_hrtf key, moving whatever is there?

    # write log data dict to log.json file
    logfilepath = "logs/"+time.strftime("%d-%m-%Y")+"/log.json"
    logfile = open(logfilepath, "r")
    log_string = logfile.read()
    logfile.close()
    log_json = json.loads(log_string)
    logfile = open(logfilepath, "w")
    log_json['logs'].append(log_data)
    logfile.write(json.dumps(log_json, indent=4, sort_keys=True))
    logfile.close()

    return
