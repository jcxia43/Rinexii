#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parse_nav import *
from gen_rinex import *



def generate_navigation_file(filename):
    f = open(filename, 'r+')
    fn = print_nav_header()
    fn2 = print_obs_header()
    t = open(fn, 'a')
    t2 = open(fn2, 'a')
    result = {}
    cpsv = []
    i = 0
    time = None
    while True:
        s = f.readline()
        if s.startswith("$G"):
            cpsv = []
            sat, frame_number, page = parse_nav(s)
            if sat not in result and frame_number == 1:
                result[sat] = {}
                result[sat]["index"] = []
            if sat in result and len(page) == 300:
                r = parse_frame(frame_number, page)
                result[sat] = dict(result[sat].items() + r.items())
                result[sat]["index"].append(frame_number)
            # last subframe, append the frame to the file
                if [1, 2, 3] == result[sat]["index"]:
                    print_nav_data(sat, t, result[sat])
                    time = result[sat]["time"]
                    result.pop(sat)
                # IMPORTANT! cos data is SOMETIMES DISORDER! 
                if frame_number == 5:
                    result.pop(sat)
        elif s.startswith("$C"):
            cpsv.append(s)
            if len(cpsv) == 6 and time is not None:
                i = 0
                for sentence in cpsv:
                    data_list = parse_CPSV(sentence)
                    sats_number = len(data_list)
                    epoch = [[time.year, time.month, time.day, time.hour,
                            time.minute, time.second + i], "0", sats_number, "0"]
                    data = []
                    for item in data_list:
                        if is_number(item[0]) and is_number(item[1]) and is_number(item[2]) and is_number(item[3]):
                            data.append(["G" + item[0], [str(float(item[1])*1000), " ", " "], [str(float(item[2])
                                        +float(item[3])), " ", " "]])    
                    i = i + 1      
                    epoch[2] = str(len(data))            
                    print_obs_data(epoch, data, t2)
                    cpsv = []
        elif s == "":
            return None

def is_number(s):
    s = s.replace("-", "0")
    l = s.split(".")
    if len(l) == 1 and l[0].isdigit():
        return True
    if len(l) == 2 and l[0].isdigit() and l[1].isdigit():
        return True
    return False

generate_navigation_file("raw_data_1.txt")

                