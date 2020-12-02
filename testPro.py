#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Lian Yue

import sys
from Pro import Ui_MainWindow
import serial
import qtawesome
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
# from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider, QMessageBox
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5 import QtGui
import function_file
import numpy as np
import image

#解决打包时递归超过最大深度问题
# sys.setrecursionlimit(100000)

# from function_file import data_send_function


''' 
参考博客
https://www.cnblogs.com/ubuntu1987/archive/2004/01/13/12191633.html
https://www.pythonf.cn/read/108311
https://blog.csdn.net/liuxf196921/article/details/88165399
https://www.jianshu.com/p/d4c0169a28db
https://blog.csdn.net/qq_44880255/article/details/106957320?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v28-3-106957320.nonecase&utm_term=pyqt%20qslider%E5%88%BB%E5%BA%A6%E6%A0%B7%E5%BC%8F&spm=1000.2123.3001.4430
https://blog.csdn.net/fhqlongteng/article/details/78535393
https://zhuanlan.zhihu.com/p/100798858
https://blog.csdn.net/weixin_40796925/article/details/107733966
https://blog.csdn.net/qq_41590417/article/details/80477990
https://blog.csdn.net/weixin_40796925/article/details/107730799  建立 PlotWidget 控件
https://blog.csdn.net/qq_40529853/article/details/100576791 体积问题
'''


