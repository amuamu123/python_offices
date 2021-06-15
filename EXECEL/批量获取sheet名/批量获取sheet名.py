import pandas
import os

def get_filename(filepath):
    newpathame = (os.path.split(filepath)[1])+'.csv' #将完整的filepath中的文件夹名提取，作为储存文件的名称
    for files in os.listdir(filepath):
        files = filepath +'\\'+ files
        get_sheetname(newpathame,files) #传参

def get_sheetname(newpathame,files):
    sheetname = pandas.read_excel(files, None)  #获取sheet名，此时的sheet名为字典
    sheetname = list(sheetname.keys())  #转换为列表
    sheetname = (','+files+'\n').join(sheetname)+','+files+'\n' #转换为str的过程中追加下Excel的名称
    write_sheetname(newpathame,sheetname)
    print(sheetname)

def write_sheetname(flie,name):
    f = open(flie,'a',encoding='utf-8') #写入CSV，一般不会乱码，乱的话修改下encoding
    f.write(name)
    f.close() 

def main(): 
    while True:
        filepath = input('请输入您要读取的文件夹路径') 
        folder = os.path.exists(filepath)
        if (not folder):
            print('未找到文件夹，请重新输入')
        else :
            print('开始读取-------\n')
            break
    get_filename(filepath)  #传参

if __name__ == '__main__':
    main()
    print('读取完毕')