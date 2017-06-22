import sys
sys.path.append('../')
import individualiser.utility_functions as util
import numpy as np

print "Fetching PCA input data"
inputData = util.prepareInputMatrix('cipic')
pcaInputMatrix = inputData[0]

print "\nRunning PCA"
pca = util.runPCA(pcaInputMatrix, 22)

print "\nNumber of components:"
print pca.n_components_
print "\nExplained variance of each component:"
print pca.explained_variance_ratio_
print "\nTotal explained variance:"
print np.sum(pca.explained_variance_ratio_)
