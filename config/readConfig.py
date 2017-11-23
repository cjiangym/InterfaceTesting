import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.text import MIMENonMultipart
from common.common_method import Common_method


class Readconfig():
    def send_email(self):
        #---------1、跟发件相关的参数-----------#
        smtpserver = "smtp.163.com"
        port = 0
        sender = "cjiangym@163.com"
        psw = "jym617609"
        #receiver = "cassiejiang@ismartgo.com"
        receiver = "testdept@ismartgo.com"
        # ----------2.编辑邮件的内容-----------#

        # 读文件
        file_path = Common_method().get_reportpath()       #从获得执行完之后的测试报告路径
        with open(file_path, "rb") as fp:
            mail_body = fp.read()
        msg = MIMEMultipart()
        msg["from"] = sender           # 发件人
        msg["to"] = receiver           # 收件人
        msg["subject"] = "APP接口测试报告" +Common_method().testTime        # 邮件主题
        # 正文
        body = MIMEText(mail_body, "html", "utf-8")
        msg.attach(body)
        # 附件
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="test_report.html"'
        msg.attach(att)

        # ----------3.发送邮件----------------#

        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver)     # 连服务器
            smtp.login(sender, psw)
        except:
            smtp = smtplib.SMTP_SSL(smtpserver, port)
            smtp.login(sender, psw)      # 登录
        smtp.sendmail(sender, receiver, msg.as_string()) # 发送
        smtp.quit()


