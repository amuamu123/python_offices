import os
from PyPDF2 import PdfFileReader,PdfFileMerger
def auto_input():
    result_pdf= PdfFileMerger() #新建实例对象
    for pdf in os.listdir(path):  #遍历文件夹
        with open (pdf,'rb') as fp:  # 打开要合并的子PDF
            pdf_reder = PdfFileReader(fp)  #读取PDF内容
            if pdf_reder.isEncrypted:   # 判断是否被加密
                print(f'忽略加密文件：{pdf}')  # 如果加密则跳过，并打印忽略加密文件
                continue
            result_pdf.append(pdf_reder,import_bookmarks = True) # 将刚刚读取到的PDF内容追加到实例对象内

    result_pdf.write(result_name) # 写入保存
    result_pdf.close()    # 关闭程序

if __name__ == '__main__' :
    path = input('\n请输入文件保存的文件夹路径：')
    result_name = input('\n请输入合并后的文件名')+'.pdf'
    os.chdir(str(path))  #切换路径
    auto_input()
    print('\n合并完成')