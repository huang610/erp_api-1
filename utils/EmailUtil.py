from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,yagmail
from config.setting import report_path




class SendEmail:
    def __init__(self,smtp_addr,username,password,recv,
                 title,content=None,file=None):
        '''
        初始化 smtp地址，用户名，密码，接收邮件者，邮件标题，邮件内容，邮件附件
        :param smtp_addr:
        :param username:
        :param password:
        :param recv:
        :param title:
        :param content:
        :param file:
        :return:
        '''
        self.smtp_addr = smtp_addr
        self.username = username
        self.password = password
        self.recv = recv
        self.title = title
        self.content = content
        self.file = file

    def send_mail(self):
        '''
        发送邮件方法
        1.初始化邮件信息
        2.邮件附件
        3.发送邮件
        :return:
        '''
        msg = MIMEMultipart()
        msg.attach(MIMEText(self.content,_charset="utf-8"))
        msg["Subject"] = self.title
        msg["From"] = self.username
        msg["To"] = self.recv

        #判断是否附件
        if self.file:
        #MIMEText读取文件
            att = MIMEText(open(self.file).read())
        #设置内容类型
            att["Content-Type"] = 'application/octet-stream'
        #设置附件头
            att["Content-Disposition"] = 'attachment;filename="%s"'%self.file
        #将内容附加到邮件主体中
            msg.attach(att)
        #登录邮件服务器
        self.smtp = smtplib.SMTP(self.smtp_addr,port=25)
        self.smtp.login(self.username,self.password)

        self.smtp.sendmail(self.username,self.recv,msg.as_string())



# if __name__ == "__main__":
    # from config.Conf import ConfigYaml
    # email_info = ConfigYaml().get_email_info()
    # smtp_addr = email_info["smtpserver"]
    # username = email_info["username"]
    # password = email_info["password"]
    # recv = email_info["receiver"]
    # msg='''
	# 各位好！
	# 	本次接口测试结果如下：
	# 		详细信息见附件【%s】。
	# '''%(report_path)
    # # attachfilepat = '/Users/huangrong/Desktop/erp_api/report/html/index.html'
    # email = SendEmail(smtp_addr,username,password,recv,msg,report_path)
    # email.send_mail()