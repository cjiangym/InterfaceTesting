import json
import unittest
import HTMLTestRunner
import time
import xlrd
import hashlib
import sys
import os
#用于命令行执行时对所有路径进行搜索（pydev在运行时会把当前工程的所有文件夹路径都作为包的搜索路径，而命令行默认只是搜索当前路径）
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

def all_case():
    #case_dir = "E:\\iSmartGo\\InterfaceTesting\\appTestcases"
    case_dir = curPath +"\\appTestcases"
    testcases = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    testcases.addTest(discover)
    print(testcases)
    return testcases

if __name__ == '__main__':
    #runner = unittest.TextTestRunner().run(all_case())
    testTime = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
    #report_path = "E:\\iSmartGo\\InterfaceTesting\\Results\\" + testTime+ "-testResult.html"
    report_path = curPath+"\\Results\\" +testTime+ "-testResult.html"
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"自动化接口测试报告",description=u"用例执行情况：")
    runner.run(all_case())
    fp.close()




