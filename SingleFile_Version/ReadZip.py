#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import zipfile

def title():
    print('+-----------------------------------------------------+')
    print('+              渊龙Sec安全团队CTF工具包               +')
    print('+              团队公开QQ群：877317946                +')
    print('+               Title: CRC-Tools_ReadZIP              +')
    print('+     python3 ReadZip.py --> ReadZip >>> Demo.zip     +')
    print('+                作者：曾哥（AabyssZG）               +')
    print('+                 版本：V1.3单文件版                  +')
    print('+-----------------------------------------------------+')

def FileRead(zipname):
    try:
    	f =open(zipname)                               #打开目标文件
    	f.close()
    except FileNotFoundError:
    	print ("未找到同目录下的压缩包文件" + zipname) #如果未找到文件，输出错误
    	return                                         #退出线程，进行详细报错
    except PermissionError:
    	print ("无法读取目标压缩包（无权限访问）")     #如果发现目标文件无权限，输出错误
    	return                                         #退出线程，进行详细报错

def ReadCRC(zipname):
    zip_url = "./" + zipname
    file_zip = zipfile.ZipFile(zip_url) #用zipfile读取指定的压缩包文件
    name_list = file_zip.namelist() #使用一个列表，获取并存储压缩包内所有的文件名
    crc_list = []
    print('+--------------遍历指定压缩包的CRC值----------------+')
    for name in name_list:
    	name_message = file_zip.getinfo(name)
    	crc_list.append(hex(name_message.CRC))
    	print('[OK] {0}: {1}'.format(name,hex(name_message.CRC)))
    print('+---------------------------------------------------+')
    crc32_list = str(crc_list)
    crc32_list = crc32_list.replace('\'' , '')
    print("读取成功，导出CRC列表为：" + crc32_list) #导出CRC列表后，导入其他脚本进行CRC碰撞

if __name__ == '__main__':
    title()
    zipname = str(input("请输入压缩包名字：\nReadZip >>> "))
    try:
        if zipname:
        	FileRead(zipname)
        	ReadCRC(zipname)
    except BaseException as e:
        err = str(e)
        print('脚本详细报错：' + err)
