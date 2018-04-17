#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import time
import getpass
import ConfigParser
import datetime

config = ConfigParser.ConfigParser()
config.read('./SetRTX1200_Config_parameter_test.ini')
#パラメータファイルを読み込む

ssh_ip = config.get('Variable', 'ip_lan3')
#ssh_ip = config.get('Constant', 'ip_router_hq')
username = config.get('Variable', 'username')
#username = config.get('Constant', 'username_hq')
password = config.get('Constant', 'password')
#password = config.get('Constant', 'password_hq')

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
adminpw = config.get('Constant', 'admin_pw_hq')

command.send("administrator\n")
time.sleep(0.5)
command.send("%s\n" % adminpw)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
buff = ''
command.send('show config \n')
time.sleep(3)
d = datetime.datetime.today()
try:
    while not buff.endswith('---つづく---'):
        command.send('\s\n')
        time.sleep(3)
        buff = command.recv(65535)
        if not buff.endswith('#'):
            Log_Before_Path = config.get('Variable', 'log_before_path') + d.strftime("_%Y-%m-%d-[%H:%M:%S]") + '.log'
            b = open(Log_Before_Path,'w')
            b.write(buff)
            b.close()
            break
except Exception, e:
    print "error info:"+str(e)
print "本社ルータ作業前config" + Log_Before_Path + "が保存されました。"
print "config解析作業に入ります......"
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
time.sleep(2)
check = open(Log_Before_Path,'r')
tmpdata = check.read()
tunnel_select = 'tunnel select ' + config.get('Variable', 'tunnel_num')
router = tmpdata.find(tunnel_select)
if router != -1:
    print "対象トンネルすでに存在するので、作業中断します！"
    check.close()
    ssh_client.close()
else:
    print "対象トンネルは利用可能の状態になっております......"
    time.sleep(2)
    check.close()
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

check_nat = open(Log_Before_Path, 'r')
lines = check_nat.readlines()
check_nat.close()
nat_list_now = ""
for line in lines:
    if line.startswith("ip lan1 nat descriptor "):
        nat_config = line[:-1]
        nat_list_now = nat_config.replace('ip lan1 nat descriptor ', '')

if nat_list_now:
        print "既存nat descriptor特定しました、追加いたします......"
        time.sleep(1)
else:
        print "既存nat descriptor特定できませんでした、新規追加いたします......"
        time.sleep(1)

