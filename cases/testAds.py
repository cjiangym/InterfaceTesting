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
from config import  serverAddressConfig

class AdsTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    svrAddr = serverAddressConfig.sv_29090

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def get_ads(self,module_id,userid,cityName):
        base_url = self.sheet1.cell_value(41,2)
        params = {
            "uid":userid,
            "cityName" :cityName,
            "moduleid" :module_id,
            "appversion" : serverAddressConfig.version,
            "os": serverAddressConfig,
            "devcode ": serverAddressConfig
        }
        response = Common_method.get_response(self,self.svrAddr,base_url,params=params)
        return response

    def test_homepageAds(self):
        u"测试首页广告"
        uid = self.sheet1.cell_value(41,4)
        cityName = self.sheet1.cell_value(41,5)
        moduleid = "8"
        response = self.get_ads(moduleid,uid,cityName)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        if result["data"]["photoList"] ==[]:
            self.assertEqual(result["data"]["photoList"],"首页没有广告,请检查后台是否有设置广告")

    def test_receiptpageAds(self):
        u"测试拍立赚页面广告"
        uid = self.sheet1.cell_value(42,4)
        cityName = self.sheet1.cell_value(42,5)
        moduleid = "12"
        response = self.get_ads(moduleid,uid,cityName)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        if result["data"]["photoList"] ==[]:
            self.assertEqual(result["data"]["photoList"],"拍了赚页面没有广告,请检查后台是否有设置广告")

    def test_inviteFriendpageAds(self):
        u"测试邀请好友页面广告"
        uid = self.sheet1.cell_value(43,4)
        cityName = self.sheet1.cell_value(43,5)
        moduleid = "4"
        response = self.get_ads(moduleid,uid,cityName)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        if result["data"]["photoList"] ==[]:
            self.assertEqual(result["data"]["photoList"],"邀请好友页面没有广告,请检查后台是否有设置广告")

    def test_giftpageAds(self):
        u"测试礼品兑换广告"
        uid = self.sheet1.cell_value(44,4)
        cityName = self.sheet1.cell_value(44,5)
        moduleid = "14"
        response = self.get_ads(moduleid,uid,cityName)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        if result["data"]["photoList"] ==[]:
            self.assertEqual(result["data"]["photoList"],"礼品兑换页面没有广告,请检查后台是否有设置广告")
