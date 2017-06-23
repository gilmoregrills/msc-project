import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np
import sklearn.decomposition as decomp



print "Fetching PCA input data for all hrtfs"

data = util.restructure_data('CIPIC', True, True)
input_matrix = data[0]

print "\nOriginal input hrtf shape:"
print input_matrix.shape

print "\nRunning PCA"
pca = decomp.PCA(n_components=24)
pca.fit(input_matrix)
#pca = util.train_pca(input_matrix, 10)# create and train 10 component pca model
hrtf_pcs = pca.transform(input_matrix)
#hrtf_pcs = util.pca_transform(input_matrix)

print "\nAbout the trained model:"
print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_
print "\nExplained variance ratio of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)

print "\nAbout the transformed input matrix:"
print "\nPre-transform:"
print input_matrix.shape
print "\nPost-transform:"
print "shape:"
print hrtf_pcs.shape
print "\nThis should represent, then, 24 components for each source position AND participant"

print "\nReconstruction:"
reconstructed_hrtf = pca.inverse_transform(hrtf_pcs)
print "\nReconstructed HRTF shape:"
print reconstructed_hrtf.shape
#maybe generate graph here



print "\nFetching PCA input data for single hrtf\n"
data = util.restructure_data('CIPIC', True, False)
input_matrix = data[0]
print "\nOriginal input hrtf shape:"
print input_matrix.shape

print "\nRunning PCA"
pca = decomp.PCA(n_components=10)
pca.fit(input_matrix)
#pca = util.train_pca(input_matrix, 10)# create and train 10 component pca model
hrtf_pcs = pca.transform(input_matrix)
#hrtf_pcs = util.pca_transform(input_matrix)

print "\nAbout the trained model:"
print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_
print "\nExplained variance ratio of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)

print "\nAbout the transformed input matrix:"
print "\nPre-transform:"
print input_matrix.shape
print "\nPost-transform:"
print "shape:"
print hrtf_pcs.shape
print "\nThis should represent, then, 10 components that can be modified for each source position"

print "\nReconstruction:"
reconstructed_hrtf = pca.inverse_transform(hrtf_pcs)
print "\nReconstructed HRTF shape:"
print reconstructed_hrtf.shape
#maybe generate graph here
