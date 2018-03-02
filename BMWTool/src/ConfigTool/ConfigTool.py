#!coding:utf8

'''
Date:2018/2/7/8:50
Author:yqq
Description:将Excel表格 提取为库 
'''


from lib.mytool12 import Add0x
from lib.mytool12 import Del0x
from collections import OrderedDict
from src.CfgTool_3062.cfgTool import DelSpace
import os
import sys


gReadCmd = "3061"   #设置读配置的命令
gIndexFilePath = "../../doc/tmp/cfgIndex.txt"
gCounter = 1

gOutConfigPath = "../../doc/tmp/config.txt"

gCN_TEXTDict = OrderedDict()   # 确保   "aktiv"  在 "nicht_aktiv" 之后被替换


def HandleAL(bitByte, inALStr):
	'''
	处理算法
	:param bitByte:
	:param inALStr: 
	:return: 底层接口支持的算法表达式
	'''

	retStr = "string y; "

	if "byte" in bitByte.lower():
		#按字节处理的
		retStr += "BYTE x1, x2;"
		tmpSplit = inALStr.split(';')
		retStr += 'if(0 == 1) y=Unknow;'

		for each in tmpSplit:
			value = each.split(':')[0].strip()
			string = each.split(':')[1].strip()
			retStr += "else if( ({0} == x1) && ({1} == x2) ) y={2};".format("0x" + value[0:2], "0x"+value[2:], string)

		retStr += "else y=Unknow;" #收尾

	elif "bit" in bitByte.lower():
		#按位处理的
		retStr += "BYTE x1;"
		if(bitByte.count('bit') == 2):    #由2位控制

			retStr += "if(0x0 == (x1&0x30)) y=nicht_aktiv;else if(0x10 == (x1&0x30)) y=aktiv;else if(0x20 == (x1&0x30)) y=dimed;else y=Unknow;"

			pass


		if(bitByte.count('bit') == 1):    #由1位控制
			tmpList = list("00000000")
			tmpList[int(bitByte.strip()[-1])] = '1'
			tmpStr = ''.join(reversed(tmpList))
			# print(tmpList)
			number = int(tmpStr, 2)  # 将二进制转为 十进制
			# print(number)

			tmpSplit = inALStr.split(';')

			firstStr = tmpSplit[0].strip().split(':')[1]
			secondStr = tmpSplit[1].strip().split(':')[1]

			retStr += "if(0 == (x1 & {0})) y={1};else y={2};".format(hex(number), firstStr, secondStr)

			pass

		pass
	else:
		#出错了
		pass

	return  '"' + DelSpace(retStr) + '"'


def GenIndex(gReadCmd, startPos, bitByte, no):
	'''
	生成索引
	:param gReadCmd: 
	:param startPos: 
	:param bitByte: 
	:param no: 序号
	:return: 
	'''

	if 'bit' in bitByte:
		flag = 0
	else:
		flag = 1

	if bitByte.lower().count('byte') == 2:
		length = 2
	elif bitByte.lower().count('bit') == 2:
		length = 2
	else:
		length = 1

	tmpStr  = gReadCmd + ('%02X' % int(startPos, 10)) + ("%02X" % flag) + ("%02X" % length) + ("%04X" % no)

	return Add0x(tmpStr)


def MyReplace(inExp):

	retStr = inExp
	for k, v in gCN_TEXTDict.items():
		if v in retStr:
			retStr = retStr.replace(v, r'\"' +  k + r'\"' )

	return retStr


def GenIndexFile(inExp):

	tmpList = inExp.split('\t')
	index = tmpList[0].strip()

	tmpStr =  Del0x(index)[4:]

	global gIndexFile
	global  gCounter
	gIndexFile.write( '\t'+"Item" + ("%03d" % gCounter) +  "="+ tmpStr + '\t\t' + '\\n\\'+"\n")

	gCounter += 1


	pass


def main():

	global gIndexFile
	gIndexFile = open(gIndexFilePath,  "w")

	with open("../../txt/cn_text.txt", "r") as inFile:
		lines = inFile.readlines()
		for line in lines:
			if(line.strip() == ""):
				continue
			if('#include' in line):
				continue

			tmpList = line.split('\t\t')
			k = tmpList[0].strip()
			v = tmpList[1].strip()[1:-1]

			print("{0}={1}".format(k, v))

			gCN_TEXTDict[k] = v




	with open("../../txt/config.txt", "r") as inFile , \
			open( gOutConfigPath, "w") as outFile:

		gIndexFile.write(Add0x("00000022" + gReadCmd) + '\t\t' + '\"\\\n')
		gIndexFile.write("[Items]\t\t\t\t\\n\\\n")


		lines = inFile.readlines()
		for i in range(len(lines)):

			line = lines[i]

			if(line.strip() == ""):
				continue

			splitList = line.split("\t")
			try:
				#配置名称
				cfgName = '"' + splitList[0] + '"'

				#控制字段
				ctrl = splitList[1]
				startPos = ctrl.split(',')[0]
				length = ctrl.split(',')[1]
				bitByte = ctrl.split(',')[2]

				#算法
				al = splitList[2].replace('"', '')



				index = GenIndex(gReadCmd, startPos, bitByte, i)



				#print("{0}\t{1}\t{2}\n".format(index, cfgName,  HandleAL(bitByte, al)))
				strExp = ("{0}\t{1}\t{2}\n".format(index, cfgName,  HandleAL(bitByte, al)))


				newExp =  MyReplace(strExp)

				GenIndexFile(newExp)

				#outFile.write("{0}\t{1}\t{2}\n".format(index, cfgName,  HandleAL(bitByte, al)))
				outFile.write(newExp)

				pass
			except:
				continue
				pass

		gIndexFile.write("{0}\\n\"\n\n".format('\t' * 5))



	gIndexFile.close()

	from lib.mytool12 import ShowMessageBox
	ShowMessageBox('提示',  '请继续依次运行 3062 3063 的生成工具.')


	pass


if __name__ == "__main__":

	main()

	from shutil import  copy

	copy('../../txt/cn_text.txt', '../../doc/tmp/cn_text.txt')

	pass










