import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime

from xlrd import xldate_as_tuple

from InterfaceTesting.run_all_cases import Common_method


#搜索促销信息商品、搜索网购赚商品，搜索零售商（我的关注页面），搜索礼品
class SearchTest(unittest.TestCase):
    commom_method = Common_method()
    sheet1 = commom_method.get_excle_sheet1()
    sheet2 = commom_method.get_excle_sheet2()

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_searchTaobao(self):
        u"测试搜索淘宝商品"
        base_url = self.sheet1.cell_value(19,2)
        searchName = (self.sheet1.cell_value (19, 4))    # 搜索关键字
        uid = str(math.floor(self.sheet1.cell_value (19, 5)))    # 用户id
        page = "1"       # 页码
        pageSize ="30"     #每页数量
        _sgts = self.commom_method.timestamp
        userkey = userkey = self.sheet1.cell_value(19,6)
        key_list = [uid,_sgts,userkey]
        _sgkey = self.commom_method.get_key(key_list)
        #获取接口地址
        params = {"searchName":searchName,"uid":uid,"page":page,"pageSize":pageSize,"_sgts":_sgts,"_sgkey":_sgkey}
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads (response.content)
        print(response.url)
        print (result)
        data = result["data"]
        status = result["status"]
        self.assertEqual(status,10001)
        self.assertNotEqual(len(data),0)

    def test_searchGoods(self):
        u"测试搜索促销商品"
        base_url = self.sheet1.cell_value(20,2)
        params = {
        "appversion" : self.commom_method.version,
        "devcode" : self.commom_method.devcode,
        "os" : self.commom_method.os,
        "cityid" : self.sheet1.cell_value(20,4),
        "lon" : self.sheet1.cell_value(20,5),
        "lat" : self.sheet1.cell_value(20,6),
        "keyword" : self.sheet1.cell_value (20, 7),
        "uid" : self.sheet1.cell_value(20,8)
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        print(response.url)
        result = json.loads(response.content)
        print(result)
        self.assertEqual(result["status"],10001)


