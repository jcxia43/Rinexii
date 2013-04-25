#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parse_nav import *
from gen_rinex import *


def generate_navigation_file(filename):
    # read raw data file
    f = open(filename, 'r+')
    # fn is navigation file name
    fn = print_nav_header()
    # fn2 is observation file name
    fn2 = print_obs_header()
    # file object of the two files
    t = open(fn, 'a')
    t2 = open(fn2, 'a')
    # result dictionary
    # eg: result{"sat":{sat infos},...}
    result = {}
    # store CPSV senteces
    cpsv = []
    time = None
    last_time = None
    while True:
        s = f.readline()
        if s.startswith("$G"):
            # a new GPECT sentence, so clear the cpsv buffer
            cpsv = []
            sat, frame_number, page = parse_nav(s)
            # locate the fisrt subframe
            if sat not in result and frame_number == 1:
                result[sat] = {}
                result[sat]["index"] = []
            if sat in result and len(page) == 300:
                r = parse_frame(frame_number, page)
                result[sat] = dict(result[sat].items() + r.items())
                # parse the subframes one by one
                # and make sure the index is [1,2,3]
                result[sat]["index"].append(frame_number)
                # last subframe, append the frame to the file
                if [1, 2, 3] == result[sat]["index"]:
                    print_nav_data(sat, t, result[sat])
                    time = result[sat]["time"]
                    result.pop(sat)
                # just in case data is disorder
                if frame_number == 5:
                    result.pop(sat)
        # a cpsv sentence
        elif s.startswith("$C"):
            cpsv.append(s)
            # make sure 6 sentences in buffer
            # and also get the time from the navigation message
            if len(cpsv) == 6 and time is not None and time != last_time:
                last_time = time
                count = 0
                for sentence in cpsv:
                    # parse the sentence
                    data_list = parse_CPSV(sentence)
                    epoch = [[time.year, time.month, time.day, time.hour,
                             time.minute, time.second+count], "0", "0", "0"]
                    data = []
                    for item in data_list:
                        # make sure every item is a legal number #.##
                        # in case the raw data is disorder
                        if is_number(item[0]) and is_number(item[1]) and is_number(item[2]) and is_number(item[3]):
                            data.append(["G"+item[0], [str(float(item[1])*1000), " ", " "], [str(float(item[2])
                                         + float(item[3])), " ", " "]])
                    # increase the count in the epoch
                    count = count + 1
                    epoch[2] = str(len(data))
                    print_obs_data(epoch, data, t2)
                cpsv = []
        # EOF
        elif s == "":
            return None


# ugly way to determine a traditional number #.##
def is_number(s):
    s = s.replace("-", "0")
    l = s.split(".")
    if len(l) == 1 and l[0].isdigit():
        return True
    if len(l) == 2 and l[0].isdigit() and l[1].isdigit():
        return True
    return False

generate_navigation_file("raw_data_1.txt")
