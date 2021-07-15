from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger

def get_reader(filename, password):
    try:
        old_file = open('新建文件夹\云彩收集者手册.pdf', 'rb')
    except IOError as err:
        print('文件打开失败！' + str(err))
        return None
    
    pdf_reader = PdfFileReader(old_file, strict=False)# 创建读实例
    # 解密操作
    if pdf_reader.isEncrypted:
        if password is None:
            print('%s文件被加密，需要密码！' % filename)
            return None
        else:
            if pdf_reader.decrypt(password) != 1:
                print('%s密码不正确！' % filename)
                return None
    if old_file in locals():
        old_file.close()
    return pdf_reader
def encrypt_pdf(filename, new_password, old_password=None, encrypted_filename=None):
    """对filename所对应的文件进行加密,并生成一个新的文件
    :param filename: 文件对应的路径
    :param new_password: 对文件加密使用的密码
    :param old_password: 如果旧文件进行了加密，需要密码
    :param encrypted_filename: 加密之后的文件名，省却时使用filename_encrypted;
    :return:""" 
    
    pdf_reader = get_reader(filename, old_password)# 创建一个Reader实例
    if pdf_reader is None:
        return
    pdf_writer = PdfFileWriter()# 创建一个写操作的实例
    pdf_writer.appendPagesFromReader(pdf_reader)# 从之前Reader中将数据写入到Writer中
    pdf_writer.encrypt(new_password)# 重新使用新密码加密
    if encrypted_filename is None:
        encrypted_filename = "".join(filename.split('.')[:-1]) + '_' + 'encrypted' + '.pdf'# 使用旧文件名 + encrypted 作为新的文件名
    pdf_writer.write(open(encrypted_filename, 'wb'))

def decrypt_pdf(filename, password, decrypted_filename=None):
    """将加密的文件及逆行解密，并生成一个无需密码pdf文件
    :param filename: 原先加密的pdf文件
    :param password: 对应的密码
    :param decrypted_filename: 解密之后的文件名
    :return:"""
    pdf_reader = get_reader(filename, password) # 生成一个Reader和Writer
    if pdf_reader is None:
        return
    if not pdf_reader.isEncrypted:
        print('文件没有被加密，无需操作！')
        return
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(pdf_reader)
    if decrypted_filename is None:
        decrypted_filename = "".join(filename.split('.')[:-1]) + '_' + 'decrypted' + '.pdf'
    pdf_writer.write(open(decrypted_filename, 'wb'))# 写入新文件

def split_by_pages(filename, pages, password=None):
    """将文件按照页数进行平均分割
    :param filename: 所要分割的文件名
    :param pages: 分割之后每个文件对应的页数
    :param password: 如果文件加密，需要进行解密操作
    :return: """
    pdf_reader = get_reader(filename, password)# 得到Reader
    if pdf_reader is None:
        return
    pages_nums = pdf_reader.numPages# 得到总的页数
    if pages <= 1:
        print('每份文件必须大于1页！')
        return
    pdf_num = pages_nums // pages + 1 if pages_nums % pages else int(pages_nums / pages)# 得到切分之后每个pdf文件的页数
    print('pdf文件被分为%d份，每份有%d页！' % (pdf_num, pages))
    for cur_pdf_num in range(1, pdf_num + 1):# 依次生成pdf文件
        pdf_writer = PdfFileWriter() # 创建一个新的写实例
        split_pdf_name = "".join(filename)[:-1] + '_' + str(cur_pdf_num) + '.pdf' # 生成对应的文件名称
        start = pages * (cur_pdf_num - 1) # 计算出当前开始的位置
        end = pages * cur_pdf_num if cur_pdf_num != pdf_num else pages_nums# 计算出结束的位置，如果是最后一份就直接返回最后的页数，否则用每份页数*已经分好的文件数
        # print(str(start) + ',' + str(end))
        for i in range(start, end):# 依次读取对应的页数
            pdf_writer.addPage(pdf_reader.getPage(i))
        pdf_writer.write(open(split_pdf_name, 'wb')) # 写入文件

def split_by_num(filename, nums, password=None):
    """将pdf文件分为nums份
    :param filename: 文件名
    :param nums: 要分成的份数
    :param password: 如果需要解密，输入密码
    :return: """
    pdf_reader = get_reader(filename, password)
    if not pdf_reader:
        return
    if nums < 2:
        print('份数不能小于2！')
        return
    pages = pdf_reader.numPages# 得到pdf的总页数
    if pages < nums:
        print('份数不应该大于pdf总页数！')
        return
    each_pdf = pages // nums# 计算每份应该有多少页
    print('pdf共有%d页，分为%d份，每份有%d页！' % (pages, nums,each_pdf))

    for num in range(1, nums + 1):
        pdf_writer = PdfFileWriter() # 生成对应的文件名称
        split_pdf_name = "".join(filename)[:-1] + '_' + str(num) + '.pdf'# 计算出当前开始的位置
        start = each_pdf * (num - 1)# 计算出结束的位置，如果是最后一份就直接返回最后的页数，否则用每份页数*已经分好的文件数
        end = each_pdf * num if num != nums else pages
        print(str(start) + ',' + str(end))
        for i in range(start, end):
            pdf_writer.addPage(pdf_reader.getPage(i))
        pdf_writer.write(open(split_pdf_name, 'wb'))

def merger_pdf(filenames, merged_name, passwords=None):   
    """传进来一个文件列表，将其依次融合起来
    :param filenames: 文件列表
    :param passwords: 对应的密码列表
    :return:"""
    filenums = len(filenames)# 计算共有多少文件
    pdf_merger = PdfFileMerger(False)# 注意需要使用False 参数
    for i in range(filenums):
        if passwords is None:# 得到密码
            password = None
        else:
            password = passwords[i]
        pdf_reader = get_reader(filenames[i], password)
        if not pdf_reader:
            return
        pdf_merger.append(pdf_reader)# append默认添加到最后
    pdf_merger.write(open(merged_name, 'wb'))

def insert_pdf(pdf1, pdf2, insert_num, merged_name, password1=None, password2=None):
    """将pdf2全部文件插入到pdf1中第insert_num页
    :param pdf1: pdf1文件名称
    :param pdf2: pdf2文件名称
    :param insert_num: 插入的页数
    :param merged_name: 融合后的文件名称
    :param password1: pdf1对应的密码
    :param password2: pdf2对应的密码
    :return: """
    pdf1_reader = get_reader(pdf1, password1)
    pdf2_reader = get_reader(pdf2, password2)
    if not pdf1_reader or not pdf2_reader:# 如果有一个打不开就返回
        return
    pdf1_pages = pdf1_reader.numPages# 得到pdf1的总页数
    if insert_num < 0 or insert_num > pdf1_pages:
        print('插入位置异常，想要插入的页数为：%d，pdf1文件共有：%d页！' % (insert_num, pdf1_pages))
        return
    m_pdf = PdfFileMerger(False)# 注意需要使用False参数，可能会出现中文乱码的情况
    m_pdf.append(pdf1)
    m_pdf.merge(insert_num, pdf2)
    m_pdf.write(open(merged_name, 'wb'))
if __name__ == '__main__':
    # encrypt_pdf('ex1.pdf', 'leafage')
    # decrypt_pdf('ex1123_encrypted.pdf', 'leafage')
    # split_by_pages('ex1.pdf', 5)
    split_by_num('新建文件夹\云彩收集者手册.pdf',80)
    # merger_pdf(['ex1.pdf', 'ex2.pdf'], 'merger.pdf')
    # insert_pdf('ex1.pdf', 'ex2.pdf', 10, 'pdf12.pdf')