#!coding:utf8


'''
Author:yqq
Descriptions: 获取"廖雪峰Python教程"所有html文件
'''

import urllib
import socket
import os
from collections import OrderedDict


 #廖雪峰首页
gLxfUrlRoot = r'https://www.liaoxuefeng.com' 

#Python教程
gLxfPythonUrl = r'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000' 

#python目录名
gDirPrefix = r'/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/'  

def DealHtml(inFile):
	'''
	处理html文件获取其他网页的链接
	返回值: { 链接名: 链接, ... }
	'''

	lineList = inFile.readlines()

	#retDict = {} #无序字典
	retDict = OrderedDict() #按照插入的顺序排序的字典

	for eachLine in lineList:
		if gDirPrefix in eachLine :

			#获取url后缀
			tmpBegin = eachLine.find('<a href="') + len('<a href="')
			tmpEnd = eachLine.find('">')
			tmpLinkSuffix = eachLine[tmpBegin : tmpEnd] #获取子网页的链接

			#获取名称
			tmpBegin = eachLine.find('">') + len('">')
			tmpEnd = eachLine.find('</a>')
			tmpLinkName = eachLine[tmpBegin : tmpEnd] #获子网页的名称
			tmpLinkName = tmpLinkName.decode('utf-8') #从utf-8转为Unicode
			
			#只保存第一次存进来的
			if tmpLinkName not in retDict: 
				retDict[tmpLinkName] = tmpLinkSuffix 
		pass

	return retDict



def GetHtmlByUrl(url, inFileName=None, encoding='utf-8' ) :
	'''
	url: url
	inFileName: 输出的文件名(系统编码格式,否则否则会乱码)
	encoding: url的编码格式
	'''

	result = ""
	url = url.encode(encoding)
	#inFileName = inFileName.encode('gb2312')   #以win10系统编码格式编码文件名
	try :
		if inFileName == None :
			raise ValueError  #入参异常
		else :
			result = urllib.urlretrieve( url, inFileName)
			result = result[0] #获取文件名
	except IOError : #IO错误
		pass
	except socket.error : #网络错误
		pass
	return result


def main():

	try:
		urllib.urlretrieve(gLxfPythonUrl, 'lxf.html')
	except:
		exit(1)
		pass
	if not os.path.exists("./LxfPython/"):
		os.makedirs("./LxfPython")

	with open("./lxf.html", "r") as inFile: #代开lxf.html文件

		#获取 url 和 url名
		retLinkDict = DealHtml(inFile)

		iCount = 1
		for linkName , link in retLinkDict.items():

			#html文件的文件名要为系统编码格式, 此处是gb2312
			linkName = linkName.encode('gb2312') #从Unicode编码转到gb2312

			#下载url所指指向的html文件
			GetHtmlByUrl(url=gLxfUrlRoot+link, inFileName='LxfPython\{0}.{1}.html'.format(iCount, linkName))

			#打印下载完成的html文件
			#print(">>{0}.html --> OK!".format(linkName.encode('utf-8'))) 
			print(">>{0}.{1}.html --> OK!".format(iCount, linkName.decode('gb2312').encode('utf-8')))

			iCount += 1


	pass


if __name__ == '__main__':

	main()

