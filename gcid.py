#!/usr/bin/env python
#coding:utf-8  

from gittle import Gittle
import subprocess
import os
import re
import sys
import getopt
import logging
import requests
import HTMLParser


class Gcid():
    def __init__(self, name = '', pre_id = '-', now_id = '-', url = ''):
        self.__name = name
        self.__pre_id = pre_id
        self.__now_id = now_id
        self.__url = url
    
    def getName(self):
        return self.__name

    def getPreId(self):
        return self.__pre_id

    def getNowId(self):
        return self.__now_id
        
    def getUrl(self):
        return self.__url

    def setName(self, name):
        self.__name = name

    def setPreId(self, pre_id):
        self.__pre_id = pre_id

    def setNowId(self, now_id):
        self.__now_id = now_id
        
    def setUrl(self, url):
        self.__url = url

    def show(self):
        print '|{0:<64}'.format(self.__name[-63:]),
        print '|{0:<40}'.format(self.__pre_id),
        print '|{0:<41}|\n'.format(self.__now_id)
        
    def showIncludeUrl(self):
        print self.__url
        print self.__name[-63:]
        print '(<%s>→' % self.__pre_id,
        print '<%s>)' % self.__now_id

def usage():  
    print '''Usage: gcid [-h] [--help]
            [-c commit_id]
            [-d directory]
            [-f file_name]
            [-u user_name]
            [-p password ]
            note: -u and -p must be use with -c
            '''


def printInfo(path, pre, now):
    print '|{0:<64}'.format(path),
    print '|{0:<40}'.format(pre),
    print '|{0:<41}|\n'.format(now)


def printWarn(files_count):
    if files_count > 200:
        s = 'There are too many tracked files (' + files_count + '). Are you sure to continue:(n/y)'
        ip = raw_input(s).strip()[0]
        if 'y' != ip:
            sys.exit(0)


def getRepo(path):
    from dulwich.errors import NotGitRepository

    repo = None
    try:
        repo = Gittle(path)
    except NotGitRepository as e:
        print e
    
    return repo


def getIds(file_name):
    cmd = 'git log -2 "' + file_name + '" | grep commit'
    #print 'CMD = %s' % cmd
    ids = ['-', '-']

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    for e in p.stderr:
        p.wait()
        return ['-', '-']

    for index, out in enumerate(p.stdout):
        if re.match(r'^commit ', out):
            ids[index] = re.split(r'commit ', out)[1][:-1]
    p.wait()

    return ids


def getGcids(files):
    gcids = []
    
    for i, f in enumerate(files):
        #print 'file name = %s' % f
        gcid = Gcid(f)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])
        
        gcids.append(gcid)
     
    return gcids


def getCookie(session, username, password):
    url = 'http://igerrit/login/#/q/status:open'
    data = {
        'username':username,
        'password':password
    }
    
    response = session.post(url, data = data)
    
    return response.request.headers.get('Cookie')


def getUrl(gcids, session, commit_id, cookie):
    url = 'http://igerrit/gitweb?p=Doc/17Model/17Cy/21_UI.git;a=commit;h=' + commit_id
    headers = {'Cookie':cookie}
    
    response = session.request('GET', url, headers = headers)
    it = re.findall(r'<td><a class="list" href=.+?</a></td>', response.text)

    for i in it:
        s = re.findall(r'gitweb.+?;h=|Navi.+?</a>', i)
        url = 'http://igerrit/' + s[0][:-3]
        url_name = s[1][:-4]
        
        html_parser = HTMLParser.HTMLParser() 
        name = html_parser.unescape(url_name) 
        short_name = re.split(r'/', name)[-1]
        
        for g in gcids:
            if name == g.getName():
                g.setName(short_name)
                g.setUrl(url)
                g.showIncludeUrl()
                break


def createGcids(files):
    for f in files:
        #print 'file name = %s' % f
        gcid = Gcid(f)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

        gcid.show()


def getIdsByFile(f):
    pass


def getIdsByDir(repo, directory):
    path = os.getcwdu() + '/' + directory
    if not os.path.isdir(path):
        print '"%s" is a invalid directory, must be use a valid directory!' % d
        sys.exit(1)
    os.chdir(path)
    
    re_str = r'^' + directory + '/'
    files = []
    for f in list(repo.tracked_files):
        if re.match(re_str, f):
            files.append(re.split(re_str, f)[1])

    files_count = len(files)
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    print '\ntracked files count = %d ' % len(files) 


def getIdsByCmid(commit_id, username = None, password = None):
    cmd = 'git show "' + commit_id + '" | grep "diff --git"'
    #print 'CMD = %s' % cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    files = []
    for f in p.stdout:   
        if re.match(r'diff --git', f):
            if re.search(r'"', f):
                #files.append(re.split(r'/', re.split(r'"', f)[1][2:])[-1])
                files.append(re.split(r'"', f)[1][2:])
            else:
                files.append(re.split(r' ', f)[2][2:])
    p.wait()
        
    if username and password:
        gcids = getGcids(files)
        session = requests.Session()
        cookie = getCookie(session, username, password)
        print cookie
        getUrl(gcids, session, commit_id, cookie)
    else:
        printInfo('path', 'comid-pre', 'comid-now')
        createGcids(files)
    print '\ntracked files count = %d' % len(files) 
    
    
def getIdsInRepo(repo):
    files = list(repo.tracked_files)
    files_count = len(files)
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    print '\ntracked files count = %d' % len(files) 


def runMain(repo):
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'ahc:d:f:u:p:', ['help', ])
        #print 'opts = %s' % opts
        #print 'args = %s' % args
        options = dict(opts)
        #print 'd = %s' % d

        if options.has_key('-h') or options.has_key('--help'):
            usage()
            sys.exit(1)
        elif options.has_key('-a'):
            getIdsInRepo(repo)
        elif options.has_key('-c'):
            if 6 > len(options['-c']):
                print 'The length of commit id must be more than 6!'
            else:
                if options.has_key('-u') and options.has_key('-p'):
                    getIdsByCmid(options['-c'], options['-u'], options['-p'])
                else:
                    getIdsByCmid(options['-c'])
        elif options.has_key('-d'):
            if '/' == options['-d'][-1]:
                options['-d'] = options['-d'][:-1]
            getIdsByDir(repo, options['-d'])
        elif options.has_key('-f'):
            getIdsByFile(options['-f'])
        else:
            getIdsInRepo(repo)
        
    except getopt.GetoptError as e:
        print 'get options error: %s ' % e
        usage()
        sys.exit(1)


if "__main__" == __name__:
    path = os.getcwdu()
    print '=====================current path : %s =====================\n' % path

    repo = getRepo(path)
    if not repo:
        sys.exit(1)
    else:
        os.chdir(path)

    runMain(repo)
