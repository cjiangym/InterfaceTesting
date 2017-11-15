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

#---------------------首页功能按钮，功能模块，精明豆页功能模块，我的页面功能按钮--------------------#

class ModulefunctionTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_recommendation(self):
        u"测试首页推荐功能模块"
        base_url = ""