#ip lan1 nat descriptor 5 6 7 8 9 10 14 15 16
command.send('ip lan1 nat descriptor ' + nat_list_now  + ' ' +  config.get('Variable', 'nat_router_type_num')  + ' ' +  config.get('Variable', 'nat_teletime_type_num')  + ' ' +  config.get('Variable', 'nat_printer_type_num') + '\n')
time.sleep(0.5)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#ip route 172.25.30.0/24 gateway tunnel 4
command.send('ip route ' + config.get('Variable', 'ip_network') + config.get('Constant', 'ip_lan1_prefix') + ' gateway tunnel ' + config.get('Variable', 'tunnel_num') + '\n')
#tunnel select 4
command.send('tunnel select ' + config.get('Variable', 'tunnel_num') + '\n')
# ipsec tunnel 104
command.send('ipsec tunnel ' + config.get('Variable', 'ipsec_tunnel_num') + '\n')
#  ipsec sa policy 104 4 esp 3des-cbc sha-hmac
command.send('ipsec sa policy ' + config.get('Variable', 'ipsec_tunnel_num') + ' ' + config.get('Variable', 'tunnel_num') + ' esp 3des-cbc sha-hmac' + '\n')
#  ipsec ike keepalive use 4 on icmp-echo 172.25.30.1 10 5
command.send('ipsec ike keepalive use ' + config.get('Variable', 'tunnel_num') + ' on icmp-echo ' + config.get('Variable', 'ip_lan1') + ' 10 5' + '\n')
#  ipsec ike local address 4 121.1.133.74
command.send('ipsec ike local address ' + config.get('Variable', 'tunnel_num') + ' ' + config.get('Constant', 'ip_router_pubilc_hq') + '\n')
time.sleep(0.5)
#  ipsec ike pre-shared-key 4 text Gaiasystem8811
command.send('ipsec ike pre-shared-key ' + config.get('Variable', 'tunnel_num') + ' ' + config.get('Constant', 'PS_key_type') + ' ' + config.get('Constant', 'PS_key_content') + '\n')
#  ipsec ike remote address 4 183.77.252.91
command.send('ipsec ike remote address ' + config.get('Variable', 'tunnel_num') + ' ' + config.get('Variable', 'branch_public_address') + '\n')
# tunnel enable 4
command.send('tunnel enable ' + config.get('Variable', 'tunnel_num') + '\n') 
time.sleep(0.5)
#command.send("tunnel select none\n")
command.send('tunnel select none' + '\n')
# nat descriptor type 11 nat
command.send('nat descriptor type ' + config.get('Variable', 'nat_router_type_num') + ' nat' + '\n') 
#nat descriptor address outer 11 172.25.100.151
command.send('nat descriptor address outer ' + config.get('Variable', 'nat_router_type_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_router') + '\n')
time.sleep(0.5)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#nat descriptor address inner 11 172.25.30.1
command.send('nat descriptor address inner ' + config.get('Variable', 'nat_router_type_num') + ' ' + config.get('Variable', 'ip_lan1') + '\n')
#nat descriptor static 11 1 172.25.100.151=172.25.30.1 28
command.send('nat descriptor static ' + config.get('Variable', 'nat_router_type_num') + ' ' + config.get('Constant', 'nat_table_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_router') + '=' + config.get('Variable', 'ip_lan1') + ' ' + config.get('Constant', 'nat_router_device_num') + '\n')
time.sleep(0.5)
#nat descriptor type 12 nat
command.send('nat descriptor type ' + config.get('Variable', 'nat_teletime_type_num') + ' nat' + '\n') 
#nat descriptor address outer 12 172.25.100.179
command.send('nat descriptor address outer ' + config.get('Variable', 'nat_teletime_type_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_teletime') + '\n')
time.sleep(0.5)
#nat descriptor address inner 12 172.25.30.50
command.send('nat descriptor address inner ' + config.get('Variable', 'nat_teletime_type_num') + ' ' + config.get('Variable', 'ip_teletime_branch') + '\n')
#nat descriptor static 12 1 172.25.100.179=172.25.30.50 1
time.sleep(0.5)
command.send('nat descriptor static ' + config.get('Variable', 'nat_teletime_type_num') + ' ' + config.get('Constant', 'nat_table_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_teletime') + '=' + config.get('Variable', 'ip_teletime_branch') + ' ' + config.get('Constant', 'nat_teletime_device_num') + '\n')
#nat descriptor type 13 nat
command.send('nat descriptor type ' + config.get('Variable', 'nat_printer_type_num') + ' nat' + '\n') 
time.sleep(0.5)
#nat descriptor address outer 13 172.25.100.180
command.send('nat descriptor address outer ' + config.get('Variable', 'nat_printer_type_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_printer') + '\n')
#nat descriptor address inner 13 172.25.30.100
command.send('nat descriptor address inner ' + config.get('Variable', 'nat_printer_type_num') + ' ' + config.get('Variable', 'ip_printer_branch') + '\n')
#nat descriptor static 13 1 172.25.100.180=172.25.30.100 1
command.send('nat descriptor static ' + config.get('Variable', 'nat_printer_type_num') + ' ' + config.get('Constant', 'nat_table_num') + ' ' + config.get('Variable', 'ip_gaiaaddress_branch_printer') + '=' + config.get('Variable', 'ip_printer_branch') + ' ' + config.get('Constant', 'nat_printer_device_num') + '\n')
time.sleep(0.5)
command.send('save' + '\n')
time.sleep(2)
print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
output = command.recv(65535)
#今まで入力した内容を受信
print output
Log_Path = config.get('Variable', 'log_add_path') + d.strftime("_%Y-%m-%d-[%H:%M:%S]") + '.log'
f = open(Log_Path,'w')
f.write(output)
#指定の場所にログとして保存
print "-------------------------------------------------------------------------------------"
print "今回の作業履歴を" + Log_Path + "に保存しました。"
print "-------------------------------------------------------------------------------------"
f.close()

print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
buff_a = ''
command.send('show config \n')
time.sleep(3)
try:
    while not buff_a.endswith('---つづく---'):
        command.send('\s\n')
        time.sleep(3)
        buff_a = command.recv(65535)
        if not buff_a.endswith('#'):
            Log_After_Path = config.get('Variable', 'log_after_path') + d.strftime("_%Y-%m-%d-[%H:%M:%S]") + '.log'
            z = open(Log_After_Path,'w')
            z.write(buff_a)
            z.close()
            break
except Exception, e:
    print "error info:"+str(e)
print "-------------------------------------------------------------------------------------"
print "本社ルータ作業後config" + Log_After_Path + "が保存されました。"
print "-------------------------------------------------------------------------------------"

ssh_client.close()
#開けっ放しにしないよう