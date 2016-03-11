#!/usr/bin/env/ python

from gittle import Gittle
import subprocess
import os
import re


Path = '/home/zhenglong/share/mygithub/python_demo/'

class Gcid():
    def __init__(self, name = '', pre_id = '-', now_id = '-'):
        self.__name = name
        self.__pre_id = pre_id
        self.__now_id = now_id
    
    def getName(self):
        return self.__name

    def getPreId(self):
        return self.__pre_id

    def getNowId(self):
        return self.__now_id

    def setName(self, name):
        self.__name = name

    def setPreId(self, pre_id):
        self.__pre_id = pre_id

    def setNowId(self, now_id):
        self.__now_id = now_id

    def show(self):
        print '|{0:<40}|'.format(self.__name),
        print '{0:<40}'.format(self.__pre_id),
        print '|{0:<40}|'.format(self.__now_id)


def printInfo(path, pre, now):
    print '|{0:<40}|'.format(path),
    print '{0:<40}'.format(pre),
    print '|{0:<40}|'.format(now)


def getGcid(file_name, gcids = []):
    gcid = None
    for g in gcids:
        if g.getName() == file_name:
            gcid = g
            break
    else:
        gcid = Gcid(file_name)
        gcids.append(gcid)

    return gcid


def getIds(f):
    os.chdir(Path)
    cmd = 'git log -2 "' + f + '" | grep commit'
    #print 'CMD = %s' % cmd
    ids = ['-', ]

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        #print re.split(r'commit ', line)[1][:-2] ,
        ids.insert(0, re.split(r'commit ', line)[1][:-2])
    retval = p.wait()
    return ids

def test():
    repo = Gittle(Path)
    files = list(repo.tracked_files)
    gcids = []
 
    printInfo('path', 'comid-pre', 'comid-now')

    for f in files:
        gcid = getGcid(f, gcids)
        
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

    for g in gcids:
        g.show()


if __name__ == '__main__':
    test()
