#! coding:utf8

# version 13 , update time: 2018-03-08
# update description :
#       添加 二进制类    MyBinary



import re
import os
from collections import OrderedDict  # 有序字典


class TextTool:
	'''
	# TextTool说明:
	# 段(section): 从段ID加上'\"'开始到'\n"'结束 
	# 域(filed):  如: "[Menu]"
	# 键值对(keyPair): 如: 'VehEcuID=1389'

	# 数据结构:
	# dict = {sect1:{filed1:{key1:[value1, value2], key2:[value1, value2]}}}	

	'''

	def __init__(self, filePath, isOrder=True):
		'''
		:param filePath: 输入文件路径
		:param isOrder: 是否有序, True:有序(速度慢); False: 无序(速度快)
		'''

		self.__filePath = filePath.strip()
		self.allSectListOfFile = []

		# 设置是否按照插入的顺序排序
		self.__isOrder = isOrder
		if self.__isOrder:
			self.allSectDictOfFile = OrderedDict()
		else:
			self.allSectDictOfFile = {}

		self.__GetAllSectDictFromFile()
		pass

	def __GetFieldsFromSect(self, sectString):
		'''
		:param sectString: 
		:return: 
		'''

		lineList = sectString.splitlines()
		sectHexStrID = (lineList[0].strip())[0: lineList[0].find('\t')]
		filedList = sectString.split('[')

		if self.__isOrder:
			sectFiledsDict = OrderedDict()
		else:
			sectFiledsDict = {}

		for filed in filedList:
			filedLineList = filed.splitlines()
			filedName = ''

			if self.__isOrder:
				filedKVDict = OrderedDict()
			else:
				filedKVDict = {}

			for line in filedLineList:
				if '=' in line:
					key = line.split('=')[0].strip()
					tmpKeyList = key.split('+')
					tmpValue = line.split('=')[1]
					value = tmpValue[0: tmpValue.find('\t')]
					for eachKey in tmpKeyList:
						if eachKey not in filedKVDict:
							filedKVDict[eachKey] = []
						filedKVDict[eachKey].append(value)
					continue
				if ']' in line:
					filedName = line[0: line.find(']')]
			if filedName != '':
				sectFiledsDict[filedName] = filedKVDict
		self.allSectDictOfFile[sectHexStrID] = sectFiledsDict
		pass

	def __GetAllSectDictFromFile(self):
		'''
		:return: 
		读数据
		'''

		with open(self.__filePath, 'r') as f:
			fileContent = f.read()

		pattern = r'^0x.*?\\n\"'  # 用正则表达式匹配" 段"
		reObj = re.compile(pattern, re.DOTALL + re.MULTILINE)
		self.allSectListOfFile = reObj.findall(fileContent)

		for sect in self.allSectListOfFile:
			self.__GetFieldsFromSect(sect)
			pass

	def ShowAll(self):
		'''
		:return: 无
		打印
		'''

		allSectDict = self.allSectDictOfFile
		for sectKey in allSectDict:
			sectDict = allSectDict[sectKey]
			print ('{0}'.format(sectKey))
			for filedKey in sectDict:
				filedDict = sectDict[filedKey]
				print ('[{0}]'.format(filedKey))
				for keyPairKey in filedDict:
					for listItem in filedDict[keyPairKey]:
						print('{0}={1}'.format(keyPairKey, listItem))
				print ('\n')
		pass

	def WriteFile(self, filePath):
		'''
		此方法主要用于, 修改值之后, 写回文件
		:param filePath: 输出文件路径
		:return: 
		'''

		# if not os.path.exists(os.path.dirname(filePath)):
		#	os.mkdir(os.path.dirname(filePath)) #如果目录不存在则创建

		if self.__filePath.strip() == filePath.strip():
			print("inFile == outFile")  # 输入的文件和输出的文件不能是同一个
			raise ValueError

		if os.path.exists(os.path.dirname(filePath)):
			with open(filePath, "w") as outFile:
				allSectDict = self.allSectDictOfFile
				for sectKey in allSectDict:
					sectDict = allSectDict[sectKey]
					# print ('{0}'.format(sectKey))
					outFile.write('{0}\t\t\"\\\n'.format(sectKey))  # 索引
					for filedKey in sectDict:
						suffix = '\t' * 5 + '\\n\\\n'
						filedDict = sectDict[filedKey]
						# print ('[{0}]'.format(filedKey))
						outFile.write('[{0}]{1}'.format(filedKey, suffix))  # 域名
						for keyPairKey in filedDict:
							for listItem in filedDict[keyPairKey]:
								# print('{0}={1}'.format(keyPairKey, listItem))
								outFile.write('\t{0}={1}{2}'.format(keyPairKey, listItem, suffix))  # 键值对
					outFile.write("{0}".format('\t' * 5 + '\\n\"\n\n'))
			pass
		else:
			print("Dir not exist!")
			raise ValueError


