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
        searchName = (sheet2.cell_value (2, 4))
        # 用户id
        uid = str(math.floor(sheet2.cell_value (2, 5)))
        # 页码
        page = "1"
        #每页数量
        pageSize ="30"
        dict = common_method.get_common_params()
        _sgts = dict["timestamp"]
        userkey = userkey = sheet2.cell_value(2,6)
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
        u"测试购物卡详情"
        common_method = Common_method()
        sheet2 = Common_method().get_excle_sheet2()
        base_url = sheet2.cell_value(3,2)
        # 搜索关键字
        cityid = "76"
        lon = "113.368719"
        lat = "23.152863"
        uid = str(math.floor(sheet2.cell_value (3, 5)))        # 用户id
        uuid = sheet2.cell_value(3,4)             #购物卡uuid
        dict = common_method.get_common_params()
        opdate = dict["timestamp"]
        devcode = dict["devcode"]
        userkey = sheet2.cell_value(3,6)
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
        #status = result["status"]
        #response_mobile = data["user"]["mobile"]
        #self.assertEqual(status,10001)
        #self.assertEqual(response_mobile,phone)
        print (result)

    def test_myshoppingcardList(self):
        u"测试我的购物卡列表"
        common_method = Common_method ()
        sheet2 = Common_method ().get_excle_sheet2 ()
        base_url = sheet2.cell_value (4, 2)
        userid = str(math.floor (sheet2.cell_value (4, 4)))  # 用户id
        userkey = str(math.floor (sheet2.cell_value (4, 5))) # Mobile或UnionID
        page = "1"
        authkey = sheet2.cell_value(4,6)
        opdate= "2017-10-23 18:14:08"
        key_list = [userid, userkey, opdate, page,authkey]
        key = common_method.get_key (key_list)
        dict = common_method.get_common_params()
        devcode = dict["devcode"]
        # 获取接口地址
        list1 = ["userid", "userkey", "page", "opdate", "key","devcode"]
        list2 = [userid, userkey, page, opdate, key,devcode]
        list3 = common_method.get_url (list1, list2)
        self.url = base_url + list3
        print (self.url)
        response = requests.get (self.url)
        result = json.loads (response.content)
        data_itmes = result["data"]["items"]
        if len (data_itmes) != 0:
            card_items = data_itmes[0]
            self.assertNotEqual (len (card_items), 0)
        status = result["status"]
        print (result)

    def test_getshoppingcardListByRetailid(self):
        u"根据零售商id获取购物卡列表"
        common_method = Common_method ()
        sheet2 = Common_method ().get_excle_sheet2 ()
        base_url = sheet2.cell_value (5, 2)
        userid = str(math.floor (sheet2.cell_value (5, 4)))  # 用户id
        userkey = str(math.floor (sheet2.cell_value (5, 5))) # Mobile或UnionID
        page = "1"
        authkey = sheet2.cell_value(5,6)
        opdate= "2017-10-23 18:14:08"
        key_list = [userid, userkey, opdate, page,authkey]
        key = common_method.get_key (key_list)
        retailid = str(math.floor(sheet2.cell_value(5,8)))
        type = str(math.floor(sheet2.cell_value(5,9)))
        dict = common_method.get_common_params()
        devcode = dict["devcode"]
        # 获取接口地址
        list1 = ["userid", "userkey", "page", "opdate", "key","retailid","type","devcode"]
        list2 = [userid, userkey, page, opdate,key,retailid,type,devcode]
        list3 = common_method.get_url (list1, list2)
        self.url = base_url + list3
        print (self.url)
        response = requests.get (self.url)
        result = json.loads (response.content)
        data_itmes = result["data"]["items"]
        if len(data_itmes)!=0:
            card_items = data_itmes[0]
            self.assertNotEqual(len (card_items), 0)
        status = result["status"]
        print (result)



    def test_scanIngoods_02(self):
        u"测试到店扫描，已扫描"
        common_method = Common_method ()
        sheet2 = Common_method ().get_excle_sheet2 ()
        base_url = sheet2.cell_value (6, 2)
        uid = str(math.floor (sheet2.cell_value (6, 4)))
        shopid = str(math.floor (sheet2.cell_value (6, 5)))
        barcode = str(math.floor(sheet2.cell_value(6,7)))
        dict = common_method.get_common_params()
        timestamp = dict["timestamp"]
        authkey = sheet2.cell_value (6, 6)
        key_list = [shopid, uid, barcode, timestamp,authkey]
        key = common_method.get_key (key_list)
        # 获取接口地址
        list1 = ["uid", "shopid", "barcode", "timestamp","key"]
        list2 = [uid, shopid, barcode, timestamp,key]
        list3 = common_method.get_url (list1, list2)
        self.url = base_url + list3
        print (self.url)
        response = requests.get (self.url)
        result = json.loads (response.content)
        data = result["data"]
        data_len = len (data)
        status = result["status"]
        self.assertEqual(data_len, 0)
        self.assertEqual (status,20007)
        print (result)
