import lmdb
import numpy as np
import cPickle as cpk

def open():
    env = lmdb.open("data/", map_size=4000011200, subdir=True)
    return env


def close(lmdb_env):
    lmdb_env.close()


def store(key, value):
    # pickle the value, cast key to byte string
    # python 2.7 string type might work anyway
    value = cpk.dumps(value)
    env = open()
    #transaction part
    with env.begin(write=True) as txn:
        result = txn.put(key, value)
        return result
        txn.commit()


def fetch(key):
    #takes key, returns pickled object/thing
    env = open()
    with env.begin(write=False) as txn:
        result = txn.get(key)
        if result == None:
            return None
        result = cpk.loads(result)
        return result
        txn.commit()


def delete(key):
    env = open()
    with env.begin(write=True) as txn:
        result = txn.delete(key) 
        return result
        txn.commit()