class TabTextTool:
	'''
	#处理以tab键分隔的文件
	#处理制表符分隔的文件类
	#数据结构: 一行一个列表
	[{k1:v1, k2:v2, k3:v3}, {k1:v1, k2:v2, ...}, {},... ]
	'''

	class LengthNotMatchError(RuntimeError):
		'''
		自定义一个异常类
		'''

		def __init__(self, arg):
			# print(arg)
			self.message = "Length Not Matching!"
			self.args = arg

	def __init__(self, inFilePath, inFieldNameList=list()):
		self.inFilePath = inFilePath
		self.allSplitedLineList = self.__ReadTabFile(inFilePath)
		self.allNamedSplitedList = []
		if len(inFieldNameList) > 0:
			self.allNamedSplitedList = self.__AddFieldName(self.allSplitedLineList, inFieldNameList)

	def __ReadTabFile(self, inFilePath):
		'''
		:param inFilePath: 输入文件路径
		:return: 
		'''
		retList = []
		if not os.path.exists(inFilePath):  # 文件不存在, 引发异常
			print("inFilePath not exists")
			raise ValueError
		if os.path.isfile(inFilePath):
			with open(inFilePath, "r") as inFile:
				contentList = inFile.readlines()
				for eachLine in contentList:
					if '\t' in eachLine:
						tmpListSplitedList = []
						tmpList = eachLine.split("\t")
						if len(tmpList) != 0:
							for item in tmpList:
								tmpListSplitedList.append(item.strip())
							retList.append(tmpListSplitedList)
						else:
							retList.append([])
				pass
		return retList

	def __AddFieldName(self, allSplitedLineList, inFieldNameList):
		'''
		:param allSplitedLineList:  
		:param inFieldNameList: 
		数据结构 : [{field1:value1, filed2:value2, ....}, {}, {},....]
		:return: 
		'''

		retList = []

		for eachLine in allSplitedLineList:

			if len(eachLine) != len(inFieldNameList):
				# 引发一个自定义异常
				print(len(eachLine))
				print(len(inFieldNameList))
				raise self.LengthNotMatchError(inFieldNameList)  # key的数量和value的数量不匹配,异常

			tmpLineDict = OrderedDict()
			for i in range(len(eachLine)):
				tmpLineDict[inFieldNameList[i]] = eachLine[i]
			retList.append(tmpLineDict)
		return retList

	def WriteFile(self, outFilePath):
		'''
		:param outFilePath: 输出文件路径
		:return: 
		如果需自定义输出文件格式, 重写这个函数即可
		'''

		tmpList = self.allNamedSplitedList

		if len(tmpList) == 0:
			raise ValueError
		else:
			with open(outFilePath, "w") as outFile:
				for eachLine in tmpList:
					outFile.write("\n=============\n")
					for eachFieldName, eachFieldValue in eachLine.items():
						if "NO-USE" in eachFieldName: continue
						outFile.write("\t{0}={1}\n".format(eachFieldName, eachFieldValue))
		pass

	def ShowAll(self):
		inList = self.allSplitedLineList
		for eachLine in inList:
			print("\n==============")
			for eachField in eachLine:
				print("{0}={1}\n".format("????", eachField))


