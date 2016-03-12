#!/usr/bin/env python

from gittle import Gittle
import subprocess
import os
import re
import sys
import getopt


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
        print '|{0:<40}'.format(self.__name),
        print '|{0:<40}'.format(self.__pre_id),
        print '|{0:<40}|'.format(self.__now_id)


def usage():  
    print '''Usage: gcid [-h] [--help]
            [-c commit_id]
            [-d directory]
            [-f file_name]'''


def printInfo(path, pre, now):
    print '|{0:<40}|'.format(path),
    print '{0:<40}'.format(pre),
    print '|{0:<40}|'.format(now)


def getPwd():
    return os.getcwdu()


def getRepo(path):
    from dulwich.errors import NotGitRepository

    repo = None
    try:
        repo = Gittle(path)
    except NotGitRepository as e:
        print e
    
    return repo


def getGcid(file_name, gcids):
    gcid = Gcid(file_name)
    gcids.append(gcid)

    return gcid


def getIds(f):
    cmd = 'git log -2 "' + str(f) + '" | grep commit'
    #print 'CMD = %s' % cmd
    ids = ['-', ]

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for i in p.stdout:
        if re.match(r'^commit ', i):
            ids.insert(0, re.split(r'commit ', i)[1][:-1])

    p.wait()
    return ids


def createGcids(files, gcids):
    for f in files:
        #print 'file name = %s' % f
        gcid = getGcid(f, gcids)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

    for g in gcids:
        g.show()

    print '===================tracked files count = %d ===================' % len(files) 
    print '===================commit ids count = %d ===================' % len(gcids) 


def getIdsByFile(f):
    pass


def getIdsByDir(d):
    path = getPwd()
    repo = getRepo(path)
    
    if not repo:
        sys.exit(1)

    path = path + '/' + d
    ret = os.path.isdir(path)

    if not ret:
        print '"%s" is a invalid directory, must be use a valid directory!' % d
        sys.exit(1)
    
    os.chdir(path)
    
    r = r'^' + d + '/'
    files = []
    for f in list(repo.tracked_files):
        if re.match(r, f):
            files.append(re.split(r, f)[1])

    files_count = len(files)
    if files_count > 200:
        s = 'There are too many files (' + files_count + '). Are you sure to continue:(n/y)'
        ip = raw_input(s).strip()[0]
        if 'y' != ip:
            sys.exit(0)

    gcids = []
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files, gcids)
    print '===================tracked files count = %d ===================' % len(files) 


def getIdsByCmid(c):
    pass


def getIdsInRepo():
    path = getPwd()
    print '=================current path : %s =====================' % path

    repo = getRepo(path)
    if not repo:
        sys.exit(1)
    else:
        os.chdir(path)

    files = list(repo.tracked_files)
    files_count = len(files)
    if files_count > 200:
        s = 'There are too many files (' + files_count + '). Are you sure to continue:(n/y)'
        ip = raw_input(s).strip()[0]
        if 'y' != ip:
            sys.exit(0)

    gcids = []
    
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files, gcids)
    print '===================tracked files count = %d ===================' % len(files) 


if "__main__" == __name__:
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'ahc:d:f:', ['help', ])
        print 'opts = %s' % opts
        print 'args = %s' % args

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(1)
            elif '-a' == opt:
                getIdsInRepo()
            elif '-c' == opt :
                getIdsByCmid(arg)
            elif '-d' == opt:
                if '/' == arg[-1]:
                    arg = arg[:-1]
                getIdsByDir(arg)
            elif '-f' == opt:
                getIdsByFile(arg)
            else:
                getIdsInRepo()
            break
        else:
            getIdsInRepo()

    except getopt.GetoptError as e:
        print 'get options error: %s ' % e
        usage()
        sys.exit(1)

