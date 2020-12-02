# import re
# import struct
# import binascii
# import sys
# import math
# import numpy as np
# # print(hex(1820))
# # # print(int(hex(32768 - abs(-49))) + 0x8000)
# # print(hex(0x7fcf + 0x8000))
# # a = '-1234'
# # print(a.isdigit())
# #
# # print(hex(32768 - 49 + 32768))
# s = '55 AA 0A 10 00 00 03 e8 03 04 05 06 07 08 09 10 0c 0e 0f cf 00 F0'
# # b = s[18:23].replace(" ", "")
# # s = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", b)  #去除前导0
# # mm = "0x"+s
# # nn = eval(mm)
# # print('十六进制： %s 转换成十进制为：%s' % (mm, nn))
#
# # d = binascii.b2a_hex(s.encode('utf-8'))
# # print(d)
# # s.strip() #去除首尾空格
# dealStr_new = s.replace(' ', '')
# # print(b)
# # recv1 = '0x' + str(b[12:20])
# # print(recv1)
# # recv2 = eval(recv1)
# # print(recv2)
# recv1 = '0x' + str(dealStr_new[12:20])  # 方位角速度
# recv1_angular_vel = eval(recv1)
# print(round(recv1_angular_vel/14800))
# recv2 = '0x' + str(dealStr_new[20:28])  # 俯仰角速度
# recv2_angular_vel = eval(recv2)
# print(recv2)
# recv3 = '0x' + str(dealStr_new[28:34])  # 方位角度
# recv3_angular_vel = eval(recv3)
# print(recv3)
# recv4 = '0x' + str(dealStr_new[34:40])  # 俯仰角度
# recv4_angular_vel = eval(recv4)
# print(recv4)
# # m=0
# # for j in s2:
# def add_1(binary_inpute):#二进制编码加1
#     _,out = bin(int(binary_inpute,2)-1).split("b")
#     return out
#
# def reverse(binary_inpute):#取反操作
#     binary_inpute = list(binary_inpute)
#     binary_out = binary_inpute
#     for epoch,i in enumerate(binary_out):
#         if i == "0":
#             binary_out[epoch] = "1"
#         else:
#             binary_out[epoch] = "0"
#     return "".join(binary_out)
#
# er = bin(int('0xFF64',16))[2:].zfill(16)
# print(er[0])
# if er[0] == '1':
#
#     a_reverse = reverse(er[1:])  # 取反
#     print(a_reverse)
#     a_add_1 = add_1(a_reverse)  # 二进制加1
#     print(-int(a_add_1,2))
# else:
#     print(int(er,2))
# #     print("0X"+j+",",end="")
# #     m+=1
# #     if m%10==0:
# #         print("\n",end="") #每10个字符换行
# # print("\n")
# # n = s2[7:21]
# # print(len(s2))#数组长度
#
# print(~5)
#
# recv3_er = bin(int('0x11', 16))[2:].zfill(16)
# print(int(recv3_er[1:], 2))
#
#
# def move(x, y, step, angle=0):
#     if 1 > 0:
#         nx = x + step * math.cos(angle)
#         ny = y - step * math.sin(angle)
#     return nx, ny
#
#
# print(np.random.normal())
# print(type(np.random.normal()))

# encoding:utf-8
# list形式
# import serial
#
# lit = [0xAA, 0x0A, 0x10, 0x60, 0x10, 0xFF, 0xff, 0xfe, 0x12, 0xFF, 0xff, 0xfe, 0xa9, 0x00, 0x00, 0xb9, 0x00, 0x00, 0xb9]
# # 等同于 lit = [224, 0, 0, 0, 0, 1, 44]
# t = None
# for i in range(len(lit)):
#     if i:
#         t ^= lit[i]
#     else:
#         t = lit[i] ^ 0
#
# print(type(lit[1]))
# print(hex(t)[2:])
# print(type(hex(t)))