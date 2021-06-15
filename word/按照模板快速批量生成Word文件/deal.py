import xlrd
from docx import Document
import re


def read_excel(path):
    """
    读取Excel中的信息
    :param path: Excel文件路径
    :return: Excel中的信息
    """
    # 打开execl
    workbook = xlrd.open_workbook(path)
    # 根据sheet索引或者名称获取sheet内容
    data_sheet = workbook.sheets()[0]
    row_num = data_sheet.nrows  # sheet行数
    col_num = data_sheet.ncols  # sheet列数
    list = []
    for i in range(1, row_num):
        rowlist = []
        for j in range(col_num):
            if j == 1:
                date_value = xlrd.xldate_as_tuple(data_sheet.cell_value(i, j), workbook.datemode)
                rowlist.append(date_value[0:3])
            else:
                rowlist.append(data_sheet.cell_value(i, j))
        list.append(rowlist)
    # 输出所有单元格的内容
    return list


def rs_word(info_list):
    """
    通过Excel中的信息替换word文档中的信息并批量生成新的文档
    :param info_list: Excel信息
    :return:
    """
    
    for info in info_list:
        document = Document('产品价格通知函.docx')  # 打开文件demo.docx
        paragraphs = document.paragraphs
        text = paragraphs[0].text
        year = str(info[1][0])
        month = str(info[1][1])
        day = str(info[1][2])
        text = year + text[2] + month + text[5] + day + text[8:]
        paragraphs[0].text = text
        name = info[0]
        text = paragraphs[2].text[:3]+name+paragraphs[2].text[-1]
        paragraphs[2].text = text
        price = info[2][0:3]
        text = re.sub('xx', price,paragraphs[4].text)
        paragraphs[4].text = text
        file_name = info[0] + str(info[1][0]) + "年" + str(info[1][1]) + "月" +str( info[1][2]) + "日" + '.docx'
        print("已经保存"+file_name)
        print()
        document.save('word/'+file_name)  # 保存文档


def start():
    """
    开始执行
    :return:∫
    """
    info_list = read_excel('客户单价通知.xlsx')
    # print(info_list[:1])
    rs_word(info_list)


if __name__ == "__main__":
    start()