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
        base_url_serachKeywords = self.sheet1.cell_value(20,2)
        params_serachKeywords = {
        "appversion" : self.commom_method.version,
        "devcode" : self.commom_method.devcode,
        "os" : self.commom_method.os,
        "cityid" : self.sheet1.cell_value(20,4),
        "lon" : self.sheet1.cell_value(20,5),
        "lat" : self.sheet1.cell_value(20,6),
        "keyword" : self.sheet1.cell_value (20, 7),
        "uid" : self.sheet1.cell_value(20,8)
        }
        response_serachKeywords = requests.get(base_url_serachKeywords,params=params_serachKeywords)    #自动搜索关键字
        self.assertEqual(response_serachKeywords.status_code,200)
        print(response_serachKeywords.url)
        result_serachKeywords = json.loads(response_serachKeywords.content)
        print(result_serachKeywords)
        self.assertEqual(result_serachKeywords["status"],10001)

        #判断搜索类型：返回type =1 零售商搜索,type=2品类搜索type=3品牌搜索，type=4关键字搜索
        base_url_searchType = self.sheet1.cell_value(21,2)
        params_searchType = {
            "appversion" : self.commom_method.version,
            "devcode" : self.commom_method.devcode,
            "os" : self.commom_method.os,
            "searchname" :self.sheet1.cell_value(20,7),
            "uid" : self.sheet1.cell_value(20,8)
        }
        response_searchType = requests.get(base_url_searchType,params=params_searchType)     #判断搜索类型
        self.assertEqual (response_searchType.status_code, 200)
        print (response_searchType.url)
        result_searchType = json.loads (response_searchType.content)
        print (result_searchType)
        self.assertEqual (result_searchType["status"], 10001)
        self.assertNotEqual(len(result_searchType["data"]),0)

        #搜索促销商品:促销商品和促销商店接口不同
        if result_searchType["data"]["type"] ==1:
            base_url_search = self.sheet1.cell_value (23, 2)    #搜索促销商店
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
            print (response_search.url)
            self.assertEqual (result_search["status"], 10001)
            self.assertNotEqual (len (result_search["data"]), 0)
        else:
            base_url_search = self.sheet1.cell_value(22,2)    #搜索促销商品
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
            print(response_search.url)
            self.assertEqual(result_search["status"],10001)
            self.assertNotEqual(len(result_search["data"]),0)

    def test_searchRetails(self):
        u"测试搜索零售商（关注零售商功能）"
        base_url_search = self.sheet2.cell_value (6, 2)  # 搜索促销商店
        params_search = {
            "districtid": "-2",  # 默认值
            "shoptypeid": "-1",  # 默认值
            "townid": "-2",  # 默认值
            "distance": "",
            "cityid": math.floor(self.sheet2.cell_value (6, 5)),
            "lon": self.sheet2.cell_value (6, 7),
            "lat": self.sheet2.cell_value (6, 8),
            "nextpage": "",
            "searchname": self.sheet2.cell_value (6, 6),
            "userid": math.floor(self.sheet2.cell_value (6, 4))
        }
        response_search = requests.get (base_url_search, params=params_search)
        self.assertEqual (response_search.status_code, 200)
        result_search = json.loads (response_search.content)
        print (response_search.url)
        self.assertEqual (result_search["status"], 10001)
        self.assertNotEqual (len (result_search["data"]), 0)

    def test_searchGift(self):
        u"测试搜索礼品"
        base_url = self.sheet1.cell_value(24,2)
        params = {
            "appversion" : self.commom_method.version,
            "categoryId" : "0",
            "searchContent" : self.sheet1.cell_value(24,5),
            "pageSize" :30,
            "pages" :1 ,
            "timestamp" : self.commom_method.timestamp,
            "uid" : self.sheet1.cell_value(24,4),
            "os" :self.commom_method.os,
            "devcode" :self.commom_method.devcode
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        result_search = json.loads (response.content)
        print (response.url)
        self.assertEqual (result_search["status"], 10001)
        self.assertNotEqual (len (result_search["data"]), 0)







