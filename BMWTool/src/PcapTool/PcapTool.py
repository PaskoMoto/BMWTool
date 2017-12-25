#!coding:utf8

'''
Date:2017/12/21/14:02
Author:yqq
Description:  解析 pcap 文件 获取 数据
'''



# -*- coding: utf-8 -*-
import json


#gPC_IP = "169.254.240.253"   #笔记本电脑的ip地址
gPC_IP = "169.254.152.227"   #笔记本电脑的ip地址
#gECU_IP = "169.254.48.1"     #实体ecu的ip地址
gECU_IP = "169.254.67.16"     #实体ecu的ip地址
gB_IP = "255.255.255.255"   #广播地址


def store(data):
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load(filePath):
    with open(filePath, "r") as json_file:
        data = json.load(json_file)
        return data



if __name__ == "__main__":
    #dataList  = load(u"../../txt/data.json")
    # dataList  = load(u"../../txt/gg.json")
    dataList  = load(u"../../txt/实体ecu的数据.json")


    with open(u"../../doc/tmp/cmd_rr.txt", "w") as outFile:
        for eachDict in dataList:

            if "data" not in eachDict["_source"]["layers"]:
                continue

            if ("udp" not in eachDict["_source"]["layers"]) and \
                ("tcp" not in eachDict["_source"]["layers"]):
                continue


            try:
                srcIP = eachDict["_source"]["layers"]["ip"]["ip.src"].strip()
                # print(eachDict["_source"]["layers"]["ip"]["ip.src"])

                dstIP = eachDict["_source"]["layers"]["ip"]["ip.dst"].strip()
                # print(eachDict["_source"]["layers"]["ip"]["ip.dst"])


                # 请求还是回复
                tmpStr = ""
                if (srcIP.strip() == gPC_IP) and \
                        (dstIP.strip() == gECU_IP or dstIP.strip() == gB_IP):
                    tmpStr = "Req: "
                elif (srcIP.strip() == gECU_IP) and (dstIP.strip() == gPC_IP):
                    tmpStr = "Rsp: "
                else:
                    print("{0}-->{1}".format(srcIP, dstIP))
                    continue

                # tmpStr = ""

                # print(eachDict["_source"]["layers"]["data"]["data.data"].replace(":", " ").upper())


                #print(tmpStr + "" + eachDict["_source"]["layers"]["data"]["data.data"].replace(":", " ").upper())
                outFile.write(tmpStr + "" + eachDict["_source"]["layers"]["data"]["data.data"].replace(":", " ").upper() + "\n")

                pass
            except:
                pass




