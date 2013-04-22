#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

def print_obs_header(**keywords):
    """
    generate the header of the rinex file
    """
    
    # 读入各种参数
    version      = keywords.get("version", "3.01")
    sat_system   = keywords.get("sat_system", "G")
    program      = keywords.get("program", "Renixii 0.1")
    agency       = keywords.get("agency", "ECNU 3G Lab")
    marker_type  = keywords.get("marker_type", "GEODETIC")
    observer     = keywords.get("observer", "Automatic")
    
    rec_number   = keywords.get("rec_number", "1234")
    rec_type     = keywords.get("rec_type", "XXXX")
    rec_version  = keywords.get("rec_version", "0000")
    
    ant_number   = keywords.get("ant_number", "1234")
    ant_version  = keywords.get("ant_version", "0000")
    
    approx_x     = keywords.get("approx_x", "0")
    approx_y     = keywords.get("approx_y", "0")
    approx_z     = keywords.get("approx_z", "0")
    
    ant_deltah   = keywords.get("ant_deltah", "0")
    ant_deltan   = keywords.get("ant_deltan", "0")
    ant_deltae   = keywords.get("ant_deltae", "0")
    
    sys_num_obs  = keywords.get("sys_num_obs", [["G", "2", "C1C", "L1L"]])
    
    interval     = keywords.get("interval", "1")
    
    first_obs    = keywords.get("first_obs", ["2013", "4", "17", "02", "01", "06"])
    obs_time_sys = keywords.get("obs_time_sys", "GPS")
    
    sys_ph_shift = keywords.get("sys_phase_shift", [["G", "C1C", "0.25"], ["B", "L2S", "-0.25"]])
    
    # 以下五个参数用以生成文件名
    station_id   = keywords.get("station_id", "ECNU")
    file_type    = keywords.get("file_type", "O")
    day_of_year  = keywords.get("day_of_year", "000")
    nth_hour     = keywords.get("nth_hour", "a")
    starting_min = keywords.get("starting_min", "00")
    year         = keywords.get("year", "13")
    
    file_name    = gen_filename(station_id, day_of_year, nth_hour, starting_min,
                                year, file_type)

    f = open(file_name, 'w')
    
    # RINEX VERSION / TYPE
    f.write("%9.2f" % float(version)) # F9.2 version
    f.write(" " * 11)                 # 11X
    f.write(file_type.ljust(20))      # A1 file type
    f.write(sat_system.ljust(20))     # A1 satellite system
    f.write("RINEX VERSION / TYPE\n")

    # PGM / RUN BY / DATE
    f.write(program.ljust(20))     # A20 Name of program
    f.write(agency.ljust(20))      # A20 Name of agency
    f.write(time.strftime("%Y%m%d %H%M%S %Z").ljust(20)) # A20 Date and Time and zone code
    f.write("PGM / RUN BY / DATE\n")

    # MARKER NAME
    f.write(station_id.ljust(60))
    f.write("MARKER NAME\n")

    # MARKER TYPE
    f.write(marker_type.ljust(60))
    f.write("MARKER TYPE\n")
    
    # OBSERVER / AGENCY
    f.write(observer.ljust(20))
    f.write(agency.ljust(40))
    f.write("OBSERVER / AGENCY\n")

    # REC # / TYPE / VERS
    f.write(rec_number.ljust(20))
    f.write(rec_type.ljust(20))
    f.write(rec_version.ljust(20))
    f.write("REC # / TYPE / VERS\n")

    # ANT # / TYPE
    f.write(ant_number.ljust(20))
    f.write(ant_version.ljust(40))
    f.write("ANT # / TYPE\n")

    # APPROX POSITION XYZ
    f.write("%14.4f" % float(approx_x))
    f.write("%14.4f" % float(approx_y))
    f.write("%14.4f" % float(approx_z))
    f.write(" " * 18)
    f.write("APPROX POSITION XYZ\n")

    # ANTENNA: DELTA H/E/N
    f.write("%14.4f" % float(ant_deltah))
    f.write("%14.4f" % float(ant_deltan))
    f.write("%14.4f" % float(ant_deltae))
    f.write(" " * 18)
    f.write("ANTENNA: DELTA H/E/N\n")

    # SYS / # / OBS TYPES
    for item in sys_num_obs:
        f.write(item[0].ljust(3))
        f.write(item[1].rjust(3))
        # 尚未考虑超过13个descriptor的情况
        for descriptor in item[2:]:
            f.write(descriptor.rjust(4))
        f.write(" " * (54 - int(item[1]) * 4))
        f.write("SYS / # / OBS TYPES\n")
    
    # INTERVAL
    f.write("%10.3f" % float(interval))
    f.write(" " * 50)
    
    f.write("INTERVAL\n")
    
    # TIME OF FIRST OBS
    y, M, d, h, m, s = first_obs
    f.write(y.rjust(6)+M.rjust(6)+d.rjust(6)+h.rjust(6)+m.rjust(6))
    f.write("%13.7f" % float(s))
    f.write(" " * 5)
    f.write(obs_time_sys)
    f.write(" " * 9)
    f.write("TIME OF FIRST OBS\n")

    # # SYS / PHASE SHIFTS
    # for item in sys_ph_shift:
    #     f.write(item[0].ljust(2))
    #     f.write(item[1].ljust(4))
    #     f.write("%8.5f" % float(item[2]))
    #     f.write(" " * 46)
    #     f.write("SYS / PHASE SHIFTS\n")
        
    # END
    f.write(" " * 60)
    f.write("END OF HEADER\n")
    f.close()
    return file_name
    