class RootMenu:
	'''
	RootMenu说明: 使用此类时, root菜单文件的首行必须是"车名", 
	             如果有多个"车"(不是车型), 则只要把
	             __init__函数中, lineList.remove(lineList[0]) 注释掉即可

	数据结构:
	{
	车名1: 
		{
			车型1 : 
			{
				系统1:
				{
					Ecu名1 : [ecuId1, ecuId2, ...]
					Ecu名2 : [ecuId1, ecuId2, ...]
					...
				},
				系统2:
				{
				}
			},  

			车型2 : {},
		}
	车名2:
		{
			...
		}
	}


	'''

	def __init__(self, inFilePath, isOrder=True):
		if os.path.isfile(inFilePath):
			with open(inFilePath, "r") as inFile:
				lineList = inFile.readlines()

				# lineList.remove(lineList[0]) #去掉首行的车名, 如果有多个车(不是车型, 如: 高低配),注释这句即可

				self.__isOrder = isOrder  # True表示按照插入顺序排序(速度慢), False则为无序(速度快)
				if self.__isOrder:
					self.menuDict = OrderedDict()  # 菜单树,(有序)
				else:
					self.menuDict = {}  # 菜单树,(无序)
				self.__AddMenuItem(self.menuDict, lineList)
				# print(len(retDict))
				# ShowAll(retDict, 0)
				pass
		else:
			raise ValueError
		pass

	def __AddMenuItem(self, inDict, nodeList):
		'''
		:param inDict: 传入传出参数, 菜单树(字典)
		:param nodeList: 剩余的节点列表
		:return: 无
		'''

		# 算法设计(递归)
		# 1.如果是叶子节点,将此节点挂在其父节点下面; --->递归边界条件
		# 2.如果不是叶子节点,将此节点的所有子节点挂上来, 再把此节点挂在其父节点上;
		# 3.再处理其他节点

		if (nodeList == None) | (nodeList == []):
			return
		if self.__IsLeafNode(nodeList[0]):  # 1.如果是叶子节点, 将此节点挂在其父节点下面; --->递归边界条件
			inDict[self.__GetLeafNodeNameAndID(nodeList[0])[0]] = [self.__GetLeafNodeNameAndID(nodeList[0])[1]]
			nodeList.remove(nodeList[0])
		else:
			if self.__isOrder:
				tmpDict = OrderedDict()  # 有序字典
			else:
				tmpDict = {}  # 无序字典

			tmpNode = nodeList[0]
			subNodeList = self.__GetSubNode(nodeList)

			self.__AddMenuItem(tmpDict, subNodeList)  # 2.将此节点下的所有子节点挂上来
			inDict[tmpNode.strip()] = tmpDict  # 再把此节点挂在其父节点上

		self.__AddMenuItem(inDict, nodeList)  # 3.再处理其他的节点

		pass

	def __GetSubNode(self, inList):
		'''
		:param inList: 剩余节点链表(还未处理的节点列表)
		:return: inList[0] 下所有子节点组成的列表, 所有这些处理过的子节点都会从inList中永久删除
		'''

		# 获取此节点下所有子节点,同时删掉以处理掉的节点
		parentNode = inList[0]  # 将第一个作为父节点
		inList.remove(inList[0])  # 永久删除已经处理的parentNode这个节点,注意remove()是没有返回值
		if len(inList) == 0:
			return []

		tmpNodeList = []
		while True:
			if len(inList) == 0:  # 节点列表空了
				break
			if inList[0].count('\t') > parentNode.count('\t'):  # 即字节点的tab的数量一定大于父节点
				tmpNodeList.append(inList[0])
				inList.remove(inList[0])  # 删掉已经处理过的节点
			else:
				break
		return tmpNodeList

	def __IsLeafNode(self, inStr):
		'''
		:param inStr: 节点字符串
		:return: 如果是叶子节点返回True; 否则返回False
		'''
		inStr = inStr.strip()
		if ('<' in inStr) & ('>' in inStr):
			return True
		return False

	def __GetLeafNodeNameAndID(self, inStr):
		'''
		:param inStr: 节点字符串, 比如:   安全气囊<900021> 
		:return: 返回节点名称(Ecu名称)和节点ID(ECU ID)
		'''

		inStr = inStr.strip()
		if ('<' in inStr) & ('>' in inStr):
			return [inStr[: inStr.find('<')], inStr[inStr.find('<') + 1: inStr.find('>')]]
		raise ValueError

	def ShowAll(self, inDict='self.menuDict', tabCount=0):
		'''
		:param inDict:  root菜单树(字典)
		:param tabCount: 缩进的tab数量
		:return: 无
		'''
		if inDict == 'self.menuDict':
			inDict = eval(inDict)

		if isinstance(inDict, list):
			return
		# print("{0}{1}".format('\t'*tabCount, inDict[0]))
		elif isinstance(inDict, dict):
			for key, value in inDict.items():
				if isinstance(value, list):
					print("{0}{1}<{2}>".format('\t' * tabCount, key, value[0]))  # 叶子节点,ECU
				else:
					print("{0}{1}".format('\t' * tabCount, key))  # 系统

				self.ShowAll(value, tabCount + 1)  # 继续递归
		else:  # 参数类型错误
			print(type(inDict))
			raise ValueError
		pass

	def HereditaryTraverse(self, inDict='self.menuDict', preStr='', separator='\t',
	                       leafNodeType=list, outFileObj=None):
		'''
		遗传遍历

		每次都从根开始遍历,  即保存"祖先"的信息 , 我称之为 "遗传遍历"

		使用这个函数, 可以直接将菜单转换为 <<车型表>>

		:param inDict:  输入字典
		:param preStr: 祖先信息
		:param separator: 分隔符
		:param leafNodeType: 保存叶子节点的"容器" 一般为 list
		:param outFileObj: 输出文件对象
		:return: 无
		'''
		if inDict == 'self.menuDict':
			inDict = eval(inDict)  # 将字符串转换为对应的变量

		if isinstance(inDict, leafNodeType):  # 递归终止条件
			for item in inDict:
				print("{0}{1}".format(preStr, item))
				if isinstance(outFileObj, file):
					# outFileObj.write("{0}{1}\n".format(preStr,  item)) #EcuId 放后面
					outFileObj.write("{0}\t{1}\n".format(item, preStr))  # EcuId 放前面
			return

		elif isinstance(inDict, dict):
			for k, v in inDict.items():
				tmpPreStr = preStr + k + separator
				self.HereditaryTraverse(v, preStr=tmpPreStr, outFileObj=outFileObj)  # 递归
		else:
			pass
		pass




