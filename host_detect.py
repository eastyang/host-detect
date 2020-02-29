# -*- coding: utf-8 -*-
"""创建于2020.02.28"""
import sys
import os
import time
import threading
from datetime import datetime


def main():
    """主函数"""
    host_file_path = "./host_list.txt"
    sleeptime = 5
    host_list = read_file(host_file_path)
    for host in host_list:
        host = host.strip()
        if len(host) > 0:
            try:
                print("%s host detect start" % host)
                threading._start_new_thread(ping_runing, (host, sleeptime,))
                time.sleep(3)
            except KeyboardInterrupt as e:
                print("Error: unable to start ping_detect thread!")
    try:
        while 1:
            pass
    except KeyboardInterrupt as e:
        print("\nHost detect master process running break: "+ str(e))
        sys.exit()


def ping_runing(ipaddr, sleeptime):
    """启动ping探测"""
    try:
        while 1:
            time.sleep(sleeptime)
            host_state = ping_detect(ipaddr)
            write_logfile(ipaddr, host_state)
            print("%s [%s]"% (current_time(), host_state))
    except KeyboardInterrupt as e:
        print("\nHost detect running break: "+ str(e))
        sys.exit()


def ping_detect(ipaddr):
    """ping探测"""
    timeout = '5'
    os_flag = 'c'
    p_result = os.popen('ping -W %s -%s 1 %s 2>/dev/null'%(timeout, os_flag,ipaddr)).readlines()[1]
    if p_result.find("time") >= 0:
        host_state = p_result.replace('\n', '')
    else:
        #host_state = "64 bytes from 192.168.100.1: icmp_seq=0 ttl=64 time=2.559 ms"
        host_state = "64 bytes from " + ipaddr + ": icmp_seq=0 ttl=NO time=timeout!!"
    return host_state


def current_date():
    """返回当前日期"""
    dt = datetime.now()
    dt_str = dt.strftime( '%m%d_%H' )
    return dt_str


def current_time():
    """返回当前日期时间，精确到秒"""
    dt = datetime.now()
    dt_str = dt.strftime( '%Y-%m-%d %H:%M:%S ' )
    return dt_str


def read_file(filename):
    """读取文件到列表"""
    try:
        file_handle = open(filename, "r")
        textlist = file_handle.read().splitlines()
        file_handle.close()
        return textlist
    except IOError as e:
        print("Read file error: "+ str(e))
        sys.exit()


def write_logfile(ipaddr, hoststat_str):
    """写入日志到日志文件"""
    log_name = ipaddr + "_" + current_date() + ".log"
    log_str = current_time() + "[" + hoststat_str + "]"
    try:
        file_handle = open(log_name, "a")
        file_handle.write(log_str+'\n')
        file_handle.close()
    except IOError as e:
        print("Write file error: "+ str(e))
        sys.exit()
    #print(log_name) 


if __name__ == "__main__":
    main()

