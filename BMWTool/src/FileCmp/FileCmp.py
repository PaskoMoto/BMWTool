#!coding:utf8

'''
Date:2018/1/30/15:43
Author:yqq
Description:  文件实时对比
'''

import os
import sys
import time


def main():

	filePath1 = "../../txt/tmp1.txt"
	filePath2 = "../../txt/tmp2.txt"

	while True:

		file1 = open(filePath1, "r")
		file2 = open(filePath2, "r")

		time.sleep(2)

		print("...")


		file1.close()
		file2.close()


	pass


if __name__ == "__main__":

	main()

	pass