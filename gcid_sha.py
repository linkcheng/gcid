#!/usr/bin/env/ python

from gittle import Gittle

if __name__ == '__main__':
    repo = Gittle('/home/zhenglong/share/mygithub/python_demo')
    fileList = list(repo.tracked_files)

    print '|{0:<45}|'.format('path'),
    print '{0:<45}'.format('sha-pre'),
    print '|{0:<45}|'.format('sha-now')
    for f in fileList:
        infoList = repo.file_versions(f)[:2]

        path = infoList[0]['path']
        sha0 = infoList[0]['sha']

        if len(infoList) < 2:
            sha1 = '-'
        else: 
            sha1 = infoList[1]['sha']

        print '|{0:<45}|'.format(path),
        print '{0:<45}'.format(sha1),
        print '|{0:<45}|'.format(sha0)

        #print 'path = %s  |  commitid_pre = %s  | commitid_now = %s' % (path, sha1, sha0)

