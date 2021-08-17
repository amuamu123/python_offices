# encoding: utf-8
from imageio import imread
import skimage.io as io
import numpy as np

def merge_wordcloud(pics):
    path = '/www/server/mailserver'
    A_wordcould_path = path+'/wordcould1.png'
    B_wordcould_path = path+'/wordcould2.png'
    pic= path+'/wordcould.png'
    # print(jzg.shape)   #查看图片的大小
    # print(jzg.dtype)   #查看数组元素数据类型
    # print(lgz.shape)
    # print(lgz.dtype)
    jzg = io.imread(pics[0])   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    lgz = io.imread(pics[1])   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    pj1 = np.zeros((1080,1920+1920,3))   #横向拼接
    pj1[:,:1920,:] = jzg.copy()   #图片jzg在左
    pj1[:,1920:,:] = lgz.copy()   #图片lgz在右
    pj1=np.array(pj1,dtype=np.uint8)   #将pj1数组元素数据类型的改为"uint8"
    io.imsave(A_wordcould_path, pj1)   #保存拼接后的图片
    # 下面左右拼接
    jzg2 = io.imread(pics[2])   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    lgz2 = io.imread(pics[3])   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    pj2 = np.zeros((1080,1920+1920,3))   #横向拼接
    pj2[:,:1920,:] = jzg2.copy()   #图片jzg2在左
    pj2[:,1920:,:] = lgz2.copy()   #图片lgz2在右
    pj2=np.array(pj2,dtype=np.uint8)   #将pj2数组元素数据类型的改为"uint8"
    io.imsave(B_wordcould_path, pj2)   #保存拼接后的图片
    # 上面与下面拼接
    uzg = io.imread(A_wordcould_path)   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    dgz = io.imread(B_wordcould_path)   # np.ndarray, [h, w, c], 值域(0, 255), RGB
    pj = np.zeros((1080+1080,1920+1920,3))   #竖向拼接
    pj[:1080,:,:] = uzg.copy()   #图片jzg在左
    pj[1080:,:,:] = dgz.copy()   #图片lgz在右
    pj=np.array(pj,dtype=np.uint8)   #将pj数组元素数据类型的改为"uint8"
    io.imsave(pic, pj)   #保存拼接后的图片
    return pic