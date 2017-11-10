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


class BeaconPushTest(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testBeaconPush(self):
        base_url = "http://sv.ismartgo.cn:29090/appsv2/app/getAppSdkBeaconActivity.do"
        params = {
            "vs" :"9.3.5",
            "devRom" :"16GB",
            "appPackName" :"ismartgo.com",
            "appkey":"E2C56DB5-DFFB-48D2-B060-D0F5A71096E0",
            "beacons" :"{"major" : "10041", "minor" : "59167","uuid" : "FDA50693-A4E2-4FB1-AFCF-C6EB07647825"}",
            "devCode" :"32a7273c-61c6-4173-aae8-c7e33e330883",
            "devModel" : "iPhone7,2",
            "internetType" : "wifi",
            "appType" :"ios"

        }

