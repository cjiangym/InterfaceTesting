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
from config import  serverAddressConfig

class MessageTest(unittest.TestCase):

    def setUp(self):
        self.svrAddr = serverAddressConfig.message_29078
        self.sheet4 = Common_method.get_excle_sheet(self,3)
    def tearDown(self):
        pass

    def test_messageCenter(self):
        u"测试获取消息中心模块"
        base_url = self.svrAddr + self.sheet4.cell_value(5,2)
        params = {
            "uid" : self.sheet4.cell_value(5,4),
            "timestamp" : serverAddressConfig.timestamp,
            "devcode" : serverAddressConfig.devcode,
            "version" : serverAddressConfig.version
        }
        response = requests.post(base_url,params=params,verify=False)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"]["messages"][0]["title"],"系统消息")

    def test_messageList(self):
        u"测试查看系统消息"
        base_url = self.svrAddr + self.sheet4.cell_value(6,2)
        params = {
            "uid" : self.sheet4.cell_value(6,4),
            "timestamp" : serverAddressConfig.timestamp,
            "devcode" : serverAddressConfig.devcode,
            "version" : serverAddressConfig.version,
            "module": 1,
            "nextpage":0
        }
        response = requests.post(base_url,params=params,verify=False)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual(result["data"],{})
        self.assertNotEqual (result["data"]["messages"],[])
        return  result

    def test_readMessage(self):
        u"测试阅读消息"
        base_url = self.svrAddr + self.sheet4.cell_value(7,2)
        try:
            self.result_msgList = self.test_messageList()
            self.msgid = self.result_msgList["data"]["messages"][0]["msgid"]
            self.lasttime = self.result_msgList["data"]["messages"][0]["createtime"]
        except:
            self.assertTrue(None,"获取消息列表失败")
        for message in self.result_msgList["data"]["messages"]:           #查找是否有未读消息，如果有则取出消息id，没有则阅读第一条消息'''
            if message["isread"] == 0:
                self.msgid = message["msgid"]
                self.lasttime = message["createtime"]
                break
        params = {
            "uid" :self.sheet4.cell_value(6,4),
            "module" : "1",
            "msgid" : self.msgid,
            "lasttime" : self.lasttime,
            "timestamp" : serverAddressConfig.timestamp,
            "version": serverAddressConfig.version
        }
        response = requests.post(base_url,params = params,verify=False)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result["status"],10001)
        self.assertEqual(result["data"],None)




