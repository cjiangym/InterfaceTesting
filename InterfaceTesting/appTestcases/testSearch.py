import unittest
import requests
import json
import xlrd
import hashlib
import math
import  datetime

from xlrd import xldate_as_tuple

from InterfaceTesting.run_all_cases import Common_method


#手机号登录、微信登录测试
class LoginTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass


    def test_searchTaobao_01(self):
        u"测试搜索淘宝商品"
        common_method = Common_method()
        sheet2 = Common_method().get_excle_sheet2()
        base_url = sheet2.cell_value(2,2)
        # 搜索关键字
        searchName = (sheet2.cell_value (2, 5))
        # 用户id
        uid = str(math.floor(sheet2.cell_value (2, 6)))
        # 页码
        page = "1"
        #每页数量
        pageSize ="30"
        dict = common_method.get_common_params()
        _sgts = dict["timestamp"]
        userkey = userkey = sheet2.cell_value(2,7)
        key_list = [uid,_sgts,userkey]
        _sgkey = common_method.get_key(key_list)
        #获取接口地址
        list1 = ["searchName","uid","page","pageSize","_sgts","_sgkey"]
        list2= [searchName,uid,page,pageSize,_sgts,_sgkey]
        list3 = common_method.get_url(list1,list2)
        self.url =base_url+list3
        print(self.url)
        response = requests.get(self.url)
        result = json.loads (response.content)
        #data = result["data"]
       # status = result["status"]
        #response_mobile = data["user"]["mobile"]
        #self.assertEqual(status,10001)
        #self.assertEqual(response_mobile,phone)
        print (result)

    def test_shoppingcardDetail(self):
        u"测试手机号码登录，正确的手机号、密码"
        common_method = Common_method()
        sheet2 = Common_method().get_excle_sheet2()
        base_url = sheet2.cell_value(3,2)
        # 搜索关键字
        cityid = "76"
        lon = "113.368719"
        lat = "23.152863"
        uid = str(math.floor(sheet2.cell_value (3, 6)))        # 用户id
        uuid = sheet2.cell_value(3,5)             #购物卡uuid
        dict = common_method.get_common_params()
        opdate = dict["timestamp"]
        devcode = dict["devcode"]
        userkey = sheet2.cell_value(3,7)
        key_list = [uid,uuid,opdate,userkey]
        key = common_method.get_key(key_list)
        #获取接口地址
        list1 = ["uid","cityid","lon","lat","uuid","opdate","key","devcode"]
        list2= [uid,cityid,lon,lat,uuid,opdate,key,devcode]
        list3 = common_method.get_url(list1,list2)
        self.url =base_url+list3
        print(self.url)
        response = requests.get(self.url)
        result = json.loads (response.content)
        #data = result["data"]
       # status = result["status"]
        #response_mobile = data["user"]["mobile"]
        #self.assertEqual(status,10001)
        #self.assertEqual(response_mobile,phone)
        print (result)

    def test_myshoppingcardList(self):
        u"测试获取我的购物卡列表"
        common_method = Common_method ()
        sheet2 = Common_method ().get_excle_sheet2 ()
        base_url = sheet2.cell_value (4, 2)
        userid = str(math.floor (sheet2.cell_value (4, 5)))  # 用户id
        userkey = str(math.floor (sheet2.cell_value (4, 6))) # Mobile或UnionID
        page = "1"
        authkey = sheet2.cell_value(4,7)
        opdate= "2017-10-23 18:14:08"
        key_list = [userid, userkey, opdate, page,authkey]
        key = common_method.get_key (key_list)
        # 获取接口地址
        list1 = ["userid", "userkey", "page", "opdate", "key"]
        list2 = [userid, userkey, page, opdate,  key]
        list3 = common_method.get_url (list1, list2)
        self.url = base_url + list3
        print (self.url)
        response = requests.get (self.url)
        result = json.loads (response.content)
        # data = result["data"]
        # status = result["status"]
        # response_mobile = data["user"]["mobile"]
        # self.assertEqual(status,10001)
        # self.assertEqual(response_mobile,phone)
        print (result)
