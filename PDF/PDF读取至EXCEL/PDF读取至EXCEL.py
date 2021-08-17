import os, sys
import re
import time
import xlsxwriter
import logging
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)
'''
pip install XlsxWriter  
pip install pdfminer3k
'''
# 读取文件夹中所有pdf文档
def pdf_parser(input_path):
    with open(input_path, 'rb') as fd:
        parse = PDFParser(fd)
        doc = PDFDocument()
        parse.set_document(doc)
        doc.set_parser(parse)
        doc.initialize('')
        resmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(resmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(resmgr, device)
        extracted_text = ''


    for page in doc.get_pages():
        interpreter.process_page(page)
        layouts = device.get_result()
        for layout in layouts:
            if isinstance(layout, LTTextBox) or isinstance(layout, LTTextLine):
                extracted_text += layout.get_text()
    return extracted_text

# 匹配有用的信息写入字典当中
def extracted_info(extracted_text, name):
    tmp_list = []
    t_list = extracted_text.split("\n")
    total_text = t_list[6]
    count = re.findall('\d+', total_text)[0]
    total = re.findall("\d+\.\d+", total_text)[0]

    tt = re.findall("(\d{2})-(\d{2}) (\d{2}):(\d{2}) ([\u4e00-\u9fa5]{2})", extracted_text) # 行车时间
    dd = re.findall("深圳市\\n(.*)\\n", extracted_text)  # 行车起点
    fare = re.findall("(\d{2}\\.\d{2})", extracted_text) # 车费
    for i, lst in enumerate(tt):
        tmp_dict = {}
        tmp_dict["行程人"] = name
        tmp_dict["上车时间"] = format_time(time_text=tt[i])
        tmp_dict["上车地点"] = dd[i]
        tmp_dict["车费"] = fare[i+1]
        tmp_list.append(tmp_dict)
    return tmp_list, count, total

# 设置好表格格式后将字典的数据写入到Excel当中
def dict_to_excel(output_path, pdffilename_list, header):
    excel_init_file = xlsxwriter.Workbook(output_path)
    table = excel_init_file.add_worksheet('sheet1')
    title_format = excel_init_file.add_format({'bold': True, 'border': 2, 'bg_color': '#595959', 'font_color': 'white', 'font_size': 12, 'font':'黑体', 'align': 'center', 'valign': 'vcenter'})
    cell_format = excel_init_file.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    table.set_default_row(40)

    for i, j in enumerate(header):
        table.set_column(i, i, 30)
        table.write_string(0, i, j, title_format)

    last_idx = 0
    for i, pdf in enumerate(pdffilename_list):
        sys.stdout.write("\r")
        sys.stdout.write("正在识别：{}\n".format(pdf))
        # sys.stdout.write("%s [%-25s] %d%%" % ("生成Excel表格: ", '#' * ((i+1) * 25 // len(pdffilename_list)), (i+1) / len(pdffilename_list) * 100))
        sys.stdout.flush()
        time.sleep(0.5)
        name = re.findall(r'- (.*).pdf$', pdf)[0].strip() # 行程人姓名
        text = pdf_parser(pdf)
        dict_list, count, total = extracted_info(text, name)
        for index, dict_content in enumerate(dict_list):
            for i in range(len(header) - 1):
                table.write_string(last_idx+index+1, i, dict_content[header[i]], cell_format)

        if int(count) != 1:
            table.merge_range('E{}:E{}'.format(str(last_idx+2), str(last_idx+2+int(count)-1)), 'Merged Range', cell_format)
            table.merge_range('A{}:A{}'.format(str(last_idx+2), str(last_idx+2+int(count)-1)), 'Mergerd Range', cell_format)
        table.write_string(last_idx+1, 0, name, cell_format)
        table.write_string(last_idx+1, 4, total, cell_format)
        last_idx += int(count)
    excel_init_file.close()

# 格式化乘车日期
def format_time(time_text):
    tt = list(time_text)
    tt.insert(1, '-')
    tt.insert(3, ' ')
    tt.insert(5, ':')
    tt.insert(7, ' ')
    return ''.join(tt)

#设置循环，获取路径下的pdf文件 
def get_all_pdf(path):
    return [f for f in os.listdir(path) if os.path.isfile(f) and f.endswith('.pdf')]

# 设置执行语句，开始进行转换
if __name__ == '__main__':
    pdffilename_list = get_all_pdf('.')
    output_xlsx = '风变员工3月行程单.xlsx'
    header = ["行程人", "上车时间", "上车地点", "车费", "合计"]
    print("开始识别PDF...")
    dict_to_excel(output_xlsx, pdffilename_list, header)
    print("\n转换完成！！")