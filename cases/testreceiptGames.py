import unittest
import requests
import json
import xlrd
import hashlib
import math
from common.common_method import Common_method
from common.getKey import Key
from config import  serverAddressConfig

class ReceiptGamesTests(unittest.TestCase):
    common_method = Common_method()
    sheet3 = common_method.get_excle_sheet(2)
    svrAddr = serverAddressConfig.gamesv_29096
    def setUp(self):
        pass
    def tearDown(self):
        pass

    #获取小票列表
    def get_receiptList(self):
        base_url = self.svrAddr + self.sheet3.cell_value(2,2)
        uid = self.sheet3.cell_value (2, 4)
        devcode = serverAddressConfig.devcode
        pages = "1"
        list_key = [uid,devcode,pages]
        key = Key.get_key(self,list_key)
        params_receiptList ={
            "appversion" : serverAddressConfig.version,
            "timestamp" : serverAddressConfig.timestamp,
            "os" :serverAddressConfig.os,
            "devcode" : devcode,
            "pages" : pages ,    # 页码
            "cityid" : self.sheet3.cell_value (2, 6),
            "cityname" : self.sheet3.cell_value (2, 5),
            "lon" : self.sheet3.cell_value (2, 7),
            "lat" : self.sheet3.cell_value (2, 8),
            "userid" : uid,
            "key" :key
        }
        response = requests.get(base_url,params_receiptList)
        return  response

    #获取内测的普通活动
    def get_game(self):
        try:
            response = self.get_receiptList()
        except:
            self.assertTrue(None,"获取小票列表失败")
        dict_game = {}
        result = json.loads(response.content)
        games = result["data"]["games"]
        for game in games:
            if "内测" in game["title"] and game["gametype"] ==1:      #gametype =1为普通拍立赚活动，gametype=2为众包活动
                dict_game = game
                break
        return dict_game

    # 获取内测的众包活动
    def get_zbgame(self):
        try:
            response = self.get_receiptList ()
        except:
            self.assertTrue(None,"获取小票列表失败")
        dict_game = {}
        result = json.loads(response.content)
        games = result["data"]["games"]
        for game in games:
            if "内测" in game["title"] and game["gametype"] == 2:  # gametype =1为普通拍立赚活动，gametype=2为众包活动
                dict_game = game
                break
        return dict_game

    def test_receipUpload(self):
        u"测试拍立赚上传小票 - 普通活动"
        base_url = self.sheet3.cell_value(3,2)
        url = self.svrAddr + base_url
        try:
            self.dict_game = self.get_game()                                      #内测的拍立赚普通活动活动
        except:
            self.assertTrue(None,"获取内测拍立赚活动失败")
        try:
            response_receiptList = self.get_receiptList()
        except:
            self.assertTrue(None,"获取小票列表失败")
        result_receiptList = json.loads(response_receiptList.content)       #不是内测的活动
        uid = self.sheet3.cell_value(3, 4)
        devcode = serverAddressConfig.devcode
        if self.dict_game:     #如果不存在内测活动，则取普通活动列表的第一个活动（使用内测活动不会产生过多脏数据）
            gameid = str(self.dict_game["gameid"])
            taskid = str(self.dict_game["taskid"])
            positionid = self.dict_game["positionid"]
        elif result_receiptList["data"]["games"]:
            for games in result_receiptList["data"]["games"]:
                if games["gametype"] != 2:         #不是众包活动
                    gameid = str(games["gameid"])
                    taskid = str(games["taskid"])
                    positionid = str(games["positionid"])
                    break
        else:
            self.assertEqual(result_receiptList["msg"],"拍立赚列表查询失败")
        list_key = [uid,devcode,gameid,taskid]
        key = Key.get_key(self,list_key)
        taskjson = [{
            "datasize":49531,
            "materialid":0,
            "dataurl":"http:\/\/img1.ismartgo.cn\/12162\/171101\/47d26454-4465-4cf5-a471-bd03c3b81dda.jpg",
            "timeseconds":"0"
        }]
        params = {
            "userid" :uid,
            "cityid": self.sheet3.cell_value(3, 5),
            "taskjson": json.dumps(taskjson),
            "lon": self.sheet3.cell_value (2, 7),
            "lat": self.sheet3.cell_value (2, 8),
            "positionid": positionid,
            "gameid": gameid,
            "taskid": taskid,
            "key": key,
            "devcode":devcode
        }
        response = requests.get(url,params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        if result["status"] ==10001:
            self.assertNotEqual(result["data"]["taskid"],None)
        elif result["status"] ==20005:
            self.assertEqual(result["msg"],"此活动每天只能参加一次")
            self.assertEqual(result["data"],None)
        else:
            self.assertEqual(result["msg"],"上传失败")

    def test_getZbgame(self):
        u"测试领取众包活动"
        base_url = self.svrAddr + self.sheet3.cell_value (4, 2)
        dict_zbgame = self.get_zbgame()  # 内测的众包活动活动
        response_receiptList = self.get_receiptList()
        self.assertEqual(response_receiptList.status_code,200)
        result_receiptList = json.loads (response_receiptList.content)  # 不是内测的活动
        devcode = serverAddressConfig.devcode
        uid = self.sheet3.cell_value (4, 4)
        gameid = ""
        if dict_zbgame:  # 如果不存在内测活动，则取活动列表的第一个活动（使用内测活动不会产生过多脏数据）
            gameid = str(dict_zbgame["gameid"])
            positionid = dict_zbgame["positionid"]
        elif result_receiptList["data"]["games"]:
            for games in result_receiptList["data"]["games"]:
                if games["gametype"] !=1:     #不是普通活动
                    gameid = str (games["gameid"])
                    positionid = str (games["positionid"])
                    break
        if gameid =="":
            self.assertEqual("","没有众包活动，无法领取")
        list_key = [uid, devcode, gameid]
        key = Key.get_key(self,list_key)
        params = {
            "userid": uid,
            "cityid": self.sheet3.cell_value (4, 5),
            "lon": self.sheet3.cell_value (2, 7),
            "lat": self.sheet3.cell_value (2, 8),
            "positionid": positionid,
            "gameid": gameid,
            "key": key,
            "devcode": devcode
        }
        response = requests.get(base_url, params=params)
        self.assertEqual (response.status_code, 200)
        result = json.loads (response.content)
        if result["status"] == 10001:
            self.assertNotEqual (result["data"]["taskid"], None)
        elif result["status"] == 20005:
            self.assertEqual (result["msg"], "当前活动其他任务未完成")
            self.assertEqual (result["data"], None)
        else:
            self.assertEqual (result["msg"], "领取失败")

    def test_myTaskList(self):
        u"测试我的列表"
        base_url = self.svrAddr + self.sheet3.cell_value(5,2)
        userid = self.sheet3.cell_value(5,4)
        devcode = serverAddressConfig.devcode
        pages = "1"
        key_list=[userid,devcode,pages]
        key = Key.get_key(self,key_list)
        params = {
            "status":self.sheet3.cell_value(5,8),
            "lon":self.sheet3.cell_value(5,6),
            "lat":self.sheet3.cell_value(5,7),
            "key":key,
            "cityid":self.sheet3.cell_value(5,5),
            "userid":userid,
            "pages":pages,
            "appversion":serverAddressConfig.version,
            "devcode":serverAddressConfig.devcode
        }
        response = requests.get(base_url,params=params)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertNotEqual(result["data"],None)
        self.assertNotEqual (result["data"]["tasks"],[])



