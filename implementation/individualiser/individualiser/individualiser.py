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
    # process input vectors into angles
    vectors = util.parse_vector(vector_string)
    angles = util.find_angles(vectors)
    # log it
    log_data['src_loc'] = list(angles[0])
    log_data['prcv_loc'] = list(angles[1])
    # work out two error values (for each dir)
    # positive num for up or right, neg for down
    # these values dictate what PCs I modify
    error = [(angles[0][0] - angles[1][0] / 10), (angles[0][1] - angles[1][1] / 10)]
    weight = 0.1 # multiplied by the error to produce numbers <1 to +/- from PCWs
    print "error = ", error
    # log it
    # if no error/below a certain threshold, make no change and return
    # indexes in CIPIC coordinate structure
    hrtf_indexes = util.cipic_indexes(angles)
    # the indexes in a 1250*n PCA matrix!
    # [0] should be primary value
    # [1][0-7] should be secondary
    pcw_indexes = util.pcw_indexes(hrtf_indexes[0])

    # fetch the pca model
    pca_model = lmdb.fetch('single_pca_model')

    # fetch the current working HRTF from custom_hrtf
    current_hrtf = lmdb.fetch('custom_hrtf')
    # archive this hrtf in preparation 
    lmdb.store('custom_hrtf_'+time.strftime("%H-%M-%S")+time.strftime("%d-%m-%Y"), current_hrtf)

    # transform HRTF to its PCA input form
    current_hrtf = util.restructure_data(current_hrtf, False)

    # fetch column mean matrix from database    
    column_mean = lmdb.fetch('avg_pca_mean')# hold this for later
    # subtract column mean matrix from PC matrix
    current_hrtf = current_hrtf - column_mean

    # actually run PCA transformation
    current_hrtf = pca.pca_transform(pca_model, current_hrtf)

    # make the adjustment, based on holzl research
    # and the weight/error identified above

    # pca_reconstruct on the PCW matrix,
    current_hrtf = pca.pca_reconstruct(pca_model, current_hrtf)
    print "inverse pca transform result: ", current_hrtf.shape
    # add column mean matrix back into modified PCW matrix 
    current_hrtf = current_hrtf + column_mean
    # reconstruct the HRTF
    current_hrtf = util.restructure_inverse(current_hrtf, False)
    print "reconstructed hrtf shape: ", current_hrtf.shape

    # store in custom_hrtf index
    lmdb.store('custom_hrtf', custom_hrtf)

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