class MyBinary:
	'''
	设计一个二进制类 提供 必要的转换函数
	'''

	def __init__(self, intValue = 0):
		self.__intValue = intValue                  #十进制值
		self.__binStr = self.Format(intValue)       #二进制字符串
		self.__intStr = str(intValue)               #十进制字符串
		self.__hexStr = hex(intValue)[2:]           #十六进制字符串
		self.__octStr = oct(intValue)[1:]            #八进制字符串
		pass


	def Set0or1(self, choose, intValue, *bits):
		'''
		将某几位设置为 1
		:param choose: 0设置为0 ,   1设置为1
		:param intValue: 
		:param bits: 哪位
		:return: 设置之后的 10 进制数
		'''
		if choose == '1' or choose == 1:
			replaceStr = '1'
		else:
			replaceStr = '0'

		# print(bits)

		if (not isinstance(intValue, int)):
			print("num or intValue type error")  #num 或 inValue 类型错误
			raise ValueError
		if len(bits) ==  0:
			print('bits is empty') #bits 为空
			raise  ValueError

		strBinTmp = self.Format(intValue)
		binStrList = list(strBinTmp)

		for bitPos in bits:
			try:
				binStrList[7 - bitPos] = replaceStr
			except:
				print('bitPos error')
				raise ValueError

		try:
			retValue = int(''.join(binStrList), 2)
		except:
			print('strBinTmp convert error')  #转换错误
			raise ValueError

		return  retValue


	def GetAll_1_Pos(self, intValue):
		'''
		获取一个整数中所有的 1 的位置
		:param intValue: 10进制数
		:return: 所有 1 的位置 组成的列表
		'''
		if (not isinstance(intValue, int))  or (intValue > 0xFF):
			print('inValue type error  or  inValue greater than 0xff')
			raise ValueError

		retList = []
		strBinTmp = self.Format(intValue)
		for i in range(len(strBinTmp)):
			if strBinTmp[i] == '1':
				retList.append(7 - i)

		retList.reverse()
		return  retList


	def Format(self, intValue, byteCount=1):
		'''
		将 intValue 格式化 二进制字符串
		:param intValue: 
		:param byteCount: 
		:return: 
		'''
		if (not isinstance(intValue, int) ) \
				or ( not  isinstance(byteCount, int) ) \
				or (byteCount < 1 ):
			print('intValue or byteCount type error')
			raise ValueError
			pass

		return ('%{0}s'.format(byteCount * 8) % (bin(intValue)[2:])).replace(' ', '0')

	pass






