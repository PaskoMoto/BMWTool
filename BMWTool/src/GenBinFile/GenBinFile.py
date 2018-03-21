#!coding:utf8

'''
Date:2018/3/7/17:29
Author:yqq
Description:将配置 转为 BIN 文件
'''
from  collections import OrderedDict
from lib.mytool13 import MyBinary

gCsrFilePath = u'../../txt/新款1系改透镜.csr'
gRawCfgFilePath = u'../../txt/config.txt'


#{cfgName1:{k1:v1, k2:v2, k3:v3}, cfgName2:{k1:v1, k2:v2, k3:v3}, ...}
gRawCfgDict = OrderedDict()  #原始配置字典

gModifyCfgDict =  OrderedDict() #一键改配置文件 中的配置字典









def ReadCsrFile(inFilePath):
	'''
	读取csr文件
	:param inFilePath: 
	:return: 
	'''
	with open(gCsrFilePath, 'r') as inFile:
		lines = inFile.readlines()
		for line in lines:
			#print(line)
			if('Werete=' in line):
				line = line.replace('Werete=', '')
			splitList = line.split('=')
			cfgName = splitList[0]
			cfgValue = splitList[1]

			gModifyCfgDict[cfgName] = cfgValue
	pass


def ReadRawCfgFile(inFilePath):
	'''
	读取原始配置文件配置
	:param inFilePath: 文件路径
	:return: 
	'''
	with open(inFilePath, 'r') as inFile:
		lines = inFile.readlines()
		for line in lines:
			if(len(line.strip()) == 0):
				continue
			#print(line.strip())
			splitList = line.strip().split('\t')
			cfgName = splitList[0]
			startPosSome = splitList[1]  #起始字节 长度
			algorithm = splitList[2].replace('"', '') #算法

	pass






def main():

	#ReadCsrFile(gCsrFilePath)
	#ReadRawCfgFile(gRawCfgFilePath)

	tt = MyBinary(9)
	tt.IntToBinStr(9)


	pass


if __name__ == "__main__":

	main()

	pass