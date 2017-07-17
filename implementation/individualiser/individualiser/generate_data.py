import sys as sys
import utility_functions as util
import pca_functions as pca
import lmdb_interface as lmdb
from clint.textui import puts, colored, indent
import numpy as np

# pseudo-install script, all it does is generate those slow-to-
# generate matrices and store them in lmdb at the correct path
# allows the project to be moved to different machines/cloned
# without copying over the big ol' database, and allows future
# implementation to be pseudo-dynamic and not re-generate these
# values over and over
x = np.zeros([20])
puts("Generating data for full database")

cipic_hrir = util.fetch_database("cipic")
#puts(colored.green("storing cipic hrir dataset, size:"))
#with indent(4, quote='>'):
    #x[1] = cipic_hrir.nbytes
    #puts(str(x[1]))
#lmdb.store('cipic_hrir', cipic_hrir)

fourier_data = util.fourier_transform(cipic_hrir, False, True)
cipic_hrtf = fourier_data[0]
#puts(colored.green("storing cipic hrtf dataset, size:"))
#with indent(4, quote='>'):
    #x[2] = cipic_hrtf.nbytes
    #puts(str(x[2]))
#lmdb.store('cipic_hrtf', cipic_hrtf)

cipic_pca_input = util.restructure_data(cipic_hrtf, True)
#puts(colored.green("storing restructured pca-ready cipic hrtf set, size:"))
#with indent(4, quote='>'):
    #x[3] = cipic_pca_input.nbytes
    #puts(str(x[3]))
#lmdb.store('cipic_pca_input', cipic_pca_input)

full_pca_model = pca.train_model(cipic_pca_input, 22)
#puts(colored.green("storing trained pca model"))
#with indent(4, quote='>'):
    #x[4] = sys.getsizeof(full_pca_model)
    #puts(str(x[4]))
#lmdb.store('full_pca_model', full_pca_model)

full_pca_transformed = pca.pca_transform(full_pca_model, cipic_pca_input)
#puts(colored.green("storing transformed pca input set, size:"))
#with indent(4, quote='>'):
    #x[5] = full_pca_transformed.nbytes
    #puts(str(x[5]))
#lmdb.store('full_pca_transformed', full_pca_transformed)

puts("\nGenerating data for single/average user")

avg_hrir = util.average_hrtf(cipic_hrir)
puts(colored.green("storing averaged hrir, size:"))
with indent(4, quote='>'):
    x[6] = avg_hrir.nbytes
    puts(str(x[6]))
lmdb.store('avg_hrir', avg_hrir)

avg_hrtf = util.average_hrtf(cipic_hrtf)
puts(colored.green("storing averaged hrtf, size:"))
with indent(4, quote='>'):
    x[7] = avg_hrtf.nbytes
    puts(str(x[7]))
lmdb.store('avg_hrtf', avg_hrtf)

avg_pca_input = util.restructure_data(avg_hrtf, False)
puts(colored.green("storing restructured pca-ready averaged hrtf set, size:"))
with indent(4, quote='>'):
    x[8] = avg_pca_input.nbytes
    puts(str(x[8]))
lmdb.store('avg_pca_input', avg_pca_input)

avg_pca_mean = util.column_mean(avg_pca_input)
puts(colored.green("storing column mean of restructured hrtf, size:"))
with indent(4, quote='>'):
    x[9] = sys.getsizeof(avg_pca_mean)
    puts(str(x[9]))
lmdb.store('avg_pca_mean', avg_pca_mean)

single_pca_model = pca.train_model(avg_pca_input-avg_pca_mean, 10)
puts(colored.green("storing trained pca model"))
with indent(4, quote='>'):
    x[10] = sys.getsizeof(single_pca_model)
    puts(str(x[10]))
lmdb.store('single_pca_model', single_pca_model)

single_pca_transformed = pca.pca_transform(single_pca_model, avg_pca_input)
puts(colored.green("storing transformed pca input set, size:"))
with indent(4, quote='>'):
    x[11] = single_pca_transformed.nbytes
    puts(str(x[11]))
lmdb.store('single_pca_transformed', single_pca_transformed)

custom_hrtf = pca.pca_reconstruct(single_pca_model, single_pca_transformed)
custom_hrtf = util.restructure_inverse(custom_hrtf+avg_pca_mean, False)
puts(colored.green("storing custom hrtf reconstructed from pca data, size:"))
with indent(4, quote='>'):
    x[12] = custom_hrtf.nbytes
    puts(str(x[12]))
lmdb.store('custom_hrtf', custom_hrtf)

puts(colored.green("Total data stored:"))
with indent(4, quote='>'):
    total_data = x.sum()
    puts(str(total_data))
#test the values were stored and can be retrieved/unpickled correctly

