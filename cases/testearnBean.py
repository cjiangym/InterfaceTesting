import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.login import Login
from common.getKey import Key
from config import serverAddressConfig


class DailySign_shopSign_goodsScanTest(unittest.TestCase):

    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    sheet2 = common_method.get_excle_sheet(1)
    login = Login()
    svrAddr = serverAddressConfig.sv_29090

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_dailySign(self):
        u"测试每日签到"
        base_url = self.sheet1.cell_value(14,2)
        uid = self.sheet1.cell_value(14,4)
        version = serverAddressConfig.version
        params_name =["uid","appversion"]
        params_value = [uid,version]
        response = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        status = result["status"]
        signinfo = result["data"]["signInfo"]
        self.assertEqual(status,10001)
        self.assertNotEqual(len(signinfo),0)

    def test_shopSignList(self):
        u"测试获取签到列表"
        base_url = self.sheet1.cell_value(15,2)
        uid = self.sheet1.cell_value(15, 4)
        cityName = self.sheet1.cell_value(15, 5)
        lon = self.sheet1.cell_value (15, 6)
        lat = self.sheet1.cell_value (15, 7)
        pages = "1"
        pageSize = "30"
        version = serverAddressConfig.version,
        os = serverAddressConfig.os,
        devcode = serverAddressConfig.devcode,
        params_name =["uid","cityName","lon","lat","pages","pageSize","appversion","os","devcode"]
        params_value = [uid,cityName,lon,lat,pages,pageSize,version,os,devcode]
        try:
            response = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual(result["status"],10001)
            self.assertNotEqual(result["data"],None)
            self.assertNotEqual (result["data"], {})
            self.assertNotEqual (result["data"]["shopSignList"],[])
            result = json.loads(response.content)
            return result
        except:
            self.assertTrue(None,"测试获取签到列表异常")

    def test_shopSign_01(self):
        u"测试到店签到"
        '''从签到列表获取待签到的数据'''
        try:
            self.result_shopSignlist = self.test_shopSignList()
        except:
            self.assertTrue(None,"签到列表获取失败,无法进行签到")
        '''从登录获取authkey用于加密'''
        phone = self.sheet1.cell_value(16,4)
        psw = self.sheet1.cell_value(16,5)
        try:
            self.result_login = self.login.phone_login(phone=phone,psw=psw)
        except:
            self.assertTrue(None,"登录失败,无法进行签到")
        shop_list_id = int(self.sheet1.cell_value(16, 7))    # 取签到列表的第x个数组数据
        base_url = self.sheet1.cell_value(16, 2)
        beacon = "0"                                      # 签到beacon，没有则为0
        uid = str(self.result_login["data"]["user"]["id"])                #从登录获取
        shopId = str(self.result_shopSignlist["data"]["shopSignList"][shop_list_id]["shopid"])
        timestamp = serverAddressConfig.timestamp
        authkey = self.result_login["data"]["authkey"]
        key_list = [uid, shopId, beacon, timestamp, authkey]
        key = Key.get_key(self,key_list)
        '''签到经纬度'''
        lon = self.result_shopSignlist["data"]["shopSignList"][shop_list_id]["lon"]
        lat = self.result_shopSignlist["data"]["shopSignList"][shop_list_id]["lat"]
        cityId = self.sheet1.cell_value(16,6)
        params_name =["beacon", "lon","lat","uid","shopId","cityId","devcode","timestamp","key"]
        params_value = [beacon,lon,lat,uid,shopId,cityId,timestamp,timestamp,key]
        try:
            sign_response = self.common_method.get_response(self.svrAddr,base_url, params_name,params_value)
            self.assertEqual(sign_response.status_code,200)
            result = json.loads(sign_response.content)
            if result["data"]:
                self.assertEqual(result["status"],10001)
                self.assertNotEqual (len(result["data"]),0)
            else:
                self.assertEqual (result["status"], 20007)
                self.assertEqual((result["msg"]), "每个商店一天只能签到一次哦")
            '''签到成功之后，签到商店列表是否已签到状态为Y'''
            try:
                self.result2_shopSignlist = self.test_shopSignList()
                self.assertEqual (self.result2_shopSignlist["data"]["shopSignList"][shop_list_id]["userIsSign"], "Y")
            except:
                self.assertTrue(None,"签到列表获取失败...")
            return sign_response
        except:
            self.assertTrue(None,"签到失败")

    def test_shopSign_02(self):
        u"测试已签到后，再次签到"
        try:
            self.response = self.test_shopSign_01()
        except:
            self.assertTrue(None,"签到失败")
        self.assertEqual(self.response.status_code,200)
        result = json.loads(self.response.content)
        self.assertEqual(result["status"],20007)
        self.assertEqual(result["msg"],"每个商店一天只能签到一次哦")

    def test_shopScanlist(self):
        u"测试获取扫描列表"
        base_url = self.sheet1.cell_value(17,2)
        timestamp = serverAddressConfig.timestamp
        phone = self.sheet1.cell_value(17,4)
        psw = self.sheet1.cell_value (17, 5)
        try:
            self.result_login = self.login.phone_login(phone=phone,psw=psw)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        uid = str(self.result_login["data"]["user"]["id"])
        cityid = self.sheet1.cell_value(17,6)
        lon = str(self.sheet1.cell_value(17,7))
        lat = str(self.sheet1.cell_value(17,8))
        pages = self.sheet1.cell_value (17, 9)
        authkey = self.result_login["data"]["authkey"]
        key_list = [uid,cityid,lon,lat,timestamp,authkey]
        key = Key.get_key(self,key_list)
        params_name = ["timestamp","pageSize","usertype","uid","cityid","lon","lat","pages","key"]
        params_value = [timestamp,"30","1",uid,cityid,lon,lat,pages,key]
        try:
            response = self.common_method.get_response(self.svrAddr,base_url,params_name,params_value)
        except:
            self.assertTrue (None,"测试获取扫描列表异常")
        else:
            self.assertEqual(response.status_code,200)
            result = json.loads(response.content)
            self.assertEqual (result["status"], 10001)
            self.assertNotEqual (result["data"], None)
            self.assertNotEqual (result["data"], {})
            self.assertNotEqual (result["data"]["scanShopList"],[])
            return result

    def test_scanGoods_01(self):
        u"测试扫描"
        base_url = self.sheet1.cell_value (18, 2)
        phone = self.sheet1.cell_value (18, 4)
        psw = self.sheet1.cell_value (18, 5)
        try:
            self.result_login = self.login.phone_login (phone, psw)
        except:
            self.assertTrue(None,"登录失败，无法获取到authkey")
        uid = str (self.result_login["data"]["user"]["id"])
        shopid = self.sheet1.cell_value (18, 6)
        authkey = self.result_login["data"]["authkey"]
        barcode = self.sheet1.cell_value (18, 7)
        timestamp = serverAddressConfig.timestamp
        key_list = [shopid, uid, barcode, timestamp, authkey]
        key = Key.get_key (self,key_list)
        params_name = ["uid","shopid","barcode","timestamp","key"]
        params_value = [uid,shopid,barcode,timestamp,key]
        try:
            response = self.common_method.get_response(self.svrAddr,base_url, params_name,params_value)
        except:
            self.assertTrue (None, "扫描失败")
        else:
            result = json.loads (response.content)
            if result["data"]:
                self.assertEqual(result["status"], 10001)
                self.assertNotEqual(result["data"], {})
            elif result["status"] == 20007:
                self.assertEqual (result["msg"], "亲，你已经扫描过了哦")
            else:
                self.assertEqual (result["msg"], "没有这样的可扫描商品")
            return response

    def test_scanGoods_02(self):
        u"测试扫描，已扫描过商品"
        try:
            self.response_scan = self.test_scanGoods_01()
        except:
            self.assertTrue(None,"扫描失败")
        result = json.loads(self.response_scan.content)
        self.assertEqual(result["data"],{})
        if result["status"] == 20007:
            self.assertEqual(result["msg"], "亲，你已经扫描过了哦")
        else:
            self.assertEqual(result["msg"], "没有这样的可扫描商品")







