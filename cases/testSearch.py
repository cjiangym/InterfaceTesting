import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime
from xlrd import xldate_as_tuple
from common.common_method import Common_method
from common.getKey import Key
from config import serverAddressConfig


#搜索促销信息商品、搜索网购赚商品，搜索零售商（我的关注页面），搜索礼品
class SearchTest(unittest.TestCase):
    commom_method = Common_method()
    sheet1 = commom_method.get_excle_sheet(0)
    sheet2 = commom_method.get_excle_sheet(1)
    svrAddr_29090 = serverAddressConfig.sv_29090
    svrAddr_29094 = serverAddressConfig.svr2_29094

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
        _sgts = serverAddressConfig.timestamp
        userkey = userkey = self.sheet1.cell_value(19,6)
        list_key = [uid,_sgts,userkey]
        _sgkey = Key.get_key(self,list_key)
        #获取接口地址
        params = {
            "searchName":searchName,
            "uid":uid,
            "page":page,
            "pageSize":pageSize,
            "_sgts":_sgts,
            "_sgkey":_sgkey
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads (response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)

    def test_searchGoods(self):
        u"测试搜索促销商品"
        base_url = self.sheet1.cell_value(20,2)
        url = self.svrAddr_29090 + base_url
        params = {
            "appversion" : serverAddressConfig.version,
            "devcode" : serverAddressConfig.devcode,
            "os" : serverAddressConfig.os,
            "cityid" : self.sheet1.cell_value(20,4),
            "lon" : self.sheet1.cell_value(20,5),
            "lat" : self.sheet1.cell_value(20,6),
            "keyword" : self.sheet1.cell_value (20, 7),
            "uid" : self.sheet1.cell_value(20,8)
        }
        response_serachKeywords = requests.get(url,params=params)         #自动搜索关键字
        self.assertEqual(response_serachKeywords.status_code,200)
        result_serachKeywords = json.loads(response_serachKeywords.content)
        self.assertEqual(result_serachKeywords["status"],10001)

        #判断搜索类型：返回type =1 零售商搜索,type=2品类搜索type=3品牌搜索，type=4关键字搜索
        base_url_searchType = self.svrAddr_29090 + self.sheet1.cell_value(21,2)
        params_searchType = {
            "appversion" : serverAddressConfig.version,
            "devcode" : serverAddressConfig.devcode,
            "os" : serverAddressConfig.os,
            "searchname" :self.sheet1.cell_value(20,7),
            "uid" : self.sheet1.cell_value(20,8)
        }
        response_searchType = requests.get(base_url_searchType,params=params_searchType)     #判断搜索类型
        self.assertEqual (response_searchType.status_code, 200)
        result_searchType = json.loads (response_searchType.content)
        self.assertEqual (result_searchType["status"], 10001)
        self.assertNotEqual(result_searchType["data"],None)

        #搜索促销商品:促销商品和促销商店接口不同
        if result_searchType["data"]["type"] ==1:
            base_url_search = self.svrAddr_29090 + self.sheet1.cell_value (23, 2)    #搜索促销商店
            params_search = {
                "districtid": "-2",  # 默认值
                "shoptypeid": "-1",  # 默认值
                "townid": "-2",       # 默认值
                "distance" : "",
                "cityName": self.sheet1.cell_value (22, 4),
                "lon": self.sheet1.cell_value (22, 5),
                "lat": self.sheet1.cell_value (22, 6),
                "pageSize": "30",
                "pages": self.sheet1.cell_value (22, 7),
                "searchname": self.sheet1.cell_value (20, 7),
                "uid": self.sheet1.cell_value (20, 8)
            }
            response_search = requests.get (base_url_search, params=params_search)
            self.assertEqual (response_search.status_code, 200)
            result_search = json.loads (response_search.content)
            self.assertEqual (result_search["status"], 10001)
            self.assertNotEqual (result_search["data"],None)
        else:
            base_url_search = self.svrAddr_29090 + self.sheet1.cell_value(22,2)    #搜索促销商品
            params_search = {
                "categoryId" : "-1",       #默认值
                "categoryId2" : "-1" ,      #默认值
                "districtId" : "-2",        #默认值
                "shopTypeId" : "-1",        #默认值
                "townId"  : "-2",            #默认值
                "brandIds" : "",
                "cityName" : self.sheet1.cell_value(22,4),
                "lon"  : self.sheet1.cell_value(22,5),
                "lat" : self.sheet1.cell_value(22,6),
                "pageSize" :"30",
                "pages" :self.sheet1.cell_value(22,7),
                "searchname" : self.sheet1.cell_value(20,7),
                "uid" :self.sheet1.cell_value(20,8)
            }
            response_search = requests.get(base_url_search,params=params_search)
            self.assertEqual(response_search.status_code,200)
            result_search = json.loads(response_search.content)
            self.assertEqual(result_search["status"],10001)
            self.assertNotEqual(result_search["data"],None)

    def test_searchGift(self):
        u"测试搜索礼品"
        base_url = self.svrAddr_29090 + self.sheet1.cell_value(24,2)
        params = {
            "appversion" : serverAddressConfig.version,
            "categoryId" : "0",
            "searchContent" : self.sheet1.cell_value(24,5),
            "pageSize" :30,
            "pages" :1 ,
            "timestamp" : serverAddressConfig.timestamp,
            "uid" : self.sheet1.cell_value(24,4),
            "os" :serverAddressConfig.os,
            "devcode" :serverAddressConfig.devcode
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        result_search = json.loads (response.content)
        self.assertEqual (result_search["status"], 10001)
        self.assertNotEqual (result_search["data"], None)







