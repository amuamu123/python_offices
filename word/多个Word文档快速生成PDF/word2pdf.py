from win32com.client import Dispatch # pip install pywin32
from os import walk
import os

wdFormatPDF = 17  # win32提供了多种word转换为其他文件的接口，其中FileFormat=17是转换为pdf


def doc2pdf(input_file, input_file_name, output_dir):
    try:
        word = Dispatch('Word.Application')
        doc = word.Documents.Open(input_file)
    except Exception as e:
        print("word无法打开, 发生如下错误:\n{}".format(e))
    try:
        pdf_file_name = input_file_name.replace(".docx", ".pdf").replace(".doc", ".pdf")
        pdf_file = os.path.join(output_dir, pdf_file_name)
        doc.SaveAs(pdf_file, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()
        print("成功转换\"{}\"".format(input_file_name))
        print()
    except Exception as e:
        print("文件保存失败, 发生如下错误:\n{}".format(e))


if __name__ == "__main__":
    doc_files = []
    directory = "D://个人资料//Python//13各类工具//多个Word文档快速生成PDF//word" # word文件夹必须使用绝对路径
    output_dir = "D://个人资料//Python//13各类工具//多个Word文档快速生成PDF//pdf" # pdf文件夹必须使用绝对路径
    for root, _, filenames in walk(directory):  # 第二个返回值是dirs， 用不上使用_占位
        for file in filenames:
            if file.endswith(".doc") or file.endswith(".docx"):
                print("转换{}中......".format(file))
                doc2pdf(os.path.join(root, file), file, output_dir)