def ReadText(inFilePath, tabCount):
	'''
		:param inFilePath: 读inFilePath文件, 如CN_TEXT.txt
		:return: 返回一个字典(按插入顺序排序)
	'''
	if os.path.isfile(inFilePath):
		with open(inFilePath, "r") as lan:
			linesList = lan.readlines()
		# retLanDict = {}
		retLanDict = OrderedDict()
		for line in linesList:
			if ('\t') not in line:
				continue
			if line != "\n":
				key = line.split("\t" * tabCount)[0]
				tmpStr = line.split("\t" * tabCount)[1]
				value = tmpStr[tmpStr.find("\"") + 1: tmpStr.rfind("\"")].strip()
				retLanDict[key] = value
		return retLanDict
	else:
		print(inFilePath + u"不是文件! 或者不存在! ")
		raise ValueError


# def ReadTextPlus(inFilePath):
# 	'''
# 		:param inFilePath: 读inFilePath文件, 如CN_TEXT.txt
# 		:return: 返回一个字典(按插入顺序排序)
# 	'''
# 	if os.path.isfile(inFilePath):
# 		with open(inFilePath, "r") as lan:
# 			linesList = lan.readlines()
# 		# retLanDict = {}
# 		retDict = OrderedDict()
# 		for line in linesList:
# 			if line != "\n":
# 				fieldCount = len(line.split('\t\t'))
# 				key = line.split("\t\t")[0]
# 				valueList = line.split('\t\t')[1:]
# 				newValueList = []
# 				for value in valueList:
# 					if (value[0] == '"') & (value[-1] == '"'):
# 						newValueList.append(value[1:-1])
# 					else:
# 						newValueList.append(value)
# 				retDict[key] = newValueList
# 		return retDict

def ReadTextPlus(inFilePath, tabCount):
	'''
		:param inFilePath: 读inFilePath文件, 如CN_TEXT.txt
		:return: 返回一个字典(按插入顺序排序)
	'''
	if os.path.isfile(inFilePath):
		with open(inFilePath, "r") as lan:
			linesList = lan.readlines()
		# retDict = {}
		retDict = OrderedDict()
		for line in linesList:
			if line != "\n":
				splitStr = tabCount * '\t'
				fieldCount = len(line.split(splitStr))
				key = line.split(splitStr)[0]
				valueList = line.split(splitStr)[1:]
				newValueList = []
				for value in valueList:
					if (value[0] == '"') & (value[-1] == '"'):
						newValueList.append(value[1:-1])
					else:
						newValueList.append(value)
				retDict[key] = newValueList
		return retDict


def Add0x(inStr):
	'''
	:param inStr: 例如:   0022334455    
	:return: 返回 0x00,0x22,0x33,0x44,0x55
	'''
	inStr = inStr.strip()  # 去除空白符
	if (len(inStr) & 1):  # 输入的是奇数
		print(">>>>" + inStr)
		raise ValueError
	else:
		return ''.join("0x" + inStr[i * 2: i * 2 + 2] + "," for i in range(len(inStr) / 2))[0: -1]
	pass


def Del0x(inStr):
	'''
	:param inStr:0x00,0x22,0x33,0x44,0x55 
	:return:0022334455   
	'''
	inStr = inStr.strip()
	return inStr.replace("0x", "").replace(",", "")


