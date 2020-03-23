import os
import sys
import re
import chardet


#扫描文件夹下面所有的文件，并保存在文件目录备份表中

path='./newsSpider/data/'
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):         # 如果是文件则添加进 fileList
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):   # 如果是文件夹
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

output = sys.stdout
outputfile = open('path.txt', 'w')
sys.stdout = outputfile
list = GetFileList(path, []) # 获取所有myFolder文件夹下所有文件名称（包含拓展名）
# 输出所有文件夹中的路径（相对于当前运行的.py文件的相对路径）
for route in list:
    # route 为路径
    print(route)
# 关闭输出重定向
outputfile.close()
sys.stdout = output
