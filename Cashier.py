# -*- coding: utf-8 -*-
# __auth__="x_b"
import os
import random
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./')


class Cashier(object):

    def __init__(self):
        self.cashier_id = str(time.time())

    def sellGoods(self, buy_queue, bought_queue, cashier_queue, task_number=45,lock=None):

        while cashier_queue.qsize() < task_number:
            print u"(cashier)待处理队列长度%s" % buy_queue.qsize()
            try:
                goods_id = buy_queue.get(block=False)
                print "cashier enter %s" % goods_id
                if not goods_id:
                    time.sleep(1)
                    continue
                lock.acquire()
                bought_queue.put(goods_id)
                lock.release()
                print u"(cashier)已处理队列长度%s" % bought_queue.qsize()
                lock.acquire()
                cashier_queue.put(os.getpid())
                lock.release()
                time.sleep(random.randint(5, 10))
            except Exception as e:
                print e
                time.sleep(1)
                continue