def print_nav_header(**keywords):
    """
    输出导航文件header

    Arguments:
    - `**keywords`:参数列表
    """
    version      = keywords.get("version", "3.01")
    sat_system   = keywords.get("sat_system", "G")
    program      = keywords.get("program", "Renixii 0.1")
    agency       = keywords.get("agency", "ECNU 3G Lab")
    gpsa         = keywords.get("gpsa", [0, 0, 0, 0])
    gpsb         = keywords.get("gpsb", [0, 0, 0, 0])

    
    
    # 以下五个参数用以生成文件名
    station_id   = keywords.get("station_id", "ECNU")
    file_type    = keywords.get("file_type", "N")
    day_of_year  = keywords.get("day_of_year", "000")
    nth_hour     = keywords.get("nth_hour", "a")
    starting_min = keywords.get("starting_min", "00")
    year         = keywords.get("year", "13")


    file_name    = gen_filename(station_id, day_of_year, nth_hour, starting_min,
                                year, file_type)

    f = open(file_name, 'w')

    # RINEX VERSION / TYPE
    f.write("%9.2f" % float(version)) # F9.2 version
    f.write(" " * 11)                 # 11X
    f.write(file_type.ljust(20))      # A1 file type
    f.write(sat_system.ljust(20))     # A1 satellite system
    f.write("RINEX VERSION / TYPE".ljust(20))
    f.write("\n")

    # PGM / RUN BY / DATE
    f.write(program.ljust(20))     # A20 Name of program
    f.write(agency.ljust(20))      # A20 Name of agency
    f.write(time.strftime("%Y%m%d %H%M%S %Z").ljust(20)) # A20 Date and Time and zone code
    f.write("PGM / RUN BY / DATE".ljust(20))
    f.write("\n")

    # IONOSPHERIC CORR
    f.write("GPSA".ljust(5))
    for i in gpsa:
        f.write(sa(12, 4, i))
    f.write(" " * 7)
    f.write("IONOSPHERIC CORR".ljust(20))
    f.write("\n")

    f.write("GPSB".ljust(5))
    for i in gpsb:
        f.write(sa(12, 4, i))
    f.write(" " * 7)
    f.write("IONOSPHERIC CORR".ljust(20))
    f.write("\n")

    # LEAP SECONDS
    f.write(" " * 60)
    f.write("LEAP SECONDS".ljust(20))
    f.write("\n")

    # END
    f.write(" " * 60)
    f.write("END OF HEADER".ljust(20))
    f.write("\n")
    f.close()
    return file_name

