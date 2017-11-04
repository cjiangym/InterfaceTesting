import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.text import MIMENonMultipart


#---------1、跟发件相关的参数-----------#
smtpserver = "smtp.163.com"
port = 0
sender = "cjiangym@163.com"
psw = "jym617609"
receiver = "705599396@qq.com"
# ----------2.编辑邮件的内容------
'''
subject = "这个是主题163"
body = '<p>这个是发送的163邮件</p>'   # 定义邮件正文为html格式
msg = MIMEText(body, "html", "utf-8")
msg['from'] = sender
msg['to'] = "705599396@qq.com"
msg['subject'] = subject
'''
# ----------2.编辑邮件的内容------
# 读文件
file_path = "D:\\InterfaceTesting\\InterfaceTesting\\report\\2017-11-01 12_56_01-testResult.html"
with open(file_path, "rb") as fp:
    mail_body = fp.read()
msg = MIMEMultipart()
msg["from"] = sender           # 发件人
msg["to"] = receiver           # 收件人
msg["subject"] = "这个我的主题"         # 主题
# 正文
body = MIMEText(mail_body, "html", "utf-8")
msg.attach(body)
# 附件
att = MIMEText(mail_body, "base64", "utf-8")
att["Content-Type"] = "application/octet-stream"
att["Content-Disposition"] = 'attachment; filename="test_report.html"'
msg.attach(att)


# ----------3.发送邮件------

try:
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)     # 连服务器
    smtp.login(sender, psw)
except:
    smtp = smtplib.SMTP_SSL(smtpserver, port)
    smtp.login(sender, psw)     # 登录
smtp.sendmail(sender, receiver, msg.as_string()) # 发送
smtp.quit()

'''
smtp = smtplib.SMTP()
smtp.connect(smtpserver)        # 连服务器
smtp.login(sender, psw)# 登录
smtp.sendmail(sender, receiver, msg.as_string())# 发送
smtp.quit()
'''


