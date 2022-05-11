# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
#构建邮件头
from email.header import Header


# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '3499475017@qq.com'
password = 'eospvjlwtiradagj'


# 收信方邮箱
to_addr = 'qihao.yun@qq.com'



# 发信服务器
smtp_server = 'smtp.qq.com'

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
msg = MIMEText('come come come and have a look','plain','utf-8')
msg['From'] = Header("77")
msg['To'] = Header("Akizuki Cat")
msg['Subject'] = Header('maowo updated 4 u')


server = smtplib.SMTP_SSL(smtp_server)
server.connect(smtp_server,465)

server.login(from_addr, password)

server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()
