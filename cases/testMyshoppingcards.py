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
from common.login import Login
from config import serverAddressConfig

class ShoppingCardsTest(unittest.TestCase):
    common_method = Common_method ()
    sheet2 = common_method.get_excle_sheet(1)
    sheet1 = common_method.get_excle_sheet(0)
    login = Login()
    phone = sheet1.cell_value(5, 5)
    psw = sheet1.cell_value(5, 6)
    result_login = login.phone_login(phone, psw)  # 手机号登录返回结果
    svrAddr = serverAddressConfig.svr2_29094

    def setUp(self):
        pass
    def tearDown(self):
        pass

     #获取购物卡列表
    def test_shoppingCardList(self):
        base_url = self.sheet2.cell_value(4, 2)
        url = self.svrAddr + base_url
        try:
            result_login = self.login.phone_login (self.phone, self.psw)  # 手机号登录返回结果
        except:
            self.assertTrue(None,"登录失败")
        userid = str(self.result_login["data"]["user"]["id"])  # 从登录接口获取返回的用户id
        userkey = self.result_login["data"]["user"]["mobile"]  # 从登录接口获取返回的Mobile
        page = "1"
        authkey = self.result_login["data"]["authkey"]
        date = xldate_as_tuple(self.sheet2.cell_value (4, 7),0)
        opdate = str (datetime.datetime(*date))
        type = (self.sheet2.cell_value (4, 8))
        list_key = [userid, userkey, opdate, page, authkey]
        key = Key.get_key(self,list_key)
        # 获取接口地址
        params = {
            "userid": userid,
            "userkey": userkey,
            "page": page,
            "opdate": opdate,
            "key": key,
            "type": type,
            "appversion": serverAddressConfig.version,
            "uid":userid,
            "timestamp":serverAddressConfig.timestamp,
            "devcode": serverAddressConfig.devcode
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual (result["status"], 10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual(result["data"],{})
        return result

    def test_shoppingcardDetail(self):
        u"测试购物卡详情"
        base_url = self.sheet2.cell_value(3, 2)
        url = self.svrAddr + base_url
        cityid = "76"
        lon = "113.368719"
        lat = "23.152863"
        opdate = serverAddressConfig.timestamp
        devcode = serverAddressConfig.devcode
        try:
            self.result_cardList = self.test_shoppingCardList()
        except:
            self.assertTrue(None,"获取购物卡列表失败")
        if self.result_cardList["data"]["items"]:       #从购物卡列表获取购物卡信息，没有购物卡则查看默认的购物卡
            uid =str(self.result_login["data"]["user"]["id"])
            uuid = self.result_cardList["data"]["items"][0]["uuid"]     #查看第一张购物卡
            authkey = self.result_login["data"]["authkey"]
        else:
            uid = self.sheet2.cell_value (3,5)              # 用户id
            uuid = self.sheet2.cell_value(3,4)             #购物卡uuid
            authkey = self.sheet2.cell_value(3,6)
        list_key = [uid,uuid,opdate,authkey]
        key = Key.get_key(self,list_key)
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
        response_cardDetail = requests.get(url,params=params)
        result = json.loads (response_cardDetail.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual (result["data"],{})

    def test_getshoppingcardListByRetailid(self):
        u"根据零售商id获取购物卡列表"
        base_url = self.sheet2.cell_value (5, 2)
        url = self.svrAddr + base_url
        try:
            result_login = self.login.phone_login(self.phone,self.psw)
        except:
            self.assertTrue(None,"登录失败")
        userid =str(self.result_login["data"]["user"]["id"])  # 用户id从登录接口获取
        userkey = self.result_login["data"]["user"]["mobile"] # Mobile或UnionID
        page = "1"
        authkey = self.result_login["data"]["authkey"]
        date = xldate_as_tuple(self.sheet2.cell_value(5, 7), 0)
        opdate = str(datetime.datetime (*date))
        list_key = [userid, userkey, opdate, page,authkey]
        key = Key.get_key(self,list_key)
        retailid = self.sheet2.cell_value(5,8)
        type = self.sheet2.cell_value(5,9)
        devcode = serverAddressConfig.version
        params = {
            "userid":userid,
            "userkey":userkey,
            "page":page,
            "opdate":opdate,
            "key":key,
            "retailid":retailid,
            "type":type,
            "devcode":devcode,
            "appversion":serverAddressConfig.version
        }
        response = requests.get(url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual (result["data"]["items"],[])

