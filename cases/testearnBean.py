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


class DailySign_shopSign_goodsScanTest(unittest.TestCase):

    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet1 ()
    sheet2 = common_method.get_excle_sheet2()
    dict = common_method.get_common_params()
    login = Login()

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_dailySign(self):
        u"测试每日签到"
        base_url = self.sheet1.cell_value(14,2)
        uid = self.sheet1.cell_value(14,4)
        params ={
            "uid":uid,
            "appversion":self.common_method.version
        }
        response = requests.get(base_url,params=params)
        result = json.loads(response.content)
        status = result["status"]
        signinfo = result["data"]["signInfo"]
        self.assertEqual(status,10001)
        self.assertNotEqual(len(signinfo),0)

        #获取到店签到列表
    def get_shopSignlist(self):
        base_url = self.sheet1.cell_value(15,2)
        params = {
            "uid":math.floor(self.sheet1.cell_value(15,4)),
            "cityName":self.sheet1.cell_value(15,5),
            "lon":self.sheet1.cell_value(15,6),
            "lat":self.sheet1.cell_value(15,7),
            "pages":str(math.floor(self.sheet1.cell_value(15,8))),
            "pageSize":"30",
            "appversion":self.common_method.version,
            "os":self.common_method.os,
            "devcode":self.common_method.devcode,
        }
        response = requests.get(base_url,params=params)
        return response

     #签到
    def get_shopSign_result(self):
        response_shopSignlist = self.get_shopSignlist ()
        phone = self.sheet1.cell_value(16,4)
        psw = self.sheet1.cell_value(16,5)
        result_login = self.login.phone_login(phone=phone,psw=psw)
        if response_shopSignlist.status_code ==200:
            result_shopSignlist = json.loads(response_shopSignlist.content)
            print(response_shopSignlist.url)
            if result_shopSignlist["data"]:
                base_url = self.sheet1.cell_value (16, 2)
                shop_list = int(self.sheet1.cell_value (16, 8))   # 去签到列表的第x个数组数据
                beacon = "0"                                    # 签到beacon，没有则为0
                uid = str(result_login["data"]["user"]["id"])                #从登录获取
                shopId = str(result_shopSignlist["data"]["shopSignList"][shop_list]["shopid"])
                timestamp = self.common_method.timestamp
                authkey = result_login["data"]["authkey"]                #从登录获取
                key_list = [uid, shopId, beacon, timestamp, authkey]
                key = self.common_method.get_key (key_list)
                params = {
                    "beacon":beacon ,
                    "lon": result_shopSignlist["data"]["shopSignList"][shop_list]["lon"],    # 从签到列表获取经纬度
                    "lat": result_shopSignlist["data"]["shopSignList"][shop_list]["lat"],
                    "uid": uid,
                    "shopId": shopId,
                    "cityId":  self.sheet1.cell_value (16, 7),  # 从签到列表获取shopid,
                    "devcode": self.sheet1.cell_value(16,6),
                    "timestamp": timestamp,
                    "key": key
                }
                response = requests.get(base_url, params=params)
                return response
        else:
            return None

    def test_shopSign_01(self):
        u"测试到店签到"
        response_shoplist = self.get_shopSignlist()  #签到列表返回结果
        response = self.get_shopSign_result()        #签到返回结果
        if response != None and response_shoplist.status_code ==200 and response.status_code ==200:
            result_shoplist = json.loads(response_shoplist.content)
            result = json.loads(response.content)
            print(result)
            if result["data"]:
                shop_list =int(self.sheet1.cell_value (16, 8))         # 取签到列表的第x个数组数据,用于验证签到结果
                self.assertEqual(result["status"],10001)
                self.assertNotEqual(len(result["data"]),0)
                self.assertEqual(result_shoplist["data"]["shopSignList"][shop_list]["userIsSign"],"Y")   #签到列表已签到，userIsSign=Y
            else:
                self.assertEqual(result["status"],20007)
                self.assertEqual(result["msg"],"每个商店一天只能签到一次哦")
        else:
            self.assertEqual(response,"签到失败")

    def test_shopSign_02(self):
        u"测试已签到后，再次签到"
        response = self.get_shopSign_result()
        if response != None and response.status_code ==200:
            result = json.loads(response.content)
        self.assertEqual(result["status"],20007)
        self.assertEqual(result["msg"],"每个商店一天只能签到一次哦")

    #获取扫描列表
    def get_shopScanlist(self):
        base_url = self.sheet1.cell_value(17,2)
        timestamp = self.common_method.timestamp
        phone = self.sheet1.cell_value(17,4)
        psw = self.sheet1.cell_value (17, 5)
        result_login = self.login.phone_login(phone=phone,psw=psw)
        uid = str(result_login["data"]["user"]["id"])
        cityid = self.sheet1.cell_value(17,6)
        lon = str(self.sheet1.cell_value(17,7))
        lat = str(self.sheet1.cell_value(17,8))
        pages = self.sheet1.cell_value (17, 9)
        authkey = result_login["data"]["authkey"]
        key_list = [uid,cityid,lon,lat,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        params = {
            "timestamp":timestamp,
            "pageSize":"30",
            "usertype":"1",          #预留参数，暂未使用
            "uid":uid,
            "cityid":cityid,
            "lon":lon,
            "lat":lat,
            "pages":pages,
            "key":key
        }
        response = requests.get(base_url,params=params)
        return response
    #扫描
    def get_scanGoods(self):
        base_url = self.sheet1.cell_value (18, 2)
        phone = self.sheet1.cell_value (18, 4)
        psw = self.sheet1.cell_value (18, 5)
        result_login = self.login.phone_login (phone, psw)
        uid = str (result_login["data"]["user"]["id"])
        shopid = self.sheet1.cell_value (18, 6)
        authkey = result_login["data"]["authkey"]
        barcode = self.sheet1.cell_value (18, 7)
        timestamp = self.dict["timestamp"]
        key_list = [shopid, uid, barcode, timestamp, authkey]
        key = self.common_method.get_key (key_list)
        params = {
            "uid": uid,
            "shopid": shopid,
            "barcode": barcode,
            "timestamp": timestamp,
            "key": key
        }
        response = requests.get (base_url, params)
        return response

    def test_scanGoods_01(self):
        u"测试扫描，未扫描过商品"
        self.get_shopScanlist()       
        response_scan = self.get_scanGoods()
        self.assertEqual(response_scan.status_code,200)
        print(response_scan.url)
        result = json.loads(response_scan.content)
        data = result["data"]
        data_len = len (data)
        status = result["status"]
        if data:
            self.assertNotEqual (data_len, 0)
            self.assertEqual(status,10001)
        elif result["status"] ==20007:
            self.assertEqual(result["msg"],"亲，你已经扫描过了哦")
        else:
            self.assertEqual(result["msg"], "没有这样的可扫描商品")

    def test_scanGoods_02(self):
        u"测试扫描，已扫描过商品"
        response_scan = self.get_scanGoods()
        self.assertEqual(response_scan.status_code,200)
        print(response_scan.url)
        result = json.loads(response_scan.content)
        self.assertEqual (len(result["data"]), 0)
        if result["status"] == 20007:
            self.assertEqual (result["msg"], "亲，你已经扫描过了哦")
        else:
            self.assertEqual(result["msg"], "没有这样的可扫描商品")

    def test_scanGoods_03(self):
        u"测试扫描，扫描条码不正确"
        base_url = self.sheet1.cell_value (18, 2)
        phone = self.sheet1.cell_value (18, 4)
        psw = self.sheet1.cell_value (18, 5)
        result_login = self.login.phone_login (phone, psw)
        uid = str (result_login["user_id"])
        shopid = self.sheet1.cell_value (18, 6)
        authkey = result_login["authkey"]
        barcode = self.sheet1.cell_value (18, 7)+"123456"
        timestamp = self.dict["timestamp"]
        appversion = self.dict["version"]
        os = self.dict["os"]
        key_list = [shopid, uid, barcode, timestamp, authkey]
        key = self.common_method.get_key (key_list)
        params = {
            "uid": uid,
            "shopid": shopid,
            "barcode": barcode,
            "timestamp": timestamp,
            "appversion": appversion,
            "os": os,
            "key": key
        }
        response = requests.get (base_url, params)
        self.assertEqual (response.status_code, 200)
        print (response.url)
        result = json.loads (response.content)
        data = result["data"]
        data_len = len (data)
        status = result["status"]
        self.assertEqual (data_len, 0)
        self.assertEqual (status, 20003)
        self.assertEqual(result["msg"],"没有这样的可扫描商品")
        print (result)







