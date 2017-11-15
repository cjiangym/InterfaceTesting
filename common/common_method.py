import json
import unittest
import HTMLTestRunner
import time
import xlrd
import hashlib
import sys
import os
import requests
#用于命令行执行时对所有路径进行搜索（pydev在运行时会把当前工程的所有文件夹路径都作为包的搜索路径，而命令行默认只是搜索当前路径）
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Common_method():
    testTime = time.strftime("%Y-%m-%d", time.localtime())   #测试报告时间
    version = "401000"
    os = "iOS"
    devcode = "e895ec8c-6c18-4a27-a509-328cd252b6fa"
    timestamp = "20171018160129"

    #获取固定值
    def get_common_params(self):
        dict = {"version":"401000",
                "os":"iOS",
                "devcode":"e895ec8c-6c18-4a27-a509-328cd252b6fa",
                "timestamp":"20171018160129"
                }
        return dict

    #测试用例excel第一个表格
    def get_excle_sheet1(self):
        path = rootPath + "\\cases.xlsx"
        xlx_data = xlrd.open_workbook (path)
        # 取第一个表格
        sheet1 = xlx_data.sheet_by_index (0)
        return sheet1

        # 测试用例excel第二个表格
    def get_excle_sheet2(self):
        path = rootPath +"\\cases.xlsx"
        xlx_data = xlrd.open_workbook(path)
        sheet2 = xlx_data.sheet_by_index(1)
        return sheet2

        # 测试用例excel第三个表格
    def get_excle_sheet3(self):
        path = rootPath + "\\cases.xlsx"
        xlx_data = xlrd.open_workbook(path)
        sheet3 = xlx_data.sheet_by_index(2)
        return sheet3

        # 测试用例excel第三个表格
    def get_excle_sheet4(self):
        path = rootPath + "\\cases.xlsx"
        xlx_data = xlrd.open_workbook (path)
        sheet4 = xlx_data.sheet_by_index (3)
        return sheet4

    # 测试用例excel第五个表格
    def get_excle_sheet5(self):
        path = rootPath + "\\cases.xlsx"
        xlx_data = xlrd.open_workbook (path)
        # 取第一个表格
        sheet5 = xlx_data.sheet_by_index(4)
        return sheet5

    #字符串加密
    def get_key(self,list_key):
        pre_key=list_key[0]
        for key_value in list_key[1:]:
            pre_key = pre_key+"#"+key_value
        pre_key = pre_key+"#smartg02ol5"
        key = hashlib.md5(pre_key.encode("utf-8")).hexdigest()
        return key

    #获取测试报告
    def get_reportpath(self):
        report_path = rootPath + "\\report\\" + self.testTime + "-testResult.html"
        return report_path

    # 获取已关注列表
    def get_mySubscribeList(self, uid):
        base_url = "http://svr2.ismartgo.cn:29094/retailsv/app/retails/getSubscribeList.do"
        params = {
            "userid": uid,
            "page": 1
        }
        response = requests.get (base_url, params=params)
        return response


'''
    #将传入的参数拼接成接口地址
    def get_url(self,list1,list2):   #list1为固定值：version，os,devcode等；list2为动态值version的值，os的值，devcode的值
        def function(parms1,param2):
            return parms1+"="+param2
        list3 = list(map(function,list1,list2))  #将list1,list2按“=”号连接
        list4 = list3[0]
        for parms in list3[1:]:
            list4 = list4+"&"+parms
        return list4
'''
