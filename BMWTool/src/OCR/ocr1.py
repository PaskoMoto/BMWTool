#!coding:utf8

'''
Date:2018/1/30/17:28
Author:yqq
Description: 百度 图像文字识别 demo
'''


from aip import AipOcr
import json

# 定义常量
def MyOCR(filePath):

	APP_ID = '9851066'
	API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk'
	SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV'

	options = {
	 	'detect_direction': 'true',
	 	#'language_type': 'CHN_ENG',
	 	'language_type': 'ENG',
	 }

	# 初始化AipFace对象
	aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

	# 用二进制方式读取图片
	with open(filePath, 'rb') as fp:
		#调用通用文字识别接口
		result = aipOcr.basicGeneral(fp.read() , options)
		#result = aipOcr.enhancedGeneral(fp.read(), options)
		#result = aipOcr.basicAccurate(fp.read(), options)

		# print(result)
		# print(len(result['words_result']))

		for i in range(len(result['words_result'])):
			print(result['words_result'][i][u'words'])

		# print(json.dumps(result).decode("unicode-escape"))
		# print(type(json.dumps(result)))


def main():

	MyOCR(u'../../txt/cfg1.jpg')

	pass


if __name__ == "__main__":

	main()

	pass


