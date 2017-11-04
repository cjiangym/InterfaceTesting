import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from InterfaceTesting.run_all_cases import Common_method


class DailySignTest(unittest.TestCase):

    common_method = Common_method ()
    sheet1 = common_method.get_excle_sheet1 ()
    sheet2 = common_method.get_excle_sheet2()
    dict = common_method.get_common_params()

    def setUp(self):
        pass
    def setUp(self):
        pass

    def test_dailySign(self):
        u"测试每日签到"
        base_url = self.sheet1.cell_value(14,2)
        uid = str(math.floor(self.sheet1.cell_value(14,4)))
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
        uid = math.floor(self.sheet1.cell_value(15,4))
        cityName = self.sheet1.cell_value(15,5)
        lon = self.sheet1.cell_value(15,6)
        lat = self.sheet1.cell_value(15,7)
        pages = str(math.floor(self.sheet1.cell_value(15,8)))
        pageSize = "30"         #页码大小，一页30条
        appversion = self.dict["version"]
        os = self.dict["os"]
        timestamp = self.dict["timestamp"]
        devcode = self.dict["devcode"]
        params = {
            "uid":uid,
            "cityName":cityName,
            "lon":lon,
            "lat":lat,
            "pages":pages,
            "pageSize":pageSize,
            "appversion":appversion,
            "os":os,
            "devcode":devcode,
        }
        response = requests.get(base_url,params=params)
        return response

     #签到
    def get_shopSign_result(self):
        response_shopSignlist = self.get_shopSignlist ()
        result_shopSignlist = json.loads (response_shopSignlist.content)
        print (response_shopSignlist.url)
        base_url = self.sheet1.cell_value (16, 2)
        beacon = "0"  # 签到beacon，没有则为0
        shop_list = math.floor (self.sheet1.cell_value (16, 6))  # 去签到列表的第x个数组数据
        lon = result_shopSignlist["data"]["shopSignList"][shop_list]["lon"]  # 从签到列表获取经纬度
        lat = result_shopSignlist["data"]["shopSignList"][shop_list]["lat"]
        uid = str (math.floor (self.sheet1.cell_value (16, 4)))
        shopId = str(result_shopSignlist["data"]["shopSignList"][shop_list]["shopid"])
        cityId = str(math.floor (self.sheet1.cell_value (16, 5)))  # 从签到列表获取shopid
        os = self.dict["os"]
        devcode = self.dict["version"]
        timestamp = self.dict["timestamp"]
        appversion = self.dict["version"]
        authkey = self.sheet1.cell_value (16, 7)
        key_list = [uid, shopId, beacon, timestamp, authkey]
        key = self.common_method.get_key (key_list)
        params = {
            "beacon": beacon,
            "lon": lon,
            "lat": lat,
            "uid": uid,
            "shopId": shopId,
            "cityId": cityId,
            "os": os,
            "devcode": devcode,
            "timestamp": timestamp,
            "appversion": appversion,
            "key": key
        }
        response = requests.get (base_url, params=params)
        return response

    def test_shopSign_01(self):
        u"测试到店签到"
        response_shoplist = self.get_shopSignlist()  #签到列表返回结果
        response = self.get_shopSign_result()        #签到返回结果
        print(response.url)
        result_shoplist = json.loads(response_shoplist.content)
        result = json.loads(response.content)
        print(result)
        shop_list = math.floor (self.sheet1.cell_value (16, 6))  # 去签到列表的第x个数组数据,用于验证签到结果
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(len(result["data"]),0)
        self.assertEqual(result_shoplist["data"]["shopSignList"][shop_list]["userIsSign"],"Y")   #签到列表已签到，userIsSign=Y

    def test_shopSign_02(self):
        u"测试已签到后，再次签到"
        response = self.get_shopSign_result()
        result = json.loads(response.content)
        print(result)
        self.assertEqual(result["status"],20007)
        self.assertEqual(result["msg"],"每个商店一天只能签到一次哦")

    #获取扫描列表
    def get_shopScanlist(self):
        base_url = self.sheet1.cell_value(17,2)
        appversion = self.dict["version"]
        devcode = self.dict["devcode"]
        os = self.dict["os"]
        timestamp = self.dict["timestamp"]
        pageSize = "30"
        usertype ="1"     #预留参数，暂未使用
        uid = str(math.floor(self.sheet1.cell_value(17,4)))
        cityid = str(math.floor(self.sheet1.cell_value(17,5)))
        lon = str(self.sheet1.cell_value(17,6))
        lat = str(self.sheet1.cell_value(17,7))
        pages = math.floor(self.sheet1.cell_value (17, 8))
        authkey = self.sheet1.cell_value(17,9)
        key_list = [uid,cityid,lon,lat,timestamp,authkey]
        key = self.common_method.get_key(key_list)
        params = {
            "appversion":appversion,
            "devcode":devcode,
            "os":os,
            "timestamp":timestamp,
            "pageSize":pageSize,
            "usertype":usertype,
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
        uid = str (math.floor (self.sheet1.cell_value (18, 4)))
        shopid = self.sheet1.cell_value (18, 5)
        authkey = self.sheet1.cell_value (18, 6)
        barcode = self.sheet1.cell_value (18, 7)
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
        self.assertNotEqual (data_len, 0)
        self.assertEqual(status,10001)
        print (result)

    def test_scanGoods_02(self):
        u"测试扫描，已扫描过商品"
        self.get_shopScanlist()
        response_scan = self.get_scanGoods()
        self.assertEqual(response_scan.status_code,200)
        print(response_scan.url)
        result = json.loads(response_scan.content)
        data = result["data"]
        data_len = len (data)
        status = result["status"]
        self.assertEqual (data_len, 0)
        self.assertEqual(status,20007)
        print (result)

    def test_scanGoods_03(self):
        u"测试扫描，扫描条码不正确"
        base_url = self.sheet1.cell_value (18, 2)
        uid = str (math.floor (self.sheet1.cell_value (18, 4)))
        shopid = self.sheet1.cell_value (18, 5)
        authkey = self.sheet1.cell_value (18, 6)
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







