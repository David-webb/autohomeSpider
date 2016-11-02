# -*- coding:utf8 -*-

import os

def rename(dirpath):
    path = dirpath
    filelist = os.listdir(path)                     # 该文件夹下所有的文件（包括文件夹）
    try:  # (第二次改名的话,一定要排序，因为os.listdir生成的元素是随机的，第二次改名(os.rename函数)会将第一生成的同名文件覆盖，导致总文件数目变少)
        filelist.sort(key=lambda x: int(x[:-4]))
        print "文件有序"
        return True
    except:
        print "第一次排序"

    for count, files in enumerate(filelist, 1):     # 遍历所有文件
        Olddir = os.path.join(path, files)          # 原来的文件路径
        if os.path.isdir(Olddir):                   # 如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0]       # 文件名
        filetype = os.path.splitext(files)[1]       # 文件扩展名
        Newdir = os.path.join(path, ("%09d" % count) + filetype)   # 新的文件路径
        os.rename(Olddir, Newdir)                   # 重命名
    return True

if __name__ == "__main__":
    for i in os.listdir('./image/car'):
        # print i
        tmpdir = os.path.join("./image/car/", i)
        if not os.path.isdir(tmpdir):  # 如果是文件则跳过
            continue
        rename(tmpdir)
