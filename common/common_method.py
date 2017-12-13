import json
import unittest
import HTMLTestRunner
import time
import xlrd
import hashlib
import sys
import os
import requests
from config import serverAddressConfig
#用于命令行执行时对所有路径进行搜索（pydev在运行时会把当前工程的所有文件夹路径都作为包的搜索路径，而命令行默认只是搜索当前路径）
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Common_method():
    testTime = time.strftime("%Y-%m-%d", time.localtime())   #测试报告时间

    #测试用例excel第x个表格
    def get_excle_sheet(self,sheet_id):
        path = rootPath + "\\cases.xlsx"
        xlx_data = xlrd.open_workbook(path)
        # 取第x个表格
        sheet = xlx_data.sheet_by_index(sheet_id)
        return sheet

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

    #封装request.get方法
    def get_response(self,svrAddr,base_url,params):
        url = svrAddr+base_url
        response = requests.get(url=url,params=params)
        return response

    # 封装request.get方法
    def post_response(self,svrAddr, base_url, params):
        url = svrAddr + base_url
        response = requests.post(url=url, params=params,verify=False)
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
