import sys
sys.path.append('../')
import individualiser.utility_functions as util
import individualiser.pca_functions as pca
import individualiser.lmdb_interface as lmdb
from clint.textui import puts, colored, indent

# pseudo-install script, all it does is generate those slow-to-
# generate matrices and store them in lmdb at the correct path
# allows the project to be moved to different machines/cloned
# without copying over the big ol' database, and allows future
# implementation to be pseudo-dynamic and not re-generate these
# values over and over

puts("Generating data for full database")

cipic_hrir = util.fetch_database('cipic')
puts(colored.green("storing cipic hrir dataset"))
lmdb.store('cipic_hrir', cipic_hrir)

cipic_hrtf = util.fourier_transform(cipic_hrir, False, True)
puts(colored.green("storing cipic hrtf dataset"))
lmdb.store('cipic_hrtf', cipic_hrtf)

cipic_pca_input = util.restructure_data(cipic_hrtf, True)
puts(colored.green("storing restructured pca-ready cipic hrtf set"))
lmdb.store('cipic_hrtf', cipic_hrtf)

full_pca_model = pca.train_model(cipic_pca_input, 22)
puts(colored.green("storing trained pca model"))
lmdb.store('full_pca_model', full_pca_model)

full_pca_transformed = pca.pca_transform(full_pca_model, cipic_pca_input)
puts(colored.green("storing transformed pca input set"))
lmdb.store('full_pca_transformed', full_pca_transformed)

puts("\nGenerating data for single/average user")

avg_hrir = util.average_hrtf(cipic_hrir)
puts(colored.green("storing averaged hrir"))
lmdb.store('avg_hrir', avg_hrir)

avg_hrtf = util.average_hrtf(cipic_hrtf)
puts(colored.green("storing averaged hrtf"))
lmdb.store('avg_hrtf', avg_hrtf)

avg_pca_input = util.restructure_data(avg_hrtf, False)
puts(colored.green("storing restructured pca-ready averaged hrtf set"))
lmdb.store('avg_pca_input', avg_pca_input)

single_pca_model = pca.train_model(avg_pca_input, 10)
puts(colored.green("storing trained pca model"))
lmdb.store('single_pca_model', single_pca_model)

single_pca_transformed = pca.pca_transform(single_pca_model, avg_pca_input)
puts(colored.green("storing transformed pca input set"))
lmdb.store('single_pca_transformed' single_pca_transformed)

#test the values were stored and can be retrieved/unpickled correctly

