import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np

print "Fetching PCA input data for all hrtfs"
data = util.restructure_data('CIPIC', True, True)
input_matrix = data[0]


print "\nRunning PCA"
pca = util.run_pca(input_matrix, 15)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)


print "\nFetching PCA input data for single hrtf"
data = util.restructure_data('CIPIC', True, False)
input_matrix = data[0]


print "\nRunning PCA"
pca = util.run_pca(input_matrix, 9)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)
