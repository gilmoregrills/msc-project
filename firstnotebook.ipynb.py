# coding: utf-8
from hrtf import hrtf
get_ipython().magic(u'whos')
hrtf1 = hrtf(40, 109, "L")
print hrtf1.data
