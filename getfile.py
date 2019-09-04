__author__ = 'pshubham'
from os.path import isfile, join
import os,magic
def getfile(path):
    onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
    files = {}
    for i in range(0,len(onlyfiles)):
        temp = os.path.join(path, onlyfiles[i])
        m = magic.from_file(temp,mime=True)
        files[onlyfiles[i]] = [temp,m]
    return files

def getdir(path):
    all =  os.listdir(path)
    onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
    dir = list(set(all) - set(onlyfiles))
    return [dir,path]