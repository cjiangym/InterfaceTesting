import unittest
import requests
import json

import time
import xlrd
import math
from common.common_method import Common_method
from config import serverAddressConfig


#sessionId
class SessionIdTest(unittest.TestCase):
    common_method = Common_method()
    sheet1 = common_method.get_excle_sheet(0)
    svrAddr = serverAddressConfig.sv_29090
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_getSessionId(self):
        u"测试获取sessionId"
        base_url = self.sheet1.cell_value(2,2)
        lon = self.sheet1.cell_value(2,5)
        lat = self.sheet1.cell_value(2,6)
        uid = self.sheet1.cell_value(2,4)
        appversion = serverAddressConfig.version
        client = serverAddressConfig.os
        devcode = serverAddressConfig.devcode
        os = serverAddressConfig.os
        reqtime = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime ())
        userkey = "123"               #没有时默认为123
        params_names = ["appversion","devcode","client","lon","lat","uid","os","reqtime","userkey"]
        params_value = [appversion,devcode,client,lon,lat,uid,os,reqtime,userkey]
        response = self.common_method.get_response(self.svrAddr,base_url,params_names,params_value)
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertIn("expire",result["data"])
        self.assertEqual(result["status"],10001)
