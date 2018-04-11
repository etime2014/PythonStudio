#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import time
import getpass
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./SetRTX1200_Config_parameter.ini')
#パラメータファイルを読み込む

ssh_ip = config.get('General', 'ip_lan3')
username = config.get('General', 'username')
password = config.get('General', 'password')

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try :
    ssh_client.connect(hostname=ssh_ip,username=username,password=password)
except paramiko.ssh_exception.AuthenticationException, e:
    print "==========================ルーターアカウント情報間違っているよ！=========================="
    raise
    ssh_client.close()
except Exception, e:
    print(e)
    ssh_client.close()
else:
    print "Sucessfully login to ", ssh_ip

command = ssh_client.invoke_shell()
command.settimeout(10)
#adminpw = getpass.getpass("administrator PW for %s: " % ssh_ip)
adminpw = config.get('General', 'admin_pw')

command.send("administrator\n")
time.sleep(0.5)
command.send("%s\n" % adminpw)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
buff = ''
command.send('show config \n')
time.sleep(3)
try:
    while not buff.endswith('---つづく---'):
        command.send(' \n')
        time.sleep(3)
        buff = command.recv(65535)
        if not buff.endswith('#'):
            Log_Before_Path = config.get('HQ-Router', 'log_before')
            b = open(Log_Before_Path,'w')
            b.write(buff)
            b.close()
            break
except Exception, e:
    print "error info:"+str(e)
print "本社ルータ作業前configが保存されました。"
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
print "config解析作業に入ります......"
check = open(Log_Before_Path)
tmpdata = check.read()
tunnel_select = 'tunnel select ' + config.get('Tunnel', 'tunnel_num')
router = tmpdata.find(tunnel_select)
if router == -1:
    print "対象トンネル見つかりませんでした、作業中断します。"
    check.close()
    ssh_client.close()
else:
    print "対象トンネル確認できました、削除作業に入ります......"
    check.close()

print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#ip route 172.25.30.0/24 gateway tunnel 4
command.send('no ip route ' + config.get('General', 'ip_network') + config.get('General', 'ip_lan1_prefix') + ' gateway tunnel ' + config.get('Tunnel', 'tunnel_num') + '\n')
#tunnel select 4
#command.send('tunnel select ' + config.get('Tunnel', 'tunnel_num') + '\n')
# ipsec tunnel 104
command.send('no ipsec tunnel ' + config.get('Tunnel', 'ipsec_tunnel_num') + '\n')
#  ipsec sa policy 104 4 esp 3des-cbc sha-hmac
command.send('no ipsec sa policy ' + config.get('Tunnel', 'ipsec_tunnel_num') + ' ' + config.get('Tunnel', 'tunnel_num') + ' esp 3des-cbc sha-hmac' + '\n')
#  ipsec ike keepalive use 4 on icmp-echo 172.25.30.1 10 5
command.send('no ipsec ike keepalive use ' + config.get('Tunnel', 'tunnel_num') + ' on icmp-echo ' + config.get('General', 'ip_lan1') + ' 10 5' + '\n')
#  ipsec ike local address 4 121.1.133.74
command.send('no ipsec ike local address ' + config.get('Tunnel', 'tunnel_num') + ' ' + config.get('Tunnel', 'hq_public_address') + '\n')
time.sleep(0.5)
#  ipsec ike pre-shared-key 4 text Gaiasystem8811
command.send('no ipsec ike pre-shared-key ' + config.get('Tunnel', 'tunnel_num') + ' ' + config.get('Pre-shared-key', 'type') + ' ' + config.get('Pre-shared-key', 'content') + '\n')
#  ipsec ike remote address 4 183.77.252.91
command.send('no ipsec ike remote address ' + config.get('Tunnel', 'tunnel_num') + ' ' + config.get('Tunnel', 'branch_public_address') + '\n')
# tunnel enable 4
command.send('no tunnel enable ' + config.get('Tunnel', 'tunnel_num') + '\n') 
# nat descriptor type 11 nat
command.send('no nat descriptor type ' + config.get('HQ-Router', 'nat_router_type_num') + ' nat' + '\n') 
#nat descriptor address outer 11 172.25.100.151
command.send('no nat descriptor address outer ' + config.get('HQ-Router', 'nat_router_type_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_router') + '\n')
time.sleep(0.5)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#nat descriptor address inner 11 172.25.30.1
command.send('no nat descriptor address inner ' + config.get('HQ-Router', 'nat_router_type_num') + ' ' + config.get('General', 'ip_lan1') + '\n')
#nat descriptor static 11 1 172.25.100.151=172.25.30.1 28
command.send('no nat descriptor static ' + config.get('HQ-Router', 'nat_router_type_num') + ' ' + config.get('HQ-Router', 'nat_table_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_router') + '=' + config.get('General', 'ip_lan1') + ' ' + config.get('HQ-Router', 'nat_router_device_num') + '\n')
#nat descriptor type 12 nat
command.send('no nat descriptor type ' + config.get('HQ-Router', 'nat_teletime_type_num') + ' nat' + '\n') 
#nat descriptor address outer 12 172.25.100.179
command.send('no nat descriptor address outer ' + config.get('HQ-Router', 'nat_teletime_type_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_teletime') + '\n')
#nat descriptor address inner 12 172.25.30.50
command.send('no nat descriptor address inner ' + config.get('HQ-Router', 'nat_teletime_type_num') + ' ' + config.get('General', 'ip_teletime_branch') + '\n')
time.sleep(0.5)
#nat descriptor static 12 1 172.25.100.179=172.25.30.50 1
command.send('no nat descriptor static ' + config.get('HQ-Router', 'nat_teletime_type_num') + ' ' + config.get('HQ-Router', 'nat_table_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_teletime') + '=' + config.get('General', 'ip_teletime_branch') + ' ' + config.get('HQ-Router', 'nat_teletime_device_num') + '\n')
#nat descriptor type 13 nat
command.send('no nat descriptor type ' + config.get('HQ-Router', 'nat_printer_type_num') + ' nat' + '\n') 
#nat descriptor address outer 13 172.25.100.180
command.send('no nat descriptor address outer ' + config.get('HQ-Router', 'nat_printer_type_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_printer') + '\n')
#nat descriptor address inner 13 172.25.30.100
command.send('no nat descriptor address inner ' + config.get('HQ-Router', 'nat_printer_type_num') + ' ' + config.get('General', 'ip_printer_branch') + '\n')
#nat descriptor static 13 1 172.25.100.180=172.25.30.100 1
command.send('no nat descriptor static ' + config.get('HQ-Router', 'nat_printer_type_num') + ' ' + config.get('HQ-Router', 'nat_table_num') + ' ' + config.get('HQ-Router', 'ip_gaiaaddress_branch_printer') + '=' + config.get('General', 'ip_printer_branch') + ' ' + config.get('HQ-Router', 'nat_printer_device_num') + '\n')
time.sleep(0.5)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

command.send('save' + '\n')
time.sleep(1.5)
output = command.recv(65535)
#今まで入力した内容を受信
Log_Path = config.get('HQ-Router', 'del_log_path')
f = open(Log_Path,'w')
f.write(output)
#指定の場所にログとして保存
print output
print "-------------------------------------------------------------------------------------"
print Log_Path + "が保存されました。"
print "-------------------------------------------------------------------------------------"

f.close()
ssh_client.close()
#開けっ放しにしないよう