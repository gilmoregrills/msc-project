import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np

print "Fetching PCA input data for structure1"
data = util.restructure_data('CIPIC', True, True, True)
input_matrix = data[0]


print "\nRunning PCA"
pca = util.run_pca(input_matrix, 12)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)

"""
print "\nFetching PCA input data for structure2"
data = util.restructure_data('CIPIC', True, True, False)
input_matrix = data[0]


print "\nRunning PCA"
pca = util.run_pca(input_matrix, 22)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)
"""

print "\nFetching PCA input data for structure3"
data = util.restructure_data('CIPIC', True, False, True)
input_matrix = data[0]


print "\nRunning PCA"
pca = util.run_pca(input_matrix, 12)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)
