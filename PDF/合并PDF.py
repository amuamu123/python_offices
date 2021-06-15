import os
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger


def auto_input():
    result_name = input('\n请输入合并后的文件名')
    result_pdf= PdfFileMerger()
    for pdf in os.listdir(path):
        with open (pdf,'rb') as fp:
            pdf_reder = PdfFileReder(fp)
            if pdf_reder.isEncrypted:
                print(f'忽略加密文件：{pdf}')
                continue
            result_pdf.append(pdf_reader,import_bookmarks = True)

    result_pdf.write(result_name+'.pdf')
    result_pdf.close()

if __name__ == '__main__' :
    print('请把程序放在同一个文件夹')

    while True :
        path = input('\n请输入文件保存的路径：')
        os.chdir(str(path))
        choice = int(input('\n1.手动2.自动'))

        if choice == 1:
            manual_input()
        else:
            auto_input()

        print('\n合并完成')
        go = int(input('\n是否继续使用1/2'))
        if go == 1:
            continue
        else:
            break

    print('over')