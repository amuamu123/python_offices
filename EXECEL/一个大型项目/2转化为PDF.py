import os
import winreg
from pathlib import Path
from PyPDF2 import PdfFileReader,PdfFileMerger

# 万物转换PDF方法
from win32com.client import Dispatch, constants, gencache, DispatchEx
class PDFConverter:
    def __init__(self, pathname, export='.'):
        self._handle_postfix = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx']
        self._filename_list = list()
        self._export_folder = os.path.join(os.path.abspath('.'), DesktopPDFpath)
        if not os.path.exists(self._export_folder):
                os.mkdir(self._export_folder)
        self._enumerate_filename(pathname)
    
    def _enumerate_filename(self, pathname):
        full_pathname = os.path.abspath(pathname)
        if os.path.isfile(full_pathname):
            if self._is_legal_postfix(full_pathname):
                self._filename_list.append(full_pathname)
            else:
                raise TypeError('文件 {} 后缀名不合法！仅支持如下文件类型：{}。'.format(pathname, '、'.join(self._handle_postfix)))
        elif os.path.isdir(full_pathname):
            for relpath, _, files in os.walk(full_pathname):
                for name in files:
                    filename = os.path.join(full_pathname, relpath, name)
                    if self._is_legal_postfix(filename):
                        self._filename_list.append(os.path.join(filename))
        else:
            raise TypeError('文件/文件夹 {} 不存在或不合法！'.format(pathname))

    def _is_legal_postfix(self, filename):
        return filename.split('.')[-1].lower() in self._handle_postfix and not os.path.basename(filename).startswith('~')
    
    def run_conver(self):
        '''
        进行批量处理，根据后缀名调用函数执行转换
        '''
        print('需要转换的文件数：', len(self._filename_list))
        for filename in self._filename_list:
            postfix = filename.split('.')[-1].lower()
            funcCall = getattr(self, postfix)
            print('原文件：', filename)
            funcCall(filename)
        print('转换完成！')
    
    def doc(self, filename):
        '''
        doc 和 docx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        print('保存 PDF 文件：', exportfile)
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
        w = Dispatch("Word.Application")
        doc = w.Documents.Open(filename)
        doc.ExportAsFixedFormat(exportfile, constants.wdExportFormatPDF,
                Item=constants.wdExportDocumentWithMarkup,
                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        
        w.Quit(constants.wdDoNotSaveChanges)
    
    def docx(self, filename):
        self.doc(filename)
    
    def xls(self, filename):
        '''
        xls 和 xlsx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        xlApp = DispatchEx("Excel.Application")
        xlApp.Visible = False    
        xlApp.DisplayAlerts = 0   
        books = xlApp.Workbooks.Open(filename,False)
        books.ExportAsFixedFormat(0, exportfile)
        books.Close(False)
        print('保存 PDF 文件：', exportfile)
        xlApp.Quit()
    
    def xlsx(self, filename):
        self.xls(filename)
    
    def ppt(self, filename):
        '''
        ppt 和 pptx 文件转换
        '''
        name = os.path.basename(filename).split('.')[0] + '.pdf'
        exportfile = os.path.join(self._export_folder, name)
        gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
        p = Dispatch("PowerPoint.Application")
        ppt = p.Presentations.Open(filename, False, False, False)
        ppt.ExportAsFixedFormat(exportfile, 2, PrintRange=None)
        print('保存 PDF 文件：', exportfile)
        p.Quit()
    def pptx(self, filename):
        self.ppt(filename)


def 转化(Desktoppath):
    folder = Desktoppath #这里输入 需要转化的文件路径
    my_file = Path(folder)
    if  my_file.is_dir(): #判断是否为文件夹
        pathname = os.path.join(os.path.abspath('.'), folder)
    else:
        pathname = Desktoppath#单个文件的转换
    pdfConverter = PDFConverter(pathname)
    pdfConverter.run_conver()

def auto_input(): #合并PDF为一份
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

if __name__ == "__main__":
    Desktoppath = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'), "Desktop")[0]#获取电脑系统桌面路径
    try:
        os.makedirs(Desktoppath+"\\考场汇总") #创建一个文件夹
    except:
        pass
    DesktopPDFpath = Desktoppath + '\\用Python生成PDF'
    path = input('输入你要转化的文件路径')
    转化(path)

    path = input('\n请输入文件保存的文件夹路径：')
    result_name = input('\n请输入合并后的文件名')+'.pdf'
    os.chdir(str(path))  #切换路径
    auto_input()
    print('\n合并完成')