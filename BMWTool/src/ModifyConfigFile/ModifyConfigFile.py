#!coding:utf8

'''
Date:2018/3/9/9:48
Author:yqq
Description:
	修改 config.TXT 为  新的库, 为了"修改配置" 时 查找对应的数据
'''
from lib.mytool13 import Add0x

gConfigFilePath_1 = '../../txt/config.txt'
gConfigFilePath_2 = '../../txt/3062_CONFIG.TXT'
gConfigFilePath_3 = '../../txt/3063_config.txt'
gCount = 0


gOutFile = open('../../doc/tmp/newConfigLib.txt', 'w')



def GetStartPos(inStr):




	pass



def ReadConfigFile1(inFilePath):
	'''
	 读 config.txt
	:param inFilePath: 
	:return: 
	'''
	def GetAndValue(inStr):
		'''
		获取  andValue
		:param inStr: 
		:return: 
		'''
		binStr = '00000000'
		if 'bit4' in binStr and 'bit5' in binStr:
			return int('00110000', 2)
		else:
			pos =  int(inStr.strip()[-1], 10)
			binStrList = list(binStr)
			binStrList[7-pos] = '1'
			print (hex(int(''.join(binStrList), 2)))
			return hex(int(''.join(binStrList), 2))

		pass


	with open(inFilePath, 'r') as inFile:
		lines = inFile.readlines()
		for line in lines:
			if len(line.strip()) == 0:
				continue
			#print(line.strip())
			line = (line.strip())

			splitList = line.split('\t')

			cfgName = splitList[0].strip()
			#ctrlByte = splitList[1].split(',')[0].strip().replace('"', '')

			if('byte' in splitList[1].split(',')[2]):
				ctrlType = 'byte'
				andValue = 'null'
				length = splitList[1].split(',')[2].count('byte')
			else:
				ctrlType = 'bit'
				andValue = GetAndValue( splitList[1].split(',')[2].strip())
				length = '1'

			algoStr =  splitList[2].strip().replace('"', '')

			global  gCount
			gCount += 1
			index =  Add0x('%012X' % gCount)

			startPos = splitList[1].split(',')[0].strip().replace('"', '')

			gOutFile.write('{0}\t\"{1}\"\t\"{2}\"\t\"{3}\"\t\"{4}\"\t\"{5}\"\t\"{6}\"\t\"3061\"\n'.format(index, cfgName, ctrlType, andValue, startPos, length, algoStr))

	pass




def ReadConfigFile_2_3(inFilePath):
	'''
	 读 config.txt
	:param inFilePath: 
	:return: 
	'''
	def GetAndValue(inStr):
		'''
		获取  andValue
		:param inStr: 
		:return: 
		'''
		andValueStr = inStr[inStr.find('&') + 1  :  inStr.find(')')]
		print (hex(int(andValueStr.replace('0x', ''), 16)))
		return andValueStr



	with open(inFilePath, 'r') as inFile:
		lines = inFile.readlines()
		for line in lines:
			if len(line.strip()) == 0:
				continue
			#print(line.strip())
			line = (line.strip())

			splitList = line.split('\t')

			cfgName = splitList[0].strip()
			ctrlByte = splitList[1].split(',')[0].strip()

			if('byte' in splitList[1].split(',')[2]):
				ctrlType = 'byte'
				andValue = 'null'
				length = splitList[1].split(',')[2].count('byte')
			else:
				ctrlType = 'bit'
				andValue = GetAndValue( splitList[1].split(',')[2].strip())
				length = '1'

			algoStr =  splitList[2].strip().replace('"', '')

			global  gCount
			gCount += 1
			index =  Add0x('%012X' % gCount)

			startPos = splitList[1].split(',')[0].strip() #起始字节

			if inFilePath == gConfigFilePath_2:
				gOutFile.write('{0}\t\"{1}\"\t\"{2}\"\t\"{3}\"\t\"{4}\"\t\"{5}\"\t\"{6}\"\t\"3062\"\n'.format(index, cfgName, ctrlType, andValue, startPos, length, algoStr))
			elif inFilePath == gConfigFilePath_3:
				gOutFile.write('{0}\t\"{1}\"\t\"{2}\"\t\"{3}\"\t\"{4}\"\t\"{5}\"\t\"{6}\"\t\"3063\"\n'.format(index, cfgName, ctrlType, andValue, startPos, length, algoStr))
			else:
				pass


	pass






def main():

	ReadConfigFile1(gConfigFilePath_1)
	ReadConfigFile_2_3(gConfigFilePath_2)
	ReadConfigFile_2_3(gConfigFilePath_3)


	gOutFile.close()

	from shutil import copy
	copy('../../doc/tmp/newConfigLib.txt', r'E:\Work\Makers\LAMP\BMW\LIBTEXT\cfgRawLib.txt')


	pass


if __name__ == "__main__":

	main()

	pass