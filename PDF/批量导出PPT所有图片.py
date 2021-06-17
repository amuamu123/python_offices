import os
import win32com.client


class PowerpointHandler(object):
    def __init__(self):
        self.powerpoint = win32com.client.Dispatch('PowerPoint.Application')
        self.cur_path = os.getcwd()

    def conv_to_jpg(self, path, file):
        ppt_format_jpg = 17
        ppt = self.powerpoint.Presentations.Open(path)
        ppt.SaveAs(file.rsplit(".")[0]+".jpg", ppt_format_jpg)
        ppt.Close()
        print("ppt文件{}已转换成功".format(file, self.cur_path))

    def quit(self):
        self.powerpoint.Quit()


if __name__ == '__main__':
    WORK_DIR = r"C:\Users\user\Desktop\ppt_handler\PPT"
    ppt_files = os.listdir(WORK_DIR)
    powerpoint_handler = PowerpointHandler()
    powerpoint_handler.powerpoint.Visible = True
    for ppt_file in ppt_files:
        if ppt_file.endswith((".ppt", ".pptx")):
            ppt_file_path = os.path.join(WORK_DIR, ppt_file)
            powerpoint_handler.conv_to_jpg(ppt_file_path, ppt_file)
    powerpoint_handler.quit()