class Pyqt5Serial(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Pyqt5Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("转台上位机V3.0")
        self.ser = serial.Serial()
        # self.port_check()
        # spin_icon = qtawesome.icon('fa.star', color='darkolivegreen')
        # spin_icon = QtGui.QIcon(':/pic.png')
        spin_icon = qtawesome.icon('fa.star', color='darkolivegreen')
        self.setWindowIcon(spin_icon)
        # 刷新一下串口的列表
        self.refresh()

        # Dial表盘
        self.dial.setNotchesVisible(True)  # 设置刻度
        self.dial.setPageStep(0.01)  # 翻页步长
        # self.dial.setNotchTarget(0.01)
        self.dial.setNotchTarget(5)  # 设置刻度密度，即单位刻度所代表的大小
        self.dial.setRange(-180, 180)  # 设置范围
        self.dial.setWrapping(True)  # 刻度不留缺口

        # slider垂直滑动条
        # 设置最小值
        self.verticalSlider.setMinimum(-180)
        # 设置最大值
        self.verticalSlider.setMaximum(180)
        # 设置步长
        self.verticalSlider.setSingleStep(0.01)
        # 设置当前值
        self.verticalSlider.setValue(0)
        # 设置在垂直滑块左侧绘制刻度线
        self.verticalSlider.setTickPosition(QSlider.TicksLeft)
        # 设置刻度间隔
        self.verticalSlider.setTickInterval(0.01)

        # 校验位
        lit_on = [0x07, 0x08, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        lit_off = [0x07, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        lit_lock = [0x07, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        t_on = None
        for i in range(len(lit_on)):
            if i:
                t_on ^= lit_on[i]
            else:
                t_on = lit_on[i] ^ 0

        t_off = None
        for i in range(len(lit_off)):
            if i:
                t_off ^= lit_off[i]
            else:
                t_off = lit_off[i] ^ 0

        t_lock = None
        for i in range(len(lit_lock)):
            if i:
                t_lock ^= lit_lock[i]
            else:
                t_lock = lit_lock[i] ^ 0

        self.active_button = ''
        self.POWER_ON = '55 AA 07 08 80 00 00 00 00 00 00 00 ' + hex(t_on)[2:].zfill(2) + ' F0'
        self.POWER_OFF = '55 AA 07 08 00 00 00 00 00 00 00 00 ' + hex(t_off)[2:].zfill(2) + ' F0'
        self.LOCK = '55 AA 07 08 10 00 00 00 00 00 00 00 ' + hex(t_lock)[2:].zfill(2) + ' F0'
        self.READ_DATA = '55 AA 07 08 00 FF 00 00 00 00 00 00 00 F0'
        # self.SERVO_OFF = '55 AA 07 08 01 01 00 00 00 00 00 00 00 00 F0'  伺服关闭


        # 绘图
        # self.plotWidget_ted = PlotWidget(self)
        # self.plotWidget_ted.plot([1, 2, 3, 4, 5], pen='r', symbol='o')
        # self.widget.addAction(self.plotWidget_ted)
        # 生成 300 个正态分布的随机数
        # self.data1 = np.random.normal(size=10)


    def init(self):

        # 打开串口按钮
        self.btn_open.clicked.connect(self.port_open)
        # 关闭串口按钮
        self.btn_close.clicked.connect(self.port_close)
        # 发送数据按钮
        # self.btn_send.clicked.connect(self.data_send)

        # self.radioButton1.setChecked(True)
        self.radioButton1.toggled.connect(self.button_active)
        self.radioButton2.toggled.connect(self.button_active)
        self.radioButton_w.toggled.connect(self.button_active)
        self.pushButton_on.clicked.connect(self.button_active_else)
        self.pushButton_off.clicked.connect(self.button_active_else)
        self.pushButton_lock.clicked.connect(self.button_active_else)
        # self.radioButton6.toggled.connect(self.button_active_else)
        self.btn_open.clicked.connect(self.data_receive)
        self.verticalSlider.valueChanged.connect(self.valueChange_slider)
        self.dial.valueChanged.connect(self.valueChange_dial)
        # 刷新串口外设按钮
        self.pushButton_flash.clicked.connect(self.refresh)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        # self.groupBox_2.plot([1, 2, 3, 4, 5], pen='r', symbol='o')

        # self.timer_send = QTimer()
        self.data1 = np.zeros(200)
        # print(self.data1)
        # self.data2 = np.random.normal(size=10)
        self.data2 = np.zeros(200)
        self.data3 = np.zeros(200)
        self.data4 = np.zeros(200)
        self.data5 = np.zeros(200)
        self.data6 = np.zeros(200)
        self.data7 = np.zeros(200)
        self.data8 = np.zeros(200)
        self.data9 = np.zeros(200)
        self.data10 = np.zeros(200)

        self.curve1 = self.plotWidget_ted_1.plot(self.data1, pen="r", name="mode1")
        self.curve2 = self.plotWidget_ted_2.plot(self.data2, pen="r", name="mode2")
        self.curve3 = self.plotWidget_ted_3.plot(self.data3, pen="r", name="mode3")
        self.curve4 = self.plotWidget_ted_4.plot(self.data4, pen="r", name="mode4")
        self.curve5 = self.plotWidget1.plot(self.data5, pen="w", name="mode5")
        self.curve6 = self.plotWidget1.plot(self.data6, pen="g", name="mode6")
        self.curve7 = self.plotWidget1.plot(self.data7, pen="r", name="mode7")
        self.curve8 = self.plotWidget2.plot(self.data8, pen="w", name="mode8")
        self.curve9 = self.plotWidget2.plot(self.data9, pen="g", name="mode9")
        self.curve10 = self.plotWidget2.plot(self.data10, pen="r", name="mode10")

        self.ptr1 = 0
        self.ptr2 = 0
        self.ptr3 = 0
        self.ptr4 = 0
        self.ptr5 = 0
        self.ptr6 = 0
        self.ptr7 = 0
        self.ptr8 = 0
        self.ptr9 = 0
        self.ptr10 = 0

        # # 设定定时器
        # self.timer = pq.QtCore.QTimer()
        # # 定时器信号绑定 update_data 函数
        # self.timer.timeout.connect(self.update_data)

    # # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
    # self.timer.start(50)

    # 数据左移
    # def update_data(self):
    #     data_received = self.data_receive()
    #     print('cccccccccccccccccccccccc')
    #     print(data_received)
    #     # while data_received != [0,0,0,0]:
    #     # 线1
    #     self.data1[:-1] = self.data1[1:]
    #
        # self.data1[-1] = np.random.normal()
        # self.data1[-1] = data_received[0]
        # print('bbbbbbbbbbbbbbbbbbbbbbbbbbb')
        # print(self.data1)
        # # 数据填充到绘制曲线中
        # self.curve1.setData(self.data1)
        # # x 轴记录点
        # self.ptr1 += 1
        # # 重新设定 x 相关的坐标原点
        # self.curve1.setPos(self.ptr1, 0)
        #
        # # 线2
        # self.data2[:-1] = self.data2[1:]
        # # self.data2[-1] = np.random.normal()
        # self.data2[-1] = data_received[1]
        # # 数据填充到绘制曲线中
        # self.curve2.setData(self.data2)
        # # x 轴记录点
        # self.ptr2 += 1
        # # 重新设定 x 相关的坐标原点
        # self.curve2.setPos(self.ptr2, 0)
        #
        # # 线3
        # self.data3[:-1] = self.data3[1:]
        # # self.data1[-1] = np.random.normal()
        # self.data3[-1] = data_received[2]
        # # 数据填充到绘制曲线中
        # self.curve3.setData(self.data3)
        # # x 轴记录点
        # self.ptr3 += 1
        # # 重新设定 x 相关的坐标原点
        # self.curve3.setPos(self.ptr3, 0)
        #
        # # 线4
        # self.data4[:-1] = self.data4[1:]
        # # self.data1[-1] = np.random.normal()
        # self.data4[-1] = data_received[3]
        # # 数据填充到绘制曲线中
        # self.curve4.setData(self.data4)
        # # x 轴记录点
        # self.ptr4 += 1
        # # 重新设定 x 相关的坐标原点
        # self.curve4.setPos(self.ptr4, 0)



    # 刷新一下串口
    def refresh(self):
        # 查询可用的串口
        plist = list(serial.tools.list_ports.comports())

        if len(plist) <= 0:
            print("No used com!")
            # self.statusBar.showMessage('没有可用的串口')

        else:
            # 把所有的可用的串口输出到comboBox中去
            self.cmb_port_name.clear()

            for i in range(0, len(plist)):
                plist_0 = list(plist[i])
                self.cmb_port_name.addItem(str(plist_0[0]))

    # 打开串口
    def port_open(self):
        self.ser.port = self.cmb_port_name.currentText()
        self.ser.baudrate = 460800
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(20)

        if self.ser.isOpen():
            self.btn_open.setEnabled(False)
            self.btn_close.setEnabled(True)

    # 关闭串口
    def port_close(self):
        try:
            self.ser.close()
        except:
            pass
        self.btn_open.setEnabled(True)
        self.btn_close.setEnabled(False)

    # 显示滑动条数据
    def valueChange_slider(self):
        value = self.verticalSlider.value()
        self.data_edit2.setText(str(value))

    # 显示圆盘数据
    def valueChange_dial(self):
        # self.dial.setRange(-100, 100)  # 设置范围
        # self.dial.setWrapping(False)  # 刻度不留缺口
        value = self.dial.value()
        self.data_edit1.setText(str(value))

    # def init_data_edit(self):
    #     self.data_edit1.setText('0.00')
    #     self.data_edit2.setText('0.00')

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            if self.active_button == '速度运行模式':

                input_speed_initial1 = round(float(self.data_edit1.text()) * 100)
                input_speed_initial2 = round(float(self.data_edit2.text()) * 100)

                hex_command1, input_speed_form = function_file.data_send_function(input_speed_initial1, input_speed_initial2,
                                                                    '03')
                self.ser.write(hex_command1)
                self.show_send.append(input_speed_form)

            elif self.active_button == '位置运行模式':
                input_speed_initial1 = round(float(self.data_edit1.text()) * 65536 / 360)
                input_speed_initial2 = round(float(self.data_edit2.text()) * 65536 / 360)
                hex_command1, input_speed_form = function_file.data_send_function(input_speed_initial1, input_speed_initial2,
                                                                    '0C')
                self.ser.write(hex_command1)
                self.show_send.append(input_speed_form)

            elif self.active_button == '稳定运行模式':
                input_speed_initial1 = round(float(self.data_edit1.text()) * 100)
                input_speed_initial2 = round(float(self.data_edit2.text()) * 100)
                hex_command1, input_speed_form = function_file.data_send_function(input_speed_initial1, input_speed_initial2,
                                                                    '60')
                self.ser.write(hex_command1)
                self.show_send.append(input_speed_form)

    #接收数据
    def data_receive(self):
        # data1 = []
        # nn = []
        data_s = [0,0,0,0]
        try:
            count = self.ser.inWaiting()
        except:
            self.port_close()
            return data_s
        if count != 0:
            dealStr = ''
            # 读串口数据
            recv = self.ser.read(count)
            print(recv[:1])
            # 在这里将接收到数据进行区分：hex 或 字符串
            # hex 格式：\xYY\xYY\xYY，如果接收到的字符是这种格式，则说明是hex字符，我们需要将
            # \x去除掉，取出YY，然后组成字符串返回
            # 如果接收到的是字符串，则使用decode进行解码
            print("接收到的数据 %s \n类型为: %s\n" % (recv, type(recv)))
            # print(dealStr[12:16])
            # print(type(dealStr[12:16]))

            try:
                dealStr = recv.decode()
            except (TypeError, UnicodeDecodeError):
                for i in range(len(recv)):
                    # print(recv[i])
                    dealStr += hex(recv[i])[2:].zfill(2)
                    # print(dealStr)
                    dealStr += ' '
            print("处理后的数据 %s \n类型为: %s\n" % (dealStr, type(dealStr)))
            print(dealStr[3:5])
            print(dealStr[6:8])
            print(dealStr[9:11])
            print(dealStr[12:14])
            # print(len(dealStr))
            # print(type(len(dealStr)))
            # print(dealStr[:5])
            # print(dealStr[len(dealStr)-3:])
            # dd = dealStr[len(dealStr)-3:len(dealStr)-1]
            # print('12345678900')
            # print(dd)
            # print(type(dd))
            print('1333333333333333333333')
            print(dealStr[59:61])
            # 校验位
            lit1 = [
                   eval('0x' + dealStr[6:8]),
                   eval('0x' + dealStr[9:11]),
                   eval('0x' + dealStr[12:14]),
                   eval('0x' + dealStr[15:17]),
                   eval('0x' + dealStr[18:20]),
                   eval('0x' + dealStr[21:23]),
                   eval('0x' + dealStr[24:26]),
                   eval('0x' + dealStr[27:29]),
                   eval('0x' + dealStr[30:32]),
                   eval('0x' + dealStr[33:35]),
                   eval('0x' + dealStr[36:38]),
                   eval('0x' + dealStr[39:41]),
                   eval('0x' + dealStr[42:44]),
                   eval('0x' + dealStr[45:47]),
                   eval('0x' + dealStr[48:50]),
                   eval('0x' + dealStr[51:53]),
                   eval('0x' + dealStr[54:56]),
                   eval('0x' + dealStr[57:59]),
                   eval('0x' + dealStr[60:62]),
                   eval('0x' + dealStr[63:65]),
                   eval('0x' + dealStr[66:68]),
                   eval('0x' + dealStr[69:71]),
                   eval('0x' + dealStr[72:74]),
                   eval('0x' + dealStr[75:77]),
                   eval('0x' + dealStr[78:80]),
                   eval('0x' + dealStr[81:83]),
                   eval('0x' + dealStr[84:86]),
                   eval('0x' + dealStr[87:89]),
                   eval('0x' + dealStr[90:92]),
                   eval('0x' + dealStr[93:95])]

            t_12 = None
            for i in range(len(lit1)):
                if i:
                    t_12 ^= lit1[i]
                else:
                    t_12 = lit1[i] ^ 0
            print('17777777777777777777777777777777777777')
            print(dealStr[len(dealStr) - 39:len(dealStr) - 37])
            print(dealStr[len(dealStr) - 42:len(dealStr) - 40])
            print(len(dealStr))
            # print(dealStr[len(dealStr)-6:len(dealStr)-4])
            print(hex(t_12))

            # if dealStr[:5] == '55 aa' and dealStr[len(dealStr)-3:len(dealStr)-1] == 'f0' and len(dealStr) == 66 and hex(t_12)[2:].zfill(2) == dealStr[len(dealStr)-6:len(dealStr)-4]:
            if dealStr[:5] == '55 aa' and dealStr[len(dealStr)-3:len(dealStr)-1] == 'f0' and len(dealStr) == 102 and hex(t_12)[2:].zfill(2) == dealStr[len(dealStr)-6:len(dealStr)-4]:
                dealStr_new = dealStr.replace(' ', '')  #去除首尾空格
                print(dealStr_new)
                print(type(dealStr_new))
                recv1 = str(dealStr_new[8:10])  # 当前运行模式
                print(recv1)
                if recv1 == '03':
                    self.lineEdit_1.setText('速度运行模式')
                elif recv1 == '0c':
                    self.lineEdit_1.setText('位置运行模式')
                elif recv1 == '10':
                    self.lineEdit_1.setText('锁定')
                elif recv1 == '60':
                    self.lineEdit_1.setText('稳定运行模式')
                elif recv1 == '80':
                    self.lineEdit_1.setText('功放上电')
                elif recv1 == '00':
                    self.lineEdit_1.setText('功放断电')
                else:
                    pass
                recv2 = str(dealStr_new[10:12])  # 转台到位状态
                print(recv2)
                if recv2 == '01':
                    self.lineEdit_2.setText('俯仰到位, 方位未到位')
                elif recv2 == '10':
                    self.lineEdit_2.setText('俯仰未到位, 方位到位')
                elif recv2 == '11':
                    self.lineEdit_2.setText('俯仰、方位均到位')
                elif recv2 == '00':
                    self.lineEdit_2.setText('俯仰、方位均未到位')
                    print('11111111111111111111111')
                else:
                    pass


                recv3 = '0x' + str(dealStr_new[12:20])   #方位角速度
                recv3_er_new = function_file.data_receive_process(recv3, 32, 14800)
                r_3 = '%.04f' % (round(recv3_er_new, 4))
                self.lineEdit_3.setText(str(r_3))

                recv4 = '0x' + str(dealStr_new[20:28])   #俯仰角速度
                recv4_er_new = function_file.data_receive_process(recv4, 32, 14800)
                r_4 = '%.04f'%(round(recv4_er_new, 4))
                self.lineEdit_4.setText(str(r_4))

                recv5 = '0x' + str(dealStr_new[28:34])   #方位角度
                recv5_er_new = function_file.data_receive_process(recv5, 24, 1000)
                r_5 = '%.04f'%(round(recv5_er_new, 4))
                self.lineEdit_5.setText(str(r_5))

                recv6 = '0x' + str(dealStr_new[34:40])  # 俯仰角度
                recv6_er_new = function_file.data_receive_process(recv6, 24, 1000)
                r_6 = '%.04f'%(round(recv6_er_new, 4))
                self.lineEdit_6.setText(str(r_6))
###########################################################
                recv7 = '0x' + str(dealStr_new[40:44])  # 俯仰角度
                recv7_er_new = function_file.data_receive_process(recv7, 16, 1241)
                r_7 = '%.04f' % (round(recv7_er_new, 4))

                recv8 = '0x' + str(dealStr_new[44:48])  # 俯仰角度
                recv8_er_new = function_file.data_receive_process(recv8, 16, 1241)
                r_8 = '%.04f' % (round(recv8_er_new, 4))

                recv9 = '0x' + str(dealStr_new[48:52])  # 俯仰角度
                recv9_er_new = function_file.data_receive_process(recv9, 16, 1241)
                r_9 = '%.04f' % (round(recv9_er_new, 4))
##############################################################
                recv10 = '0x' + str(dealStr_new[52:56])  # 俯仰角度
                recv10_er_new = function_file.data_receive_process(recv10, 16, 1241)
                r_10 = '%.04f' % (round(recv10_er_new, 4))

                recv11 = '0x' + str(dealStr_new[56:60])  # 俯仰角度
                recv11_er_new = function_file.data_receive_process(recv11, 16, 1241)
                r_11 = '%.04f' % (round(recv11_er_new, 4))

                recv12 = '0x' + str(dealStr_new[60:64])  # 俯仰角度
                recv12_er_new = function_file.data_receive_process(recv12, 16, 1241)
                r_12 = '%.04f' % (round(recv12_er_new, 4))
                # self.lineEdit_6.setText(str(r_6))
                # data_s[0] = r_3
                # data_s[1] = r_4
                # data_s[2] = r_5
                # data_s[3] = r_6
                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                # print(data_s)
                ##  data1
                self.data1[:-1] = self.data1[1:]
                self.data1[-1] = r_3

                # 数据填充到绘制曲线中
                self.curve1.setData(self.data1)
                # x 轴记录点
                self.ptr1 += 1
                # 重新设定 x 相关的坐标原点

                self.curve1.setPos(self.ptr1, 0)
                # return data_s

                # 线2
                self.data2[:-1] = self.data2[1:]
                # self.data2[-1] = np.random.normal()
                self.data2[-1] = r_4
                # 数据填充到绘制曲线中
                self.curve2.setData(self.data2)
                # x 轴记录点
                self.ptr2 += 1
                # 重新设定 x 相关的坐标原点
                self.curve2.setPos(self.ptr2, 0)

                # 线3
                self.data3[:-1] = self.data3[1:]
                # self.data1[-1] = np.random.normal()
                self.data3[-1] = r_5
                # 数据填充到绘制曲线中
                self.curve3.setData(self.data3)
                # x 轴记录点
                self.ptr3 += 1
                # 重新设定 x 相关的坐标原点
                self.curve3.setPos(self.ptr3, 0)

                # 线4
                self.data4[:-1] = self.data4[1:]
                # self.data1[-1] = np.random.normal()
                self.data4[-1] = r_6
                # 数据填充到绘制曲线中
                self.curve4.setData(self.data4)
                # x 轴记录点
                self.ptr4 += 1
                # 重新设定 x 相关的坐标原点
                self.curve4.setPos(self.ptr4, 0)

                # self.plotWidget1.plot(self.data1, name="mode2")
                # self.plotWidget1.setPos(self.ptr4, 0)
                # self.graphicsView_1.plot(self.data3, name="mode3")

                # self.curve5.setData(self.data1)
                # self.curve5.setPos(self.ptr4, 0)
                # self.curve5.setData(self.data3)
                self.data5[:-1] = self.data5[1:]
                self.data5[-1] = r_7
                self.data6[:-1] = self.data6[1:]
                self.data6[-1] = r_8
                self.data7[:-1] = self.data7[1:]
                self.data7[-1] = r_9
                self.curve5.setData(self.data5)
                self.curve6.setData(self.data6)
                self.curve7.setData(self.data7)
                self.ptr5 += 1
                self.curve5.setPos(self.ptr5, 0)
                self.ptr6 += 1
                self.curve6.setPos(self.ptr6, 0)
                self.ptr7 += 1
                self.curve7.setPos(self.ptr7, 0)
                # self.curve5.setData(self.data6)
                # self.curve5.setData(self.data3, name="mode7")

                self.data8[:-1] = self.data8[1:]
                self.data8[-1] = r_10
                self.data9[:-1] = self.data9[1:]
                self.data9[-1] = r_11
                self.data10[:-1] = self.data10[1:]
                self.data10[-1] = r_12
                self.curve8.setData(self.data8)
                self.curve9.setData(self.data9)
                self.curve10.setData(self.data10)
                self.ptr8 += 1
                self.curve8.setPos(self.ptr8, 0)
                self.ptr9 += 1
                self.curve9.setPos(self.ptr9, 0)
                self.ptr10 += 1
                self.curve10.setPos(self.ptr10, 0)
                # self.data6[:-1] = self.data6[1:]
                # # self.data1[-1] = np.random.normal()
                # self.data6[-1] = r_8
                # self.curve5.setData(self.data6)
                # # self.curve5.setData(self.data3, name="mode7")



            else:
                pass
        else:
            pass


                # nn.append('%.04f' % (round(recv3_er_new, 4)))
                # nn.append('%.04f' % (round(recv4_er_new, 4)))
                # nn.append('%.04f' % (round(recv5_er_new, 4)))
                # nn.append('%.04f' % (round(recv6_er_new, 4)))
                # data1 = np.array(nn)
                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                # print(data1)
                # print(type(data1))

                # self.c = self.plotWidget_ted_1.plot(data1, name="mode2")
                # # self.ptr1 = 0
                # self.timer.timeout.connect(self.update_data)
                # # # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
                # self.timer.start(50)

    # ''' 功放、锁定、伺服选定时直接发送的数据 '''
    # def str_data_send(self):
    #     if self.active_button == '功放上电':
    #         hex_command = bytes.fromhex(self.POWER_ON)
    #         self.ser.write(hex_command)
    #         self.show_send.append(self.POWER_ON)
    #     elif self.active_button == '功放断电':
    #         hex_command = bytes.fromhex(self.POWER_OFF)
    #         self.ser.write(hex_command)
    #         self.show_send.append(self.POWER_OFF)
    #     elif self.active_button == '锁定':
    #         hex_command = bytes.fromhex(self.LOCK)
    #         self.ser.write(hex_command)
    #         self.show_send.append(self.LOCK)
        # elif self.active_button == '取数指令':
        #     hex_command = bytes.fromhex(self.READ_DATA)
        #     self.ser.write(hex_command)
        #     self.show_send.append(self.READ_DATA)

    # 位置模式和速度模式按钮动作
    def button_active(self):
        radiobutton = self.sender()
        if radiobutton.text() == '速度运行模式' or radiobutton.text() == '稳定运行模式' or radiobutton.text() == '位置运行模式':
            self.active_button = radiobutton.text()
            self.data_edit1.setText('0.00')
            self.data_edit2.setText('0.00')
            self.data_edit1.setEnabled(True)
            self.data_edit2.setEnabled(True)
            if radiobutton.isChecked() == True:
                print('<' + radiobutton.text() + '>被选中')
                # 发送数据按钮
                print('<' + radiobutton.text() + '>下的数据:')
                self.btn_send.disconnect()
                self.btn_send.clicked.connect(self.data_send)
            else:
                pass
            if radiobutton.text() == '速度运行模式' or radiobutton.text() == '稳定运行模式':
                # Dial表盘
                self.dial.setNotchesVisible(True)  # 设置刻度
                self.dial.setPageStep(0.01)  # 翻页步长
                # self.dial.setNotchTarget(0.01)
                # 设置当前值
                self.dial.setValue(0)
                self.dial.setNotchTarget(5)  # 设置刻度密度，即单位刻度所代表的大小
                self.dial.setRange(-100, 100)  # 设置范围
                self.dial.setWrapping(False)  # 刻度不留缺口

                # slider垂直滑动条
                # 设置最小值
                self.verticalSlider.setMinimum(-100)
                # 设置最大值
                self.verticalSlider.setMaximum(100)
                # 设置步长
                self.verticalSlider.setSingleStep(0.01)
                # 设置当前值
                self.verticalSlider.setValue(0)
                # 设置在垂直滑块左侧绘制刻度线
                self.verticalSlider.setTickPosition(QSlider.TicksLeft)
                # 设置刻度间隔
                self.verticalSlider.setTickInterval(0.01)

            elif radiobutton.text() == '位置运行模式':
                # Dial表盘
                self.dial.setNotchesVisible(True)  # 设置刻度
                self.dial.setPageStep(0.01)  # 翻页步长
                # self.dial.setNotchTarget(0.01)
                # 设置当前值
                self.dial.setValue(0)
                self.dial.setNotchTarget(5)  # 设置刻度密度，即单位刻度所代表的大小
                self.dial.setRange(0, 360)  # 设置范围
                self.dial.setWrapping(True)  # 刻度不留缺口

                # slider垂直滑动条
                # 设置最小值
                self.verticalSlider.setMinimum(-10)
                # 设置最大值
                self.verticalSlider.setMaximum(90)
                # 设置步长
                self.verticalSlider.setSingleStep(0.01)
                # 设置当前值
                self.verticalSlider.setValue(0)
                # 设置在垂直滑块左侧绘制刻度线
                self.verticalSlider.setTickPosition(QSlider.TicksLeft)
                # 设置刻度间隔
                self.verticalSlider.setTickInterval(0.01)

    # 功放、伺服关闭、断电按钮动作
    def button_active_else(self):
        button_txt = self.sender()
        # if button_txt.text() == '功放上电' or button_txt.text() == '功放断电' or button_txt.text() == '锁定':
        #     self.active_button = button_txt.text()
        #     self.data_edit1.setEnabled(False)
        #     self.data_edit2.setEnabled(False)
        if button_txt.text() == '功放上电':
            self.data_edit1.clear()
            self.data_edit2.clear()
            self.data_edit1.setEnabled(False)
            self.data_edit2.setEnabled(False)
            print('<' + button_txt.text() + '>被选中')
            # 发送数据按钮
            print('<' + button_txt.text() + '>下的数据:')
            # self.btn_send.disconnect()
            hex_command = bytes.fromhex(self.POWER_ON)
            self.ser.write(hex_command)
            self.show_send.append(self.POWER_ON)
            # self.pushButton_on.clicked.connect(self.str_data_send)
        elif button_txt.text() == '功放断电':
            self.data_edit1.clear()
            self.data_edit2.clear()
            self.data_edit1.setEnabled(False)
            self.data_edit2.setEnabled(False)
            print('<' + button_txt.text() + '>被选中')
            # 发送数据按钮
            print('<' + button_txt.text() + '>下的数据:')
            # self.btn_send.disconnect()
            hex_command = bytes.fromhex(self.POWER_OFF)
            self.ser.write(hex_command)
            self.show_send.append(self.POWER_OFF)
            # self.pushButton_off.clicked.connect(self.str_data_send)
        elif button_txt.text() == '锁定':
            self.data_edit1.clear()
            self.data_edit2.clear()
            self.data_edit1.setEnabled(False)
            self.data_edit2.setEnabled(False)
            print('<' + button_txt.text() + '>被选中')
            # 发送数据按钮
            print('<' + button_txt.text() + '>下的数据:')
            # self.btn_send.disconnect()
            hex_command = bytes.fromhex(self.LOCK)
            self.ser.write(hex_command)
            self.show_send.append(self.LOCK)
            # self.pushButton_lock.clicked.connect(self.str_data_send)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = Pyqt5Serial()
    myshow.showMaximized()  #窗口最大化显示
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = QMainWindow()
#     ui = Pro.Ui_MainWindow()
#     ui.setupUi(mainWindow)
#     mainWindow.show()
#     sys.exit(app.exec_())


# def button_state(self):
#     radiobutton = self.sender()
#     if  radiobutton.text() =='速度运行模式':
#         if radiobutton.isChecked() == True:
#             print('<' + radiobutton.text() + '>被选中')
#             # 发送数据按钮
#             print('等待发送速度运行模式下的数据:' )
#             self.btn_send.clicked.connect(self.data_send)
#         else:
#             print('<' + radiobutton.text() + '>取消选中')
#     if radiobutton.text() == '位置运行模式':
#         if radiobutton.isChecked() == True:
#             print('<' + radiobutton.text() + '>被选中')
#             print('等待发送位置运行模式下的数据:')
#             self.btn_send.clicked.connect(self.data_send)
#         else:
#             print('<' + radiobutton.text() + '>取消选中')


# print(-int(recv3_er[1:],2))
# recv3_er_new = reverse(recv3_er[1:])
# recv3_er_add = add_1(recv3_er_new)
#
# self.lineEdit_3.setText(str(round(-int(recv3_er_add[1:],2)/14800, 2)))
# bin(int('0x11', 16)) 十六进制数转二进制数 输出字符串类型
# print(-int(recv3_er_add[1:],2))
# print('1111111111111111111111')
