#!!/usr/bin/python
#coding=utf-8
#Auth: Kuritan

import dns.resolver
import os
import httplib
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header

mailto_list=['zhai_yujia2@venustech.com.cn'] 

#########################################
mail_host="smtp.163.com"
mail_user="salamander321" 
mail_pass="kirsi103"
mail_postfix="163.com"
##########################################

def send_mail(to_list,sub,content):  
    	me="Observer"+"<"+mail_user+"@"+mail_postfix+">"  
        msg = MIMEText(content,_subtype='plain',_charset='utf_8')  
        msg['Subject'] = sub  
        msg['From'] = me  
        msg['To'] = ";".join(mailto_list) 
        try:  
           server = smtplib.SMTP()  
           server.connect(mail_host,"25")
           #server.starttls()  
           server.login(mail_user,mail_pass)  
           server.sendmail(me, to_list, msg.as_string())  
           server.close()  
           return True  
        except Exception, e:  
           print str(e)  
           return False

iplist=[] #Defined var for domain name list
appdomain = "www.awshanghai.com"
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
		conn.request("GET", "/redmine",headers = {"Host":appdomain})
		r=conn.getresponse()
		getcontent=r.read(15)
		#print getcontent
	finally:
		if getcontent == "<html><body>You":
			print ip+"	[OK]"
			content = """
			・Redmine server is down !  Guys,  Let's Rack & Roll !
			・Redmineサーバがアクセス不能になりました！速やかに対応してください。
			・Redmine服务器无法访问。请迅速处理！"""
			send_mail(mailto_list,"DNS_Error",content)
		else:
			print ip+"	[Error]"

if __name__=="__main__":
	if get_iplist(appdomain) and len(iplist)>0:
		for ip in iplist:
			checkip(ip)
	else:
		print "dns resolver error."