def print_nav_data(sat, f, keywords):
    """
    打印导航文件内容
    sat is the sat number, keywords contains all
    necessory parameters
    """
    
    d = keywords.get("time")
    af0 = keywords.get("af0")
    af1 = keywords.get("af1")
    af2 = keywords.get("af2")

    f.write("G"+("%2.2d" % int(sat)))
    f.write(("%4d" % d.year).rjust(5))
    f.write(("%2.2d" % d.month).rjust(3))
    f.write(("%2.2d" % d.day).rjust(3))
    f.write(("%2.2d" % d.hour).rjust(3))
    f.write(("%2.2d" % d.minute).rjust(3))
    f.write(("%2.2d" % d.second).rjust(3))
    f.write(sa(19, 12, af0))
    f.write(sa(19, 12, af1))
    f.write(sa(19, 12, af2))
    f.write("\n")

    # orbit 1
    iode = keywords.get("iode")
    crs = keywords.get("crs")
    deltan = keywords.get("deltan")
    M0 = keywords.get("M0")

    f.write(" " * 4)
    f.write(sa(19, 12, iode))
    f.write(sa(19, 12, crs))
    f.write(sa(19, 12, deltan))
    f.write(sa(19, 12, M0))
    f.write("\n")

    # orbit 2
    cuc = keywords.get("cuc")
    eEcc = keywords.get("eEcc")
    cus = keywords.get("cus")
    sqrta = keywords.get("sqrta")

    f.write(" " * 4)
    f.write(sa(19, 12, cuc))
    f.write(sa(19, 12, eEcc))
    f.write(sa(19, 12, cus))
    f.write(sa(19, 12, sqrta))
    f.write("\n")

    # orbit 3
    toe = keywords.get("toe")
    cic = keywords.get("cic")
    OMEGA0 = keywords.get("OMEGA0")
    cis = keywords.get("cis")

    f.write(" " * 4)
    f.write(sa(19, 12, toe))
    f.write(sa(19, 12, cic))
    f.write(sa(19, 12, OMEGA0))
    f.write(sa(19, 12, cis))
    f.write("\n")

    # orbit 4
    i0 = keywords.get("i0")
    crc = keywords.get("crc")
    omega = keywords.get("omega")
    omegadot = keywords.get("omegadot")

    f.write(" " * 4)
    f.write(sa(19, 12, i0))
    f.write(sa(19, 12, crc))
    f.write(sa(19, 12, omega))
    f.write(sa(19, 12, omegadot))
    f.write("\n")

    # orbit 5
    idot = keywords.get("idot")
    l2 = 0
    WN = keywords.get("WN")
    l2pflag = 0

    f.write(" " * 4)
    f.write(sa(19, 12, idot))
    f.write(sa(19, 12, l2))
    f.write(sa(19, 12, WN))
    f.write(sa(19, 12, l2pflag))
    f.write("\n")

    # orbit 6
    sv_accuracy = 0
    sv_health = keywords.get("sv_health")
    tgd = keywords.get("tgd")
    iodc = keywords.get("iodc")

    f.write(" " * 4)
    f.write(sa(19, 12, sv_accuracy))
    f.write(sa(19, 12, sv_health))
    f.write(sa(19, 12, tgd))
    f.write(sa(19, 12, iodc))
    f.write("\n")

    # orbit 7
    HOW = keywords.get("HOW")
    array = 0

    f.write(" " * 4)
    f.write(sa(19, 12, HOW))
    f.write(sa(19, 12, array))
    f.write("\n")

def sa(whole, little, num):
    s = "%" + str(whole) + "." + str(little - 1) + "e"
    t = s % (num * 10)
    index = t.find(".")
    t = t.replace("e", "D")
    l = list(t)
    l[index - 1], l[index] = l[index], l[index - 1]
    t = "".join(l)
    return t

def gen_filename(si, doy, nh, sm, yr, ft):
    """
    生成RINEX文件文件名

    ssssdddhmm.yyO 
    | | || | | 
    | | || | +- O: observation file 
    | | || +--- yy: two-digit year 
    | | |+------ mm: starting minute within the hour (00, 15, 30, 45) 
    | | +------- h: character for the n-th hour in the day 
    | | a = 1st hour: 00h-01h; b = 2nd hour: 01h-02h; 
    | | . . . x = 24th hour: 23h-24h. 
    | +--------- ddd: day of the year 
    +------------ ssss: 4-char station ID or ID for the LEO 
 receiver/antenna 

    Arguments:
    - `si`:station ID
    - `doy`: day of the year
    - `nh`: n-th hour in the day
    - `sm`: starting minute within the hour
    - `yr`: two-digit year
    - `ft`: file type
    """
    # Check needed!

    return si + doy + nh + sm + '.' + yr + ft    
    
def print_obs_data(epoch, data, f):
    """
    打印一个历元的观测数据
    epoch = [[year, month, day, hour, min, sec], epoch_flag, # of sats in current epoch, receiver clock offset]
    data = [[sat, [obs, lli, signal strength],...],...,]
    """

    f.write("> ")
    y,M,d,h,m,s = epoch[0]
    f.write(str(y).rjust(4)+str(M).rjust(3)+str(d).rjust(3)+str(h).rjust(3)+str(m).rjust(3))
    f.write("%11.7f" % float(s))
    epoch_flag = epoch[1]
    sat_number = int(epoch[2])
    f.write(epoch_flag.rjust(3))
    f.write(str(epoch[2]).rjust(3)+" "*6)
    f.write("%15.12f\n" % float(epoch[3]))
    
    for i in range(sat_number):
        f.write(data[i][0].ljust(5))
        for ob in data[i][1:]:
            f.write("%14.3f" % float(ob[0]))
            f.write(ob[1].rjust(1)+ob[2].rjust(1))
        f.write("\n")

    



# a = print_obs_header()
# f = open(a, 'a')
# print_obs_data([["2012","11","13","0","0","0"],"0","2","0"], [["G13",["12412.3", "", "8"], ["33.14", "", "6"]],["R6",["38.4","","8"]]], f)
# b = print_nav_header()

        
        
