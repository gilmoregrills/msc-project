import lmdb
import numpy as np
import pickle as pk
import cPickle as cpk


def store(key, value):
    # pickle the value, cast key to byte string
    # python 2.7 string type might work anyway
    value = cpk.dumps(value)
    env = lmdb.open("data", map_size=1800001120)
    with env.begin(write=True) as txn:
        result = txn.put(key, value)
        return result
        txn.commit()

def fetch(key):
    #takes key, returns pickled object/thing
    env = lmdb.open("data", map_size=1800001120)
    with env.begin(write=False) as txn:
        result = txn.get(key)
        result = cpk.loads(result)
        return result
        txn.commit()

def delete(key):
    env = lmdb.open("data", map_size=1800001120)
    with env.begin(write=True) as txn:
        result = txn.delete(key) 
        return result
        txn.commit()
