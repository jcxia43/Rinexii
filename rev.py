#!/usr/bin/python
# -*- coding: utf-8 -*-

# filename: rev.py
# author: onlyme
# date: 2013.03.12
# description: 一机多天线PC段串口接收程序

import serial
import sys


# 打开GPS CPSV数据流
CMD_OPENGP_STREAM = "$BDRMO,,4,1*FF\r\n"
# 关闭GPS CPSV数据流
CMD_CLOSEGP_STREAM = "$BDRMO,RAM,3,1*FF\r\n"

BAUDRATE = 115200jjjjXSXC

TIMEOUT = 10


def parse_CPSV(sentence):
    """
    解析CPSV数据语句，读入sentence，將sentence解析为一个tuple list，
    其中tuple格式为（卫星号，码相位，载波相位整数部分，小数部分）
    Eg: sentence = "$CPSV,9,100,200,0.01,25,55,201,0.44,3c\r\n"
    返回 [(9,100,200,0.01), (25,55,201,0.44)]
    """
    array = sentence.split(',')

    sat = array[1:-1:4]
    code_phase = array[2:-1:4]
    phase_int = array[3:-1:4]
    phase_float = array[4:-1:4] # NOT NEAT!
    # 最后一个载波相位小数部分和校验和以'*'分隔
    phase_float.append(array[-1].split('*')[0])

    return zip(sat, code_phase, phase_int, phase_float)

def main():
    """
    接收程序主体
    """
    try:
        port = serial.Serial(sys.argv[1], BAUDRATE, timeout = TIMEOUT)

        # 串口打开
        if port.isOpen():
            data = open('DATA','w')
            # 打开数据流
            port.write(CMD_OPENGP_STREAM)
            i = 0
            while True:
                try:
                    i = i + 1
                    print "retrieving record No.", i
                    item = port.readline()
                    # collection内包含所有信息
                    # 其中tuple格式为（卫星号，码相位，载波相位整数部分，小数部分）
#                    collection = parse_CPSV(item) 
                    data.write(item)
                    print item
                except KeyboardInterrupt:
                    port.write(CMD_CLOSEGP_STREAM)
                    port.close()
                    data.close()
                    print "done!"
    except ValueError:
        # 无效端口
        print "Invalid port!"

main()
