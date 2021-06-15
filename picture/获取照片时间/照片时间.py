import os
import exifread

def getExif(path, filename):
    old_full_file_name = os.path.join(imgpath, filename)
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(old_full_file_name, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    #显示图片所有的exif信息
    # print("showing res of getExif: \n")
    # print(tags)
    # print("\n\n\n\n");
    if FIELD in tags:
        print("\nstr(tags[FIELD]): %s" %(str(tags[FIELD])))  # 获取到的结果格式类似为：2018:12:07 03:10:34
        print("\nstr(tags[FIELD]).replace(':', '').replace(' ', '_'): %s" %(str(tags[FIELD]).replace(':', '').replace(' ', '_'))) # 获取结果格式类似为：20181207_031034
        print("\nos.path.splitext(filename)[1]: %s" %(os.path.splitext(filename)[1]))  # 获取了图片的格式，结果类似为：.jpg
        new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
        print("\nnew_name: %s" %(new_name)) # 20181207_031034.jpg


        time = new_name.split(".")[0][:13]
        new_name2 = new_name.split(".")[0][:8] + '_' +filename
        print("\nfilename: %s" %filename)
        print("\n%s的拍摄时间是: %s年%s月%s日%s时%s分" %(filename,time[0:4],time[4:6],time[6:8],time[9:11],time[11:13]))
        
        # 可对图片进行重命名
        new_full_file_name = os.path.join(imgpath, new_name2)
        #print(old_full_file_name," ---> ", new_full_file_name)    
        # os.rename(old_full_file_name, new_full_file_name)
    else:
        print('No {} found'.format(FIELD),' in: ', old_full_file_name)
        
def getpath(imgpath):
    for filename in os.listdir(imgpath):
        # os.path.join用于路径拼接，将imgpath和filename连在一起得到完整的路径，后面的参数可有多个，从第一个以”/”开头的参数开始拼接
        full_file_name = os.path.join(imgpath, filename) 	    
        # os.path.isfile用于判断路径指向的是否为文件，相类似的os.path.isdir用于判断是否为文件夹
        if os.path.isfile(full_file_name):            
            getExif(imgpath, filename)
            print(full_file_name)

if __name__ == "__main__":
    global imgpath
    imgpath = input('输入需要读取的照片所在文件夹路径')
    getpath(imgpath)