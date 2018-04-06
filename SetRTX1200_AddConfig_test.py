#!/usr/bin/env python
# -*- coding:utf-8 -*-

#こちらは、どこでも事務所ルータを設置する時のスクリプトです
#実行するために、python2.X環境が必要
#ルータ側は事前にSSH設定を済んで、lan3にIPを設定し、SSHリモート可能の状態に設置してください
#ユーザ情報も手動でコンフィグを入れてください
#sshd service on
#sshd host key generate 2048
#下記IPは例です
#ip lan3 address 192.168.0.12/24
#ip route 192.168.0.0/24 gateway 192.168.0.5
#administrator password *
#login user test *
#事前準備のコンフィグ設定後、saveをお忘れなく

import paramiko
import time
import getpass
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./SetRTX1200_AddConfig_parameter.ini')

ssh_ip = config.get('General', 'ip_lan3')
username = config.get('General', 'username')
password = config.get('General', 'password')
adminpw = getpass.getpass("administrator PW for %s: " % ssh_ip)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ssh_ip,username=username,password=password)

print "Sucessfully login to ", ssh_ip

command = ssh_client.invoke_shell()

command.send("administrator\n")
time.sleep(0.5)
command.send("%s\n" % adminpw)
command.send("login timer 21474836\n")
time.sleep(0.5)
command.send("ip filter source-route on\n")
command.send("ip filter directed-broadcast on\n")
command.send("pp select 1\n")
command.send("pp always-on on\n")
command.send("pppoe use lan2\n")
command.send("pppoe auto connect on\n")
command.send("pppoe auto disconnect off\n")
command.send("pp auth accept pap chap\n")
time.sleep(0.5)
command.send("ppp lcp mru on 1454\n")
command.send("ppp ipcp ipaddress on\n")
command.send("ppp ipcp msext on\n")
command.send("ppp ipv6cp use off\n")
command.send("ip pp mtu 1454\n")
command.send("ip pp secure filter in 1040 1041 2000\n")
command.send("ip pp secure filter out 1010 1011 1012 1013 1014 1015 3000 dynamic 105 106\n")
time.sleep(0.5)
command.send("pp enable 1\n")
command.send("pp select none\n")
command.send("ip filter 1010 reject * * udp,tcp 135 *\n")
command.send("ip filter 1011 reject * * udp,tcp * 135\n")
command.send("ip filter 1012 reject * * udp,tcp netbios_ns-netbios_ssn *\n")
command.send("ip filter 1013 reject * * udp,tcp * netbios_ns-netbios_ssn\n")
command.send("ip filter 1014 reject * * udp,tcp 445 *\n")
command.send("ip filter 1015 reject * * udp,tcp * 445\n")
time.sleep(1)
command.send("ip filter 1040 pass * * udp * 500\n")
command.send("ip filter 1041 pass * * esp\n")
command.send("ip filter 2000 reject * *\n")
command.send("ip filter 3000 pass * *\n")
command.send("ip filter dynamic 105 * * tcp\n")
command.send("ip filter dynamic 106 * * udp\n")
time.sleep(0.5)
command.send("ipsec auto refresh on\n")
command.send("syslog debug on\n")
command.send("dhcp service server\n")
command.send("dhcp server rfc2131 compliant except remain-silent\n")

command.send("dns private address spoof on\n")
time.sleep(0.5)

#ここからカスタマイズエリア,parameter.iniを使う
#command.send("ip route default gateway pp 1 filter 1040 1041 gateway tunnel 3\n")
command.send('ip route default gateway pp ' + config.get('PP', 'pp_num') + ' filter 1040 1041 gateway tunnel ' + config.get('Tunnel', 'tunnel_num') + '\n')
time.sleep(1)
#command.send("console prompt paqua-wakayama\n")
command.send('console prompt ' + config.get('General', 'console_prompt') + '\n')
#command.send("ip lan1 address 172.25.32.1/24\n")
command.send('ip lan1 address ' + config.get('General', 'ip_lan1') + '\n')
#command.send("pp select 1\n")
command.send('pp select ' + config.get('PP', 'pp_num') + '\n')
#command.send("pp auth myname U6393MS232D@atson.net s69ategg\n")
command.send('pp auth myname ' + config.get('PP', 'pp_user') + ' ' + config.get('PP', 'pp_pw') + '\n')
command.send("pp select none\n")
#command.send("tunnel select 3\n")
command.send('tunnel select ' + config.get('Tunnel', 'tunnel_num') + '\n')
time.sleep(0.5)
#command.send("ipsec tunnel 103\n")
command.send('ipsec tunnel ' + config.get('Tunnel', 'ipsec_tunnel_num') + '\n')
#command.send("ipsec sa policy 103 3 esp 3des-cbc sha-hmac\n")
command.send('ipsec sa policy ' + config.get('Tunnel', 'ipsec_tunnel_num') + ' ' + config.get('Tunnel', 'tunnel_num') + ' esp 3des-cbc sha-hmac' + '\n')
#command.send("ipsec ike keepalive use 3 on icmp-echo 172.25.100.254 10 5\n")
command.send('ipsec ike keepalive use ' + config.get('Tunnel', 'tunnel_num') + ' on icmp-echo ' + config.get('General', 'ip_router_hq') + ' 10 5' + '\n')
time.sleep(0.5)
#command.send("ipsec ike pre-shared-key 3 text Gaiasystem8811\n")
command.send('ipsec ike pre-shared-key ' + config.get('Tunnel', 'tunnel_num') + ' ' + config.get('Pre-shared-key', 'type') + ' ' + config.get('Pre-shared-key', 'content') + '\n')
#command.send("ipsec ike remote address 3 121.1.133.74\n")
command.send('ipsec ike remote address ' + config.get('Tunnel', 'tunnel_num') + ' ' + config.get('Tunnel', 'remote_address') + '\n')
#command.send("tunnel enable 3\n")
command.send('tunnel enable ' + config.get('Tunnel', 'tunnel_num') + '\n')
#command.send("tunnel select none\n")
command.send('tunnel select none' + '\n')
time.sleep(0.5)
#command.send("dhcp scope 1 172.25.32.21-172.25.32.28/24\n")
command.send('dhcp scope ' + config.get('DHCP', 'scope_num')  + ' ' + config.get('DHCP', 'scope_range') + '\n')
#command.send("dhcp scope option 1 dns=172.31.102.210,172.31.102.143\n")
command.send('dhcp scope option ' + config.get('DHCP', 'scope_num') + ' dns=' + config.get('DHCP', 'dhcp_primary_dns') + ',' + config.get('DHCP', 'dhcp_secondary_dns') + '\n')
#command.send("dns server 202.224.32.1 202.224.32.2\n")
command.send('dns server ' + config.get('General', 'net_primary_dns') + ' ' + config.get('General', 'net_secondary_dns') + '\n')
#command.send("dns server pp 1\n")
command.send('dns server pp ' + config.get('PP', 'pp_num') + '\n')
time.sleep(0.5)

#command.send("no ip route 192.168.0.0/24 gateway 192.168.0.5\n")
command.send('no ip route ' + config.get('General', 'default_route_intra') + '\n')
#command.send("no ip lan3 address 192.168.0.12/24\n")
command.send('no ip lan3 address ' + config.get('General', 'ip_lan3') + config.get('General', 'ip_lan3_prefix')  + '\n')
command.send("save\n")
time.sleep(3)
output = command.recv(65535)
print output
time.sleep(1)
print "PP内local address未設定!!!"
print "トンネル内ipsec ike local address未設定!!!"

ssh_client.close