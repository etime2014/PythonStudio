#!/usr/bin/env python3
#-*- coding:utf-8 -*-
age = input("请输入年龄:")
Age = int(age)
if Age >= 18:
    print("adult")
elif 6<= Age < 18:
    print("teenager") 
else:
    print("kid")
input("Press Enter to exit...")
