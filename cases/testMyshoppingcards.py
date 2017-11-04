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

class ShoppingCardsTest(unittest.TestCase):
    common_method = Common_method ()
    sheet2 = common_method.get_excle_sheet2()
    sheet1 = common_method.get_excle_sheet1()
    login = Login()
    dict = common_method.get_common_params()
    phone = sheet1.cell_value(5, 5)
    psw = sheet1.cell_value (5, 6)
    response_login = login.phone_login (phone, psw)  # 手机号登录返回结果

    def setUp(self):
        pass
    def tearDown(self):
        pass

     #获取购物卡列表
    def get_shoppingCardList(self):
        base_url = self.sheet2.cell_value (4, 2)
        if self.response_login.status_code ==200:
            result_login = json.loads (self.response_login.content)
            if result_login["data"]:
                userid = str (result_login["data"]["user"]["id"])  # 从登录接口获取返回的用户id
                userkey = result_login["data"]["user"]["mobile"]  # 从登录接口获取返回的Mobile
                page = str (math.floor (self.sheet2.cell_value (4, 8)))
                authkey = result_login["data"]["authkey"]
                date = xldate_as_tuple (self.sheet2.cell_value (4, 7), 0)
                opdate = str (datetime.datetime(*date))
                type = (self.sheet2.cell_value (4, 9))
                key_list = [userid, userkey, opdate, page, authkey]
                key = self.common_method.get_key (key_list)
                dict = self.common_method.get_common_params ()
                devcode = dict["devcode"]
                # 获取接口地址
                params = {
                    "userid": userid,
                    "userkey": userkey,
                    "page": page,
                    "opdate": opdate,
                    "key": key,
                    "devcode": devcode,
                    "type": type
                }
                response = requests.get (base_url, params=params)
                return response
            return None

    def test_myshoppingCardList(self):
        u"测试我的购物卡列表 - 手机账号"
        response_cardList = self.get_shoppingCardList()
        if response_cardList.status_code ==200:
            result = json.loads (response_cardList.content)
            if result["data"]:
                print(response_cardList.url)
                print (result)
                data_itmes = result["data"]["items"]
                if len (data_itmes) != 0:
                    card_items = data_itmes[0]
                    self.assertNotEqual (len (card_items),0)
                self.assertEqual(result["status"],10001)
            else:
                self.assertEqual(result["msg"],0)
        else:
            self.assertEqual(response_cardList,200)

    def test_shoppingcardDetail(self):
        u"测试购物卡详情"
        base_url = self.sheet2.cell_value(3, 2)
        cityid = "76"
        lon = "113.368719"
        lat = "23.152863"
        opdate = self.dict["timestamp"]
        devcode = self.dict["devcode"]
        response_cardList = self.get_shoppingCardList()
        if response_cardList.status_code ==200 and self.response_login.status_code ==200:
            result_cardList = json.loads(response_cardList.content)
            result_login = json.loads(self.response_login.content)
            if result_cardList["data"]:
                if len(result_cardList["data"]["items"]) !=0:       #从购物卡列表获取购物卡信息，没有购物卡则查看默认的购物卡
                    uid =str(result_login["data"]["user"]["id"])
                    uuid = result_cardList["data"]["items"][0]["uuid"]     #查看第一张购物卡
                    authkey = result_login["data"]["authkey"]
                else:
                    uid = str(math.floor(self.sheet2.cell_value (3,5)))        # 用户id
                    uuid = self.sheet2.cell_value(3,4)             #购物卡uuid
                    authkey = self.sheet2.cell_value(3,6)
                key_list = [uid,uuid,opdate,authkey]
                key = self.common_method.get_key(key_list)
                params = {
                    "uid":uid,
                    "cityid":cityid,
                    "lon":lon,
                    "lat":lat,
                    "uuid":uuid,
                    "opdate":opdate,
                    "key":key,
                    "devcode":devcode
                }
                response_cardDetail = requests.get(base_url,params=params)
                result = json.loads (response_cardDetail.content)
                print(response_cardDetail.url)
                print (result)
                status = result["status"]
                self.assertEqual(status,10001)
                self.assertNotEqual(len(result["data"]),0)
            else:
                self.assertEqual(result_cardList["msg"],0)
        else:
            self.assertEqual(response_cardList,200)

    def test_getshoppingcardListByRetailid(self):
        u"根据零售商id获取购物卡列表"
        base_url = self.sheet2.cell_value (5, 2)
        if self.response_login ==200:
            result_login = json.loads(self.response_login.content)
            if result_login["data"]:
                userid =str(result_login["data"]["user"]["id"])  # 用户id从登录接口获取
                userkey = result_login["data"]["user"]["mobile"] # Mobile或UnionID
                page = "1"
                authkey = result_login["data"]["authkey"]
                date = xldate_as_tuple(self.sheet2.cell_value(5, 7), 0)
                opdate = str(datetime.datetime (*date))
                key_list = [userid, userkey, opdate, page,authkey]
                key = self.common_method.get_key (key_list)
                retailid = self.sheet2.cell_value(5,8)
                if isinstance(retailid,float):
                    retailid = str(math.floor(retailid))
                type = str(math.floor(self.sheet2.cell_value(5,9)))
                if isinstance(type,float):
                    type = str(math.floor(type))
                devcode = self.common_method.version
                params = {
                    "userid":userid,
                    "userkey":userkey,
                    "page":page,
                    "opdate":opdate,
                    "key":key,
                    "retailid":retailid,
                    "type":type,
                    "devcode":devcode
                }
                response = requests.get (base_url,params=params)
                result = json.loads (response.content)
                print(response.url)
                print (result)
                data_itmes = result["data"]["items"]
                self.assertEqual(response.status_code,200)
                if len(data_itmes)!=0:
                    card_items = data_itmes[0]
                    self.assertNotEqual(len (card_items),0)
                status = result["status"]
                self.assertEqual(status,10001)
            else:
                self.assertEqual(result_login["msg"],0)
        else:
            self.assertEqual(self.response_login.status_code,200)

