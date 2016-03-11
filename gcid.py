#!/usr/bin/env python

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


def getPwd():
    return os.getcwd()


def getRepo(path):
    from dulwich.errors import NotGitRepository

    repo = None
    try:
        repo = Gittle(path)
    except NotGitRepository as e:
        print e
    
    return repo


def getGcid(file_name, gcids = []):
    gcid = Gcid(file_name)
    gcids.append(gcid)

    return gcid


def getIds(f):
    cmd = 'git log -2 "' + f + '" | grep commit'
    #print 'CMD = %s' % cmd
    ids = ['-', ]

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    ids.insert(0, re.split(r'commit ', p.stdout.readline())[1][:-1])

    p.wait()
    return ids


def test():
    path = getPwd()
    #path = Path
    print '=================current path : %s =====================' % path

    repo = getRepo(path)

    if not repo:
        return
    else:
        os.chdir(path)

    files = list(repo.tracked_files)
    print '===================tracked files count = %d ===================' % len(files) 
    
    gcids = []
 
    #printInfo('path', 'comid-pre', 'comid-now')

    for f in files:
        print 'file name = %s' % f
        gcid = getGcid(f, gcids)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

    for g in gcids:
        g.show()

    print '===================tracked files count = %d ===================' % len(files) 
    print '===================commit ids count = %d ===================' % len(gcids) 

if __name__ == '__main__':
    test()
