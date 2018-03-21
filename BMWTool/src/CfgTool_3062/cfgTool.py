#!coding:utf8

'''
Date:2018/2/28/16:48
Author:yqq
Description:生成3062 算法表达式
'''

from lib.mytool12 import Add0x

is3062 = 0


#gOutputConfigPath = '../../doc/tmp/3062_config.txt'
#gOutputIndexPath = '../../doc/tmp/3062_index.txt'
#gOutputTextPath = '../../doc/tmp/3062_Text.txt'
gInConfigPath = ''
gCmd = ''
if is3062:
	gInConfigPath = '../../txt/3062_CONFIG.TXT'
	gCmd = '3062'
else:
	gCmd = '3063'
	gInConfigPath = '../../txt/3063_CONFIG.TXT'

gVStrList = []

gIndexFilePath = "../../doc/tmp/cfgIndex.txt"
gOutConfigPath = "../../doc/tmp/config.txt"
goutTextPath = '../../doc/tmp/cn_text.txt'


gOutputIndexFile = ''


def DelSpace(inStr):
	'''
	删除inStr 中 else 前面的
	:param inStr: 
	:return: 
	'''

	if ('; else' in inStr) :
		retStr = inStr.replace('; else', ';else')  #去掉else前面的空格
	elif (';  else' in inStr):
		retStr = inStr.replace(';  else', ';else')
	else:
		retStr = inStr

	return  retStr


def GetAL(ctrlType, al):
	'''
	生成算法
	:param ctrlType: 算法控制类型
	:param al: 算法 
	:return: 算法表达式
	'''

	retStrExp = ''

	if 'byte' in ctrlType.lower():
		#整个字节控制

		retStrExp += 'string y; BYTE x;if(0) y=0;'

		valueList = al.split(';')
		for eachValue  in valueList:
			try:
				v = eachValue.split(':')[0]
				vStr = eachValue.split(':')[1]
				if vStr.strip() not in gVStrList:
					gVStrList.append(vStr.strip())
				retStrExp += 'else if(0x{0} == x) y={1};'.format(v, vStr)
			except:
				print(eachValue)

			pass

	elif ('&' in  ctrlType) or ('x' in ctrlType):
		#位控制
		retStrExp += 'string y; BYTE x; if(0) y=0;'
		valueList = al.split(';')
		for eachValue in valueList:
			try:
				v = eachValue.split(':')[0]
				vStr = eachValue.split(':')[1]
				if vStr.strip() not in gVStrList:
					gVStrList.append(vStr.strip())
				retStrExp += 'else if({0} == 0x{1}) y={2};'.format(ctrlType, v, vStr)
			except:
				print(eachValue)
			pass

		pass

	else:
		print ("GetAL error occur")
		return  'GetAL error'

	retStrExp += 'else y=\\\"0x00,0x00,0x00,0x00,0x00,0x02\\\";'
	return DelSpace(retStrExp)



def GetIndex(gCmd, startPos, ctrlType, length, no):
	'''
	生成索引
	:param gCmd: 
	:param startPos: 
	:param ctrlType: 
	:param length: 
	:param no: 
	:return:  索引
	'''

	if 'byte' in ctrlType:
		ctrlType = '01'
	else:
		ctrlType = '00'

	index = gCmd + '%02X'%(int(startPos)) + ctrlType + '%02X'%(int(length)) + "%04X" % (int(no))

	tmpStr = ''
	try:
		tmpStr =   Add0x(index.upper())

		pass
	except:
		print('%02X'%(int(startPos)))
		print('%02X'%(int(length)))
		print("%02X" % (int(no)))
		pass


	global gOutputIndexFile
	gOutputIndexFile.write('\t' + 'Item%03d'%no  + '=' + index[4:] + '\t\t\t\\n\\' + '\n')

	return  tmpStr


def DealCfg(cfg, no):

	splitList = cfg.split('\t')

	if len(splitList) < 3:
		print(cfg + "发生了错误， 请检查！")
		return "ERROR 0"
	cfgName = splitList[0]  #配置名称
	items = splitList[1]    #起始字节 长度 控制类型


	if len(items.split(',')) < 3:
		return  "ERROR 1"
	startPos = items.split(',')[0]  #起始字节
	length = items.split(',')[1]    #长度
	ctrlType = items.split(',')[2]  #控制类型

	al = GetAL(ctrlType, splitList[2]) #生成算法

	index = GetIndex(gCmd, startPos, ctrlType, length, no)

	return "{0}\t{1}\t{2}".format(index, '"' + cfgName + '"', '"' + al + '"')




def main():

	global gOutputIndexFile
	gOutputIndexFile = open(gIndexFilePath, 'a')
	if is3062:
		gOutputIndexFile.write("0x00,0x00,0x00,0x22,0x30,0x62\t\t\"\\ \n")
	else: #30 63
		gOutputIndexFile.write("0x00,0x00,0x00,0x22,0x30,0x63\t\t\"\\ \n")

	gOutputIndexFile.write('[Items]\t\t\t\t\t\\n\\ \n')

	cfgList = []
	with open(gInConfigPath, 'r') as inFile:
		lines = inFile.readlines()
		for line in lines:
			if(line.strip() == ""):
				continue
			else:
				cfgList.append(line.strip())

	expList = []

	for i in range(len(cfgList)):
		tmpStr = DealCfg(cfgList[i], i)
		expList.append(tmpStr)
		# print(tmpStr)


	vStrDict = {}
	with open(goutTextPath, 'a') as outTextFile:
		for i in range(len(gVStrList)):
			if is3062:
				index = "30620000%04X" % (i)
			else:
				index = "30630000%04X" % (i)
			# print(Add0x(index))
			vStrDict[gVStrList[i].strip()] = Add0x(index)

			outTextFile.write("{0}\t\t\"{1}\"\n".format(Add0x(index), gVStrList[i].strip()))

			pass


	with open(gOutConfigPath, 'a') as outCfgFile:
		for exp in expList:
			newExp = exp
			for vStr, index in vStrDict.items():
				if vStr + ';' in exp:
					newExp = newExp.replace(vStr + ';', r'\"' + index + r'\"' + ';')
				else:
					pass
			#print(newExp)
			outCfgFile.write(newExp + '\n')

	gOutputIndexFile.write('\t\t\t\t\t\\n\"\n')
	gOutputIndexFile.close()

	pass


def main2():

	from shutil import copy

	copy(gIndexFilePath, r'E:\Work\Makers\LAMP\BMW\LIBTEXT\cfgIndex.txt')
	copy(gOutConfigPath, r'E:\Work\Makers\LAMP\BMW\LIBTEXT\config.txt')
	copy(goutTextPath, r'E:\Work\Makers\LAMP\BMW\LIBTEXT\cn_text.txt')

	#copy(gIndexFilePath, r'E:\Work\Makers\LAMP\BMW\LIBTEXT\cfgIndex.txt')
	#copy(gOutConfigPath, r'E:\Work\Makers\LAMP\BMW\LIBTEXT\config.txt')

	from lib.mytool12 import ShowMessageBox
	# ShowMessageBox('提示', '请继续运行 3063的工具')

	pass

if __name__ == "__main__":

	from lib.mytool12 import ShowMessageBox
	ShowMessageBox('提示', '每次运行此工具前, 都须先运行3061工具.')

	main()

	main2()



	pass