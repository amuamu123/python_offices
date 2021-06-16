import time,schedule

def mqq(filepath,imagepath):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.image import MIMEImage
    form_addr='1234@qq.com'
    password='mygpbxwgaoozbfjj'#输入示范、16位无空格
    to_addrs=['1234@qq.com']#多个人用，隔开例：['1234@qq.com','1234@sina.com']
    smtp_server='smtp.qq.com'
    #smtp_server='smtp.sina.cn' #选择你对应的邮箱接口
    #smtp_server='smtp.163.com' #选择你对应的邮箱接口
    #smtp_server = 'smtp.gmail.com' #选择你对应的邮箱接口
    msg=MIMEMultipart()                             #发送附件的方法定义为一个变量
    content='邮件正文' #随便写什么都行
    msg.attach(MIMEText(content,'html', 'utf-8'))  #发送正文

    att=MIMEText(open(filepath,'rb').read(),'base64','utf-8')    #调用传送附件模块，传送附件
    att["Content-Type"]='application/octet-stream' #修改下方filename为文件名（文本型，不支持中文）
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", "中文附件.XLSX"))
    #att["Content-Disposition"]='attachment;filename="English.XLSX"'  #附件描述外层要用单引号
    msg.attach(att)#发送附件

    mime_images = '<p><img src="cid:imageid{0}" alt="imageid{0}"></p>'.format(1)#批量添加图片时需要修改值
    mime_img = MIMEImage(open(imagepath, 'rb').read(), _subtype='octet-stream')
    mime_img.add_header('Content-ID', 'imageid')
    msg.attach(mime_img)#上传图片至缓存空间
    mime_html = MIMEText('<html><body><p>{0}</p>{1}</body></html>'.format('', mime_images), 'html', 'utf-8')# 上传正文
    msg.attach(mime_html)# 添加附图至正文

    msg['From'] = Header(form_addr)
    msg['To']=','.join(to_addrs)
    msg['Subject']=Header('python')
    server=smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server,465)
    server.login(form_addr,password)
    server.sendmail(form_addr,to_addrs,msg.as_string())
    server.quit()

def job():
    mqq(r"语法地图.XLSX",r'cat-5233986.jpg')
schedule.every().friday.at("18:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)