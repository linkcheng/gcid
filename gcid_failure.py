#!/usr/bin/env/ python

from gittle import Gittle

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
        print '|{0:<45}|'.format(self.__name),
        print '{0:<45}'.format(self.__pre_id),
        print '|{0:<45}|'.format(self.__now_id)


def printInfo(path, pre, now):
    print '|{0:<45}|'.format(path),
    print '{0:<45}'.format(pre),
    print '|{0:<45}|'.format(now)

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

def test():
    repo = Gittle('/')
    #repo = Gittle('/')
    coms = repo.commits()
    gcids = []
 
    printInfo('path', 'comid-pre', 'comid-now')

    for com in coms:
        fileInfo = repo.get_commit_files(com)
        files = fileInfo.keys()
        
        for f in files:
            gcid = getGcid(f, gcids)
            gcid.show()

            if gcid.getNowId() == '-':
                gcid.setNowId(com)
            else:
                if gcid.getPreId() == '-':
                    gcid.setPreId(com)
            print gcid.show()
            print '==========++++++++++++++++++++++==================='
        print '**********+++++++++++++++++++++++++++*****************'

    #for g in gcids:
    #    g.show()


if __name__ == '__main__':
    test()
