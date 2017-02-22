# -*- coding: utf-8 -*-
# __auth__="x_b"
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./')
import time


#
class Customer(object):
    def __init__(self):
        self.customer_id = str(time.time())

    def buyGoods(self, good_id=None, buy_queue=None, bought_queue=None,lock=None):
        start_time = time.time()
        if not good_id:
            return None
        lock.acquire()
        buy_queue.put(good_id)
        lock.release()
        while True:
            try:
                print u"customer enter %s" % good_id
                print u"(customer)已处理队列长度%s" % bought_queue.qsize()
                bought_good_id = bought_queue.get(block=False)
                print u"%s 货物拿出" % bought_good_id
                if bought_good_id == good_id:
                    end_time = time.time()
                    consumed = end_time - start_time
                    # print consumed
                    print u"%s 货物已被买走,消耗时间为%s" % (good_id, consumed)
                    return consumed
                else:
                    lock.acquire()
                    bought_queue.put(bought_good_id)
                    lock.release()
                    print u"%s 货物放回" % bought_good_id
                time.sleep(1)
            except Exception as e:
                print e
                time.sleep(1)
                continue




