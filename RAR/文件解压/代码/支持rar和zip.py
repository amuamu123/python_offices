import difflib
import os
import winreg
import shutil
from unrar import rarfile  #解压rar
import zipfile  #解压zip

def take_second(elem):# 获取列表的第二个元素
    return elem[1]

def all_path(dir_path, dir_name):# 获取指定路径下所有的文件，并过筛选相应文件
    file_filter = [".pdf", ".docx"]# 设置过滤后的文件类型 当然可以设置多个类型
    result = [] # maindir(当前主目录)   subdir(当前主目录下的所有目录)  file_name_list(当前主目录下的所有文件)
    for maindir, subdir, file_name_list in os.walk(dir_path):
        for filename in file_name_list:
            com_path = os.path.join(maindir, filename)# 合并成一个完整路径
            ext = os.path.splitext(com_path)[1]# 获取文件后缀 [0]获取的是除了文件名以外的内容
            if ext in file_filter:# 过滤文件
                num = difflib.SequenceMatcher(None, filename, dir_name).quick_ratio()# 比较该文件与压缩文件名相似度
                result.append([com_path, num])
    result.sort(key=take_second, reverse=True)# 获取相似度最高的数据
    if len(result) != 0:
        result = result[0]
    return result

def do_unrar(path,temp_out_path):# 获取文件路径
    dir_path = os.path.dirname(path)# 获取文件名称
    dir_name = os.path.basename(path)
    try:
        rarfile.RarFile(path).extractall(temp_out_path)# 进行解压操作
        print('解压成功')
        #file_list = all_path(temp_out_path, dir_name)# 进行解压文件过滤操作
        #if len(file_list) != 0:  # 将最终文件移至当前文件夹
        #    return shutil.copy(file_list[0], dir_path)
        #return None
    except Exception as e:
        print('解压失败：{0}'.format(e),end='')
    #finally:
        #shutil.rmtrepie(temp_out_path)        # 删除文件

def do_unzip(path,temp_out_path):  #解压zip代码
    try:
        outfilesname = zipfile.ZipFile(path,mode='r')
        print(outfilesname.namelist())
        outfilesname.extractall(temp_out_path)#默认解压到当前文件夹
        outfilesname.close()
        print('解压成功')
    except Exception as e:
        print('解压失败：{0}'.format(e),end='')

if __name__ == '__main__':
    Desktoppath = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'), "Desktop")[0]#获取电脑系统桌面路径
    nowpath = os.path.dirname(os.path.realpath(__file__)) #获取当前代码路径
    res = input('文件路径(保持解压文件和程序文件/解压密码包在同个盘内):')
    temp_out_path = Desktoppath #解压路径为 桌面
    #do_unrar(res)   #解压rar则取消此注释
    #do_unzip(res)     #解压zip则取消此注释[zip默认只支持utf-8解码,解压GBK会乱码]