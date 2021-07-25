raw_headers = """
        lossless: 0
        flag_qc: 0
        p: 2
        n: 10
        w: 周杰伦
        g_tk_new_20200303: 5381
        g_tk: 5381
        loginUin: 0
        hostUin: 0
        format: json
        inCharset: utf8
        outCharset: utf-8
        notice: 0
        platform: yqq.json
        needNewCode: 0
"""
#headers = dict([line.split(": ",1) for line in raw_headers.split("\n")])
def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    header_raw = header_raw.strip()  # 处理可能的空字符3
    header_raw = header_raw.split("\n")  # 分割每行
    header_raw = [line.split(":", 1) for line in header_raw]  # 分割冒号
    header_raw = dict((k.strip(), v.strip()) for k, v in header_raw)  # 处理可能的空字符
    return header_raw

print(get_headers(raw_headers))
