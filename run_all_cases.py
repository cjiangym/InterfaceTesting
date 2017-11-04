import json
import unittest
import HTMLTestRunner
import time
import xlrd
import hashlib
import sys
import os
from config.readConfig import Readconfig
from common.common_method import Common_method
#用于命令行执行时对所有路径进行搜索（pydev在运行时会把当前工程的所有文件夹路径都作为包的搜索路径，而命令行默认只是搜索当前路径）
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

def all_case():
    #case_dir = "E:\\iSmartGo\\InterfaceTesting\\appTestcases"
    case_dir = curPath +"\\cases"
    testcases = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    testcases.addTest(discover)
    print(testcases)
    return testcases

if __name__ == '__main__':

    #使用HTMLTestRunner生成测试报告
    report_path = Common_method().get_reportpath()
        #curPath+"\\report\\" +testTime+ "-testResult.html"
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"APP接口测试报告",description=u"用例执行情况：")
    runner.run(all_case())
    fp.close()
    #-----发送邮件----------------------#
    send_email = Readconfig().send_email()







