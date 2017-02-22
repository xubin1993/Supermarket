# -*- coding: utf-8 -*-
# __auth__="x_b"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./')


class Goods(object):
    def __init__(self, good_name=None, good_id=None):
        self.good_name = good_name
        self.good_id = good_id
