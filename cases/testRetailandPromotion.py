import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
import re
from xlrd import xldate_as_tuple
from common.common_method import Common_method

class PromotionTest(unittest.TestCase):
    common_method = Common_method()
    sheet2 = common_method.get_excle_sheet2()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_homepagePromotion(self):
        u"测试首页促销信息"
        base_url = self.sheet2.cell_value(7,2)
        params = {
            "uid" :self.sheet2.cell_value(7,4),
            "cityid" :self.sheet2.cell_value(7,5),
            "lon" :self.sheet2.cell_value(7,6),
            "lat":self.sheet2.cell_value(7,7)

        }
