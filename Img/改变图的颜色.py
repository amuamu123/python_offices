# encoding: utf-8
from PIL import Image
from imageio import imread

def get_wordcloud(path):
    logo_path = 'logo.png'  # logo地址
    img = Image.open(logo_path)
    Img = img.convert('L')# 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    threshold = 195# 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    photo = Img.point(table, '1') # 图片二值化
    photo.save(logo_path)# 二值化logo地址