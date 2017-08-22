import sklearn.decomposition as decomp
import numpy as np
import utility_functions as util

# Just wrapping around the PCA functions 
# used initially to test something but 
# now it's basically redundant lol 

# creates PCA object and trains/fits it
def train_model(input_matrix, components):
    pca = decomp.PCA(n_components=components)
    pca.fit(input_matrix)
    return pca

# takes a trained PCA object/model, and an input matrix, and returns the PCs/features
def pca_transform(pca_model, input_matrix):
    output_matrix = pca_model.transform(input_matrix)
    return output_matrix

# takes a trained PCA model with a previously-transformed input matrix, and returns
# a matrix matching the original input (the restructured HRTF)
def pca_reconstruct(pca_model, input_matrix):
    output_matrix = pca_model.inverse_transform(input_matrix)
    return output_matrix

# model PCWs as spherical harmonics
def spher_harm(weights):
    return

