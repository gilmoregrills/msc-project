import numpy as np
import os.path
from hrtf import hrtf

hrtf40109l = hrtf(40, 109, "L")

print hrtf40109l.data
