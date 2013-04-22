#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import date, datetime, time, timedelta


def parse_nav(sentence):
    """
    解析电文，返回帧号及内容
    $GNECT,024,L1,09,I,
    8B10B4C95AF0B80000A62B262B37FFFFF927CC4C9FAC7246A0EED58FBA91FFA4EB150019AC8*42
    """
    if not sentence:
        return None, None, None
    try:
        array = sentence.split(',')
        sat_num = array[1]
        page = array[5][:array[5].find("*")]
        bin_page = bin(int(page, 16))[2:]
        frame_num = int(bin_page[49:52], 2)
        return sat_num, frame_num, bin_page
    except:
        return None, None, None

def parse_frame(frame_number, page):
    result = {}
    if frame_number == 1:
        z_count = int(page[30:47], 2)
        week_num = int(page[60:70], 2) + 1024
        time = calc_time(z_count, week_num)
        idoc = int(page[82:84], 2) * 256 + int(page[210:218], 2)
        result["WN"] = week_num
        result["HOW"] = z_count * 6 - 4
        result["time"] = time
        result["ura"] = int(page[72:76], 2)
        result["sv_health"] = int(page[76:82], 2)
        result["iodc"] = idoc
        result["tow"] = z_count
        result["tgd"] = float(b2sd(page[196:204])*pow(2, -31))
        result["toc"] = int(page[218:234], 2) * pow(2, 4)
        result["af0"] = float(b2sd(page[270:292])*pow(2, -31))
        result["af1"] = float(b2sd(page[248:264])*pow(2, -43))
        result["af2"] = float(b2sd(page[240:248])*pow(2, -55))
        result["toe"] = z_count * 6
    elif frame_number == 2:
        result["iode"] = int(page[60:68], 2)
        result["crs"] = float(b2sd(page[68:84])*pow(2, -5))
        result["deltan"] = float(b2sd(page[90:106])*pow(2, -43))
        result["eEcc"] = float((int(page[166:174], 2)*pow(2, 24)
                               +int(page[180:204], 2))*pow(2, -33))
        result["M0"] = float((b2sd(page[106:114])*pow(2, 24)
                             +int(page[121:144], 2))*pow(2, -31))
        result["cuc"] = float(b2sd(page[150:166])*pow(2, -29))
        result["cus"] = float(b2sd(page[210:226])*pow(2, -29))
        result["sqrta"] = float((int(page[226:234], 2)*pow(2, 24)
                                +int(page[240:264], 2))*pow(2, -19))
        # result["toe"] = int(page[270:287], 2) * pow(2, 4)
    elif frame_number == 3:
        result["cic"] = float(b2sd(page[60:76])*pow(2, -29))
        result["OMEGA0"] = float((b2sd(page[76:84])*pow(2, 24)
                                +int(page[90:114], 2))*pow(2, -31))
        result["cis"] = float(b2sd(page[120:136])*pow(2, -29))
        result["i0"] = float((b2sd(page[136:144])*pow(2, 24)
                            +int(page[151:174], 2))*pow(2, -31))
        result["crc"] = float(b2sd(page[180:196])*pow(2, -5))
        result["omega"] = float((b2sd(page[196:204])*pow(2, 24)
                                +int(page[210:234], 2))*pow(2, -31))
        result["omegadot"] = float(b2sd(page[240:264])*pow(2, -43))
        result["iode"] = int(page[270:278], 2)
        result["idot"] = float(b2sd(page[278:292])*pow(2, -43))
    return result

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

def calc_time(z_count, week_num):
    d = datetime(1980, 1, 6)
    delta = timedelta(seconds=6*z_count, weeks=week_num)
    return d + delta

def b2sd(binary):
    """
    binary_to_signed_decimal
    """
    t = 0
    for i in range(len(binary)):
        if i == 0 and binary[i] == "1":
            flag = -1
        else:
            flag = int(binary[i])
        t = t + flag * pow(2, len(binary) - i - 1)
    return t