#!coding:utf-8
import urllib
import socket
# 获取网页html，拿"下厨房"这个网站来示例
html = urllib.urlretrieve(r'https://item.jd.com/10956720807.html#none')

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

	print(html)




	pass


if __name__ == "__main__":

	main()

	pass