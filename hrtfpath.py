import numpy as np

def hrtfpath(root, subdir, select, ext, elev, azim)
#again cloning from the MIT KEMAR matlab scripts
#all props to Bill Gardner and the MIT Media Lab
    x = '/'
    return(root+x+subdir+x+elev+x+select+elev+azim+ext)

