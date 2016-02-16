#!/usr/bin/env python3
#-*- coding:utf-8 -*-
x = input("请输入身高(M):")
height = float(x)
y = input("请输入体重(KG):")
weight = float(y)
bmi = weight/(height*height)
if bmi < 18.5:
    print("过轻")
elif 18.5 <= bmi < 25:
    print("正常")
elif 25 <= bmi < 28:
    print("过重")
elif 28 <= bmi < 32:
    print("肥胖")
else:
    print("严重肥胖")
input("Press Enter to exit...")
