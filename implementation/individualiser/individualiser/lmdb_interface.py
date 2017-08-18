import lmdb
import numpy as np
import cPickle as cpk

# wrapper functions to make the already 
# easy to use LMDB python wrapper easier?
# I'm not sure why I did this, but it 
# made things marginally more simple??

def open():
    env = lmdb.open("data/", map_size=8000011200, subdir=True)
    return env


def close(lmdb_env):
    lmdb_env.close()


def store(key, value):
    # pickle the value, cast key to byte string
    # python 2.7 string type might work anyway
    value = cpk.dumps(value)
    env = open()
    #transaction part
    with env.begin(write=True) as trans:
        result = trans.put(key, value)
        return result
        trans.commit()


def fetch(key):
    #takes key, returns pickled object/thing
    env = open()
    with env.begin(write=False) as trans:
        result = trans.get(key)
        if result == None:
            return None
        result = cpk.loads(result)
        return result
        trans.commit()


def delete(key):
    env = open()
    with env.begin(write=True) as trans:
        result = trans.delete(key) 
        return result
        trans.commit()
