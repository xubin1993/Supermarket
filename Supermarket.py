# -*- coding: utf-8 -*-
# __auth__="x_b"
import multiprocessing
import random
import sys
import time

from Cashier import Cashier
from Customer import Customer
from Goods import Goods

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./')


class Supermarket(object):
    def __init__(self):
        self.manager = multiprocessing.Manager()
        # 父进程创建Queue，并传给各个子进程：
        self.goods_name = ["Apple", "Macbook", "Cookie"]
        self.goods_dict = dict()
        self.poll = multiprocessing.Pool(processes=50)

    def produceGoods(self, num=15):
        j = 1
        for name in self.goods_name:
            for i in xrange(((j - 1) * num)+1, (j * num)+1):
                goods = Goods(good_name=name, good_id=i)
                self.goods_dict[goods.good_id] = goods.good_name
            j += 1

    def start(self, cashier_num=3):

        buy_queue = self.manager.Queue()
        bought_queue = self.manager.Queue()
        cashier_queue = self.manager.Queue()
        customer_queue = self.manager.Queue()
        lock = self.manager.Lock()
        self.produceGoods()
        task_number = len(self.goods_dict.keys())
        for i in xrange(0, cashier_num):
            self.poll.apply_async(runCashier, (buy_queue, bought_queue, cashier_queue, task_number, lock))
        goods_sell_time_dict = {}
        start_time = time.time()
        while self.goods_dict:
            goods_id = random.choice(self.goods_dict.keys())
            self.goods_dict.pop(goods_id)
            wait_time = random.randint(1, 3)
            time.sleep(wait_time)
            goods_sell_time_dict[str(goods_id)] = str(wait_time)
            self.poll.apply_async(runCustomer, (goods_id, buy_queue, bought_queue, customer_queue, lock))
        self.poll.close()
        self.poll.join()
        print u"结束"
        end_time = time.time()
        sell_consumed_time = end_time - start_time
        return goods_sell_time_dict, cashier_queue, sell_consumed_time, customer_queue


def runCustomer(goods_id, buy_queue, bought_queue, customer_queue, lock):
    customer = Customer()
    consumed_time = customer.buyGoods(goods_id, buy_queue, bought_queue, lock)
    customer_queue.put(str(goods_id) + "|_|" + str(consumed_time if consumed_time else 0))


def runCashier(buy_queue, bought_queue, cashier_queue, task_number, lock):
    cashier = Cashier()
    cashier.sellGoods(buy_queue, bought_queue, cashier_queue, task_number, lock)


def count(data_dict):
    a = 0.0
    for value in data_dict.values():
        a += float(value)
    average = a / len(data_dict.values())
    return average


def count_average(customer_queue, goods_sell_time_dict, cashier_queue, sell_consumed_time):
    customer_wait_time_dict = {}
    while not customer_queue.empty():
        data = customer_queue.get()
        customer_wait_time_dict[data.split("|_|")[0]] = data.split("|_|")[1]

    customer_wait_average = count(data_dict=customer_wait_time_dict)
    print u"顾客平均等待时间为:%s" % customer_wait_average
    print goods_sell_time_dict
    for key in goods_sell_time_dict.keys():
        goods_sell_time_dict[key] = float(goods_sell_time_dict.get(key)) + float(customer_wait_time_dict.get(key))

    goods_sell_time_average = count(data_dict=goods_sell_time_dict)
    print u"每个商品平均售出时间:%s" % goods_sell_time_average

    print u"开始销售到售罄总共时间:%s" % sell_consumed_time
    data_dict = dict()
    while not cashier_queue.empty():
        pid = cashier_queue.get()
        if pid not in data_dict.keys():
            data_dict[pid] = 1
        else:
            data_dict[pid] = data_dict.get(pid) + 1
    for key in data_dict.keys():
        print u"cashier: %s 接待顾客: %s" % (key, data_dict.get(key))


if __name__ == "__main__":
    ss = Supermarket()
    goods_sell_time_dict, cashier_queue, sell_consumed_time, customer_queue = ss.start()

    count_average(customer_queue=customer_queue, goods_sell_time_dict=goods_sell_time_dict, cashier_queue=cashier_queue,
                  sell_consumed_time=sell_consumed_time)
