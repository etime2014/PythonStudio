#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import time
import getpass
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./SetRTX1200_parameter.ini')

ip = config.get('General', 'ip_router')
username = config.get('General', 'username')
password = config.get('General', 'password')
adminpw = getpass.getpass("Administrator PW for %s: " % ip)


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip,username=username,password=password)

print "Sucessfully login to ", ip

command = ssh_client.invoke_shell()

command.send("administrator\n")
time.sleep(1)
command.send("%s\n" % adminpw)
command.send("ip lan1 address 172.12.12.12/24\n")
command.send("save\n")
time.sleep(1)
output = command.recv(65535)
print output

ssh_client.close
