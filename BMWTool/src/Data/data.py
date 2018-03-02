#!coding:utf8

'''
Date:2017/12/27/14:16
Author:yqq
Description:

	处理采数的数据
'''

import os



headStr = """\
[SETTING]
	PROT=KWP
	BPS=115200
	PIN=7,15
	THREAD=
	PARAM=		;空时表示K线进入；脉冲进系统：PARAM=25,25；地址码进系统：PARAM=01,55,D0,8F,~KW2,~ADDR
	CS=ADD
	P1=5
	P2=50
	P3=3
	P4=0
[COMMAND]
"""


def main():


	dirName = u"../../txt/采数/"
	outDir = u"../../doc/tmp/采数"

	if not os.path.exists(outDir):
		os.makedirs(outDir)

	for fileName in  os.listdir(dirName):
		filePath = os.path.join(dirName, fileName )

		with open(filePath, "r") as inFile, \
				open(filePath.replace(u"/txt/", u"/doc/tmp/"), "w") as outFile:
			linesList = inFile.readlines()

			outFile.write(headStr + "\n\n\n")

			cmdStrList = []
			for line in linesList:
				if "Req" in line:
					cmdStr = line[line.find("Req:") + 4: ].strip()
					# print(cmdStr)
					cmdStrList.append(cmdStr)
					pass

			for cmdStr in cmdStrList:
				tmpAddr = cmdStr[cmdStr.find(" ") + 1 : cmdStr.find(" ") + 3].strip()
				if tmpAddr == "72":
					preStr = "Req:"
					print(preStr + cmdStr)
					outFile.write(preStr + cmdStr + "\n")

				elif tmpAddr == "F1":
					preStr = "Ans:"
					print(preStr + cmdStr + "\n\n")
					outFile.write(preStr + cmdStr + "\n\n")
				else:
					print("ggg")
					continue
	pass


if __name__ == "__main__":

	main()

	pass