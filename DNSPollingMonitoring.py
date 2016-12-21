#!!/usr/bin/python
#coding=utf-8
#Auth: UA094
#Present for AWSH
#DAISUKI DESU KARA

import dns.resolver
import os
import httplib
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header

mailto_list=['iua094_zhai@aw-shanghai.cn'] #此处修改为收件人邮箱

#########################################
mail_host="smtp.163.com" #此处修改为发件服务器
mail_user="XXXXX"  #此处修改为发件人邮箱用户名，@前面的部分
mail_pass="YYYYY"  #此处修改为发件人邮箱密码
mail_postfix="163.com"  #此处修改为发件邮箱后缀，@后面的部分
##########################################

def send_mail(to_list,sub,content):  
    	me="Observer"+"<"+mail_user+"@"+mail_postfix+">"  
        msg = MIMEText(content,_subtype='plain',_charset='utf_8')  
        msg['Subject'] = sub  
        msg['From'] = me  
        msg['To'] = ";".join(mailto_list) 
        try:  
           server = smtplib.SMTP()  
           server.connect(mail_host,"25") #此处25代表端口号
           #server.starttls()  
           server.login(mail_user,mail_pass)  
           server.sendmail(me, to_list, msg.as_string())  
           server.close()  
           return True  
        except Exception, e:  
           print str(e)  
           return False

iplist=[] #Defined var for domain name list
appdomain = "www.awshanghai.com"   #此处是被监控网站域名，或者也可以激活下面一行变为每次手输
#Or input a URL when you run this script.
#appdomain = raw_input("Please input a URL:")

def get_iplist(domain=""):
	try:
		A = dns.resolver.query(domain, 'A')
	except Exception,e:
		print "dns resolver error:"+str(e)
		return
	for i in A.response.answer:
		for j in i.items:
			iplist.append(j.address)
	return True

def checkip(ip):
	checkurl = ip+":80"
	getcontent = ""
	httplib.socket.setdefaulttimeout(5)
	conn = httplib.HTTPConnection(checkurl)

	try:
		conn.request("GET", "/redmine",headers = {"Host":appdomain}) #此处对/redmine页面发起get请求并添加头文件
		r=conn.getresponse()
		getcontent=r.read(15)
		#print getcontent
	finally:
		if getcontent == "<html><body>You":
			print ip+"	[OK]"	#此处为终端显示，也可改为记录到log文件中，请随意
		else:
			print ip+"	[Error]"  #此处为终端显示，也可改为记录到log文件中，请随意
			#以下为邮件正文
			content = """
			・Redmine server is down !  Guys,  Let's Rack & Roll !
			・Redmineサーバがアクセス不能になりました！速やかに対応してください。
			・Redmine服务器无法访问。请迅速处理！"""
			send_mail(mailto_list,"Redmine Server is Down !",content) #此处为中间参数为邮件标题

if __name__=="__main__":
	if get_iplist(appdomain) and len(iplist)>0:
		for ip in iplist:
			checkip(ip)
	else:
		print "dns resolver error."