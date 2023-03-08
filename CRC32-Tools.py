# -*- coding: utf-8 -*-
import zipfile
import argparse
import string
import binascii
import itertools


def FileRead(zipname):
    try:
        f = open(zipname)  # 打开目标文件
        f.close()
    except FileNotFoundError:
        print("未找到同目录下的压缩包文件" + zipname)  # 如果未找到文件，输出错误
        return  # 退出线程，进行详细报错
    except PermissionError:
        print("无法读取目标压缩包（无权限访问）")  # 如果发现目标文件无权限，输出错误
        return  # 退出线程，进行详细报错


def ReadCRC(zipname):
    zip_url = "./" + zipname
    file_zip = zipfile.ZipFile(zip_url)  # 用zipfile读取指定的压缩包文件
    name_list = file_zip.namelist()  # 使用一个列表，获取并存储压缩包内所有的文件名
    crc_list = []
    print('+--------------遍历指定压缩包的CRC值----------------+')
    for name in name_list:
        name_message = file_zip.getinfo(name)
        crc_list.append(hex(name_message.CRC))
        print('[OK] {0}: {1}'.format(name, hex(name_message.CRC)))
    print('+---------------------------------------------------+')
    crc32_list = str(crc_list)
    crc32_list = crc32_list.replace('\'', '')
    print("读取成功，导出CRC列表为:" + crc32_list)  # 导出CRC列表后，导入其他脚本进行CRC碰撞


def crc(zipname, byte):
    zip_url = "./" + zipname
    file_zip = zipfile.ZipFile(zip_url)  # 用zipfile读取指定的压缩包文件
    name_list = file_zip.namelist()  # 使用一个列表，获取并存储压缩包内所有的文件名
    crc_list = []
    crc32_list = []
    print('+--------------遍历指定压缩包的CRC值----------------+')
    for name in name_list:
        name_message = file_zip.getinfo(name)
        crc_list.append(name_message.CRC)
        crc32_list.append(hex(name_message.CRC))
        print('[OK] {0}: {1}'.format(name, hex(name_message.CRC)))
    print('+-------------对输出的CRC值进行碰撞-----------------+')
    comment = ''
    chars = string.printable
    for crc_value in crc_list:
        for char in itertools.product(chars, repeat=byte):  # 获取任意Byte字符
            char = ''.join(char)
            thicken_crc = binascii.crc32(char.encode())  # 获取CRC32值
            calc_crc = thicken_crc & 0xffffffff  # 将任意Byte字符串的CRC32值与0xffffffff进行与运算
            if calc_crc == crc_value:  # 匹配两个CRC32值
                print(f'[Success] {hex(crc_value)}: {char}')
                comment += char
    print('+-----------------CRC碰撞结束!!!-----------------+')
    crc32_list = str(crc32_list)
    crc32_list = crc32_list.replace('\'', '')
    print("读取成功，导出CRC列表为:" + crc32_list)  # 导出CRC列表
    if comment:
        print(f'CRC碰撞成功，结果为: {comment}')  # 输出CRC碰撞结果
    else:
        print(f'CRC碰撞没有结果，请检查压缩包内文件是否为{byte}Byte!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CRC-Tools V2.2 原链接https://github.com/AabyssZG/CRC32-Tools，由https://github.com/basket-ball改进代码')
    #parser = argparse.ArgumentParser(prog="CRC32-Tools", usage="开源项目[%(prog)s] 实现了如下功能:")
    parser.add_argument('readzip', action='store', help='读取对应压缩包')
    parser.add_argument('-b', '--byte', action='store', dest='byte',
                        type=int, help='对输入大小Byte的压缩包自动进行CRC碰撞并输出文件内容')
    args = parser.parse_args()
    try:
        if args.byte:
            FileRead(args.readzip)
            crc(args.readzip, args.byte)
    except BaseException as e:
        err = str(e)
        print('脚本详细报错:' + err)
