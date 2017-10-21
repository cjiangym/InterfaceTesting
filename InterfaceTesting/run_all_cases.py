import unittest
import HTMLTestRunner
import time
import xlrd
import hashlib

def all_case():
    case_dir = "E:\\iSmartGo\\InterfaceTesting\\appTestcases"
    testcases = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    testcases.addTest(discover)
    print(testcases)
    return testcases

if __name__ == '__main__':
    #runner = unittest.TextTestRunner().run(all_case())
    testTime = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
    report_path = "E:\iSmartGo\InterfaceTesting\\Results\\" + testTime+ "-testResult.html"
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"自动化接口测试报告",description=u"用例执行情况：")
    runner.run(all_case())
    fp.close()

#通用方法
class Common_method():
    #固定传值
    version = "401000"
    os = "iOS"
    devcode = "e895ec8c-6c18-4a27-a509-328cd252b6fa"
    timestamp = "20171018160129"

    #获取固定值
    def get_static_params(self):
        dict = {"version":"401000",
                "os":"iOS",
                "devcode":"e895ec8c-6c18-4a27-a509-328cd252b6fa",
                "timestamp":"20171018160129"
                }
        return dict

    #测试用例excel第一个表格
    def get_excle_sheet1(self):
        xlx_data = xlrd.open_workbook ("E:\\iSmartGo\\InterfaceTesting\\Cases.xlsx")
        # 取第一个表格
        sheet1 = xlx_data.sheet_by_index (0)
        return sheet1

    #字符串加密
    def get_key(list_key):
        pre_key=list_key[0]
        for key_value in list_key[1:]:
            pre_key = pre_key+"#"+key_value
        pre_key = pre_key+"#smartg02ol5"
        key = hashlib.md5(pre_key.encode("utf-8")).hexdigest()
        return key

    #将传入的参数拼接成接口地址
    def get_url(list1,list2):   #list1为固定值：version，os,devcode等；list2为动态值version的值，os的值，devcode的值
        def function(parms1,param2):
            return parms1+"="+param2
        list3 = list(map(function,list1,list2))  #将list1,list2按“=”号连接
        list4 = list3[0]
        for parms in list3[1:]:
            list4 = list4+"&"+parms
        return list4

    #获取参数
    #def get_params(list):


