# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/19 14:08
@Auth ： Tiger
@File ：thread.py
@IDE ：PyCharm
@Motto:Coding is nothing
"""
import threading
import time
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.delay, 3)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
            print("if is in process")
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
print ("退出主线程")
print ("Exiting Main Thread")

if __name__ == '__main__':
    print("退出主线程####")
    print("###Exiting Main Thread")
    # 创建新线程
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)

    # 开启新线程
    thread1.start()
    thread2.start()