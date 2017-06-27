import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np
import individualiser.pca_functions as PCA



print "Fetching PCA input data for all hrtfs"


data = util.fetch_database('CIPIC')
data1 = util.fourier_transform(data, False, True)
hrtf_db = data1[0]

print "\nOriginal input hrtf shape:"
print hrtf_db.shape
print "restructuring database for input\n"
hrtf_db_input = util.restructure_data(hrtf_db, True)

print "\nRunning PCA"
model = PCA.train_model(hrtf_db_input, 24)
transformed_hrtf = PCA.pca_transform(model, hrtf_db_input)


print "\nAbout the trained model:"
print "\nNumber of components:"
print model.n_components_
print "\nExplained variance of each component:"
print model.explained_variance_
print "\nExplained variance ratio of each component:"
print model.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(model.explained_variance_ratio_)

print "\nAbout the transformed input matrix:"
print "\nPre-transform:"
print hrtf_db.shape
print "\nPost-transform:"
print "shape:"
print transformed_hrtf.shape
print "\nThis should represent, then, 24 components for each source position AND participant"

print "\nReconstruction:"
reconstructed_hrtf = PCA.pca_reconstruct(model, transformed_hrtf)
print "\nReconstructed HRTF shape:"
print reconstructed_hrtf.shape
#maybe generate graph here

if reconstructed_hrtf == hrtf_db:
    print "test success!"
else: 
    print "test failed"


print "\nFetching PCA input data for single hrtf\n"
avg_hrtf = util.average_hrtf(data)
print "\nOriginal input hrtf shape:"
print avg_hrtf.shape

print "\nRestructuring to input matrix shape:"
pca_input = util.restructure_data(avg_hrtf, False)
print pca_input.shape

print "\nRunning PCA"
model = PCA.train_model(pca_input, 10)
transformed_hrtf_two = PCA.pca_transform(model, pca_input)

print "\nAbout the trained model:"
print "\nNumber of components:"
print model.n_components_
print "\nExplained variance of each component:"
print model.explained_variance_
print "\nExplained variance ratio of each component:"
print model.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(model.explained_variance_ratio_)

print "\nAbout the transformed input matrix:"
print "\nPre-transform:"
print pca_input.shape
print "\nPost-transform:"
print "shape:"
print transformed_hrtf_two.shape
print "\nThis should represent, then, 10 components that can be modified for each source position"

print "\nReconstruction:"
reconstructed_hrtf = PCA.pca_reconstruct(model, transformed_hrtf_two)
print "\nReconstructed HRTF shape:"
print reconstructed_hrtf.shape
#maybe generate graph here

if reconstructed_hrtf == avg_hrtf:
    print "test success!"
else: 
    print "test failed"
