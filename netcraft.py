#!/usr/bin/env python
#coding:utf-8

'''
从netcraft.com 中获取 所有的子域名字典
'''
import requests
import subprocess
import re
import sys

def getcontent(url, cookies, domain):
    global allsub
    global re_url
    try_num = 0
    re_url = url
    headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6',
            'Cookie' : cookies,
            'Referer' : re_url,
            }
    while try_num < 5:
        try:
            req = requests.get(url = url, headers = headers, timeout = 10)
            sub = re.findall('rel="nofollow">(.*?)\.<FONT COLOR="#ff0000">' + domain, req.text)
            allsub = allsub + sub
            next_req = re.findall('<A href="(.*?)"><b>Next page</b></a>', req.text)
            if next_req:
                url = 'http://searchdns.netcraft.com' + next_req[0]
            else:
                url = ''
            return url

        except Exception,e:
            print e
            try_num += 1


def getsub(domain):
    global allsub
    allsub = []
    global re_url
    re_url = 'http://searchdns.netcraft.com/?restriction=site+contains&host=t-safe.org&lookup=wait..&position=limited'
    shell = 'phantomjs getcookies.js'
    run = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutput, errorput) = run.communicate()
    cookies = stdoutput.rstrip()
    url = 'http://searchdns.netcraft.com/?restriction=site+contains&position=limited&host=%s'%domain
    while url != '':
        #print url
        url = getcontent(url, cookies, domain)
        #print allsub
    return allsub

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: python netcraft.py domain.com'
        sys.exit(-1)
    else:
        domain = sys.argv[1]
        print getsub(domain)