def MyHex(inArg):
	'''
	:param inArg:  
	:return: 将一个整数(最大255), 或者十进制整数字符串转换为0xAB类型的
	'''

	tmpStr = str(inArg)
	if tmpStr.isdigit():
		tmpInt = int(tmpStr, 10)
		if tmpInt > 255:
			raise ValueError
	else:
		print(type(inArg))
		raise ValueError
	return "0x" + ("%02x" % tmpInt).upper()


def MyHexPlus(inArg):
	'''
	:param inArg: 将一个整数, 或者十进制整数字符串转换为0xAB类型的 
	:return: 
	'''
	tmpStr = hex(int(str(inArg), 10))[2:].upper()
	if (len(tmpStr) & 1):
		tmpStr = '0' + tmpStr
	return Add0x(tmpStr)


def MyHexPlusPlus(inArg, fillLength=1):
	'''
	:param inArg: 将一个整数, 或者十进制整数字符串转换为0xAB类型的 
	:param fillLength :  填充到多少个字节 
	:return: 
	'''
	if (int(str(inArg), 10) <= (2 << (fillLength * 8 - 1)) - 1):
		tmpLen = len(hex(int(str(inArg), 10))[2:].upper())
		return Add0x('0' * (2 * fillLength - tmpLen) + hex(int(str(inArg), 10))[2:].upper())

	tmpStr = hex(int(str(inArg), 10))[2:].upper()
	if (len(tmpStr) & 1):
		tmpStr = '0' + tmpStr
	return Add0x(tmpStr)


def ShowMessageBox(titleText, contentText):
	'''
	显示一个提示对话框
	:param titleText:  标题文本
	:param contentText:  提示内容文本
	:return: 
	'''
	from tkMessageBox import showinfo
	showinfo(titleText, contentText)
	pass


def DictKVInvert(inDict, isOrder=False):
	'''
	字典键值互换
	:param inDict: 
	:return: 
	'''
	if isOrder:
		retDict = OrderedDict()
	else:
		retDict = dict()

	for k, v in inDict.items():
		retDict[v] = k
	return retDict


def GetTextFromTextLib(indexKey, retOfReadTextPlus):
	'''
	从textFilePath获取文本 
	(适用于 以tab分隔的文本库, 如： cn_text.txt  express.txt  ...)
	:param indexKey:   带0x的索引 或者 不带 0x 的索引
	:param textFilePath:  文本库的路径 
	:param tabCount: 文本库 分隔 tab的数量
	:return:  list
	'''
	retDict = retOfReadTextPlus
	if ('0x' in indexKey):
		index = Add0x(Del0x(indexKey))
	else:
		index = Add0x(indexKey)
	if (index in retDict):
		return retDict[index]
	else:
		return []  # 空列表


def JoinDir(inFileDir, outFilePath=""):
	'''
	将一个目录下的所有文件合并成一个文件
	:param inFileDir: 
	:param outFileName: 
	:return: 
	'''
	if not os.path.exists(inFileDir):
		print("inFileDir is not exists")
		raise ValueError

	if outFilePath == "":
		print("outFilePath is empty")
		raise ValueError

	# if  not os.path.exists( os.path.join(outFilePath, outFileName) ):
	#	raise ValueError

	with open(outFilePath, "w") as joinedFile:
		for eachFileName in os.listdir(inFileDir):
			eachFilePath = os.path.join(inFileDir, eachFileName)
			with open(eachFilePath, "r") as inFile:
				tmpLinesList = inFile.readlines()
				joinedFile.writelines(tmpLinesList)

	pass


#
# def JoinTwoFile(fileName1, fileName2, outFilePath):
# 	'''
#
# 	:param fileName1: 待合并的文件1
# 	:param fileName2: 待合并的文件2
# 	:param outFilePath: 已合并的文件
# 	:return:
# 	'''
#
# 	with open(fileName1, "r") as inFile1, open(fileName2, "r") as inFile2,\
# 		open(outFilePath, "w") as outFile:
# 		lines1 = inFile1.readlines()
# 		lines2 = inFile2.readlines()
#
# 		outFile.writelines(lines1)
# 		outFile.writelines(lines2)
#
# 	pass


def InList(inStr, inList):
	for item in inList:
		if item in inStr:
			return True
	return False












