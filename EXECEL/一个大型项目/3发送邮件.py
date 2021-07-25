import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import winreg

def mqq(filepath,to_addrs):
    form_addr='1234@qq.com'
    password='mygpbxwgaoozbfjj'#输入示范、16位无空格
    to_addrs=[to_addrs]#多个人用，隔开例：['1234@qq.com','1234@sina.com']
    smtp_server='smtp.qq.com'
    msg=MIMEMultipart()              #发送附件的方法定义为一个变量
    content='邮件正文' #随便写什么都行
    msg.attach(MIMEText(content,'html', 'utf-8'))  #发送正文

    att=MIMEText(open(filepath,'rb').read(),'base64','utf-8')    #调用传送附件模块，传送附件
    att["Content-Type"]='application/octet-stream' #修改下方filename为文件名（文本型，不支持中文）
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", "中文附件.XLSX"))
    msg.attach(att)#发送附件

    msg['From'] = Header(form_addr)
    msg['To']=','.join(to_addrs)
    msg['Subject']=Header('python')
    server=smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server,465)
    server.login(form_addr,password)
    server.sendmail(form_addr,to_addrs,msg.as_string())
    server.quit()

dict = {'1班':'123456789@qq.com','2班':'123456789@qq.com'}

Desktoppath = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'), "Desktop")[0]#获取电脑系统桌面路径
topname = Desktoppath+"\\考场汇总\\"
for i in dict:
    mqq(topname+i+'考试表.xlsx',dict[i])