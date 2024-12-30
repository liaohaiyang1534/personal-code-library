# A simple GUI 
# for extracting dispersion curves from dispersion spectrum

import  tkinter
from matplotlib.backends.backend_tkagg import(
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib import pyplot as plt
from matplotlib.path import Path

import numpy as np
import h5py
import os
import yaml
import argparse
import shutil

import argparse

from PIL import ImageGrab

def find_closel(a,x):
    return int((a-x[0])/(x[1]-x[0]))

def find_closer(a,x):
    return int((a-x[0])/(x[1]-x[0]))+1

def inpolygon(xq, yq, xv, yv):
    """
    reimplement inpolygon in matlab
    :type xq: np.ndarray
    :type yq: np.ndarray
    :type xv: np.ndarray
    :type yv: np.ndarray
    """
    # 合并xv和yv为顶点数组
    vertices = np.vstack((xv, yv)).T
    # 定义Path对象
    path = Path(vertices)
    # 把xq和yq合并为test_points
    test_points = np.hstack([xq.reshape(xq.size, -1), yq.reshape(yq.size, -1)])
    # 得到一个test_points是否严格在path内的mask，是bool值数组
    _in = path.contains_points(test_points)
    # 得到一个test_points是否在path内部或者在路径上的mask
    _in_on = path.contains_points(test_points, radius=-1e-10)
    # 得到一个test_points是否在path路径上的mask
    _on = _in ^ _in_on

    return _in_on, _on

def get_yaml_data(filename):
    file = open(filename,'r',encoding='utf-8')
    file_data = file.read()
    file.close()
    data = yaml.load(file_data,Loader=yaml.FullLoader)
    return data

class DispersionCurve():
    # Class for saving dispersion curves of each dispersion spectrum
    def __init__(self):
        self.norders = 0
        self.dc = dict()
     
    
    def addorder(self,order):
        self.norders += 1
        self.dc[order] = dict()

    def add(self,order,x,y):
        # add dispersion curves for one order
        self.addorder(order)
        self.dc[order]['f'] = x
        self.dc[order]['c'] = y
    
class DispersionSpectrum():
    # simple GUI for extracting dispersion curves
    def __init__(self,f,c,data,outfile,infile,master):
        self.f = f
        self.c = c
        self.nf = len(f)
        self.nc = len(c)
        self.data = data
        self.NumP = len(data)
        self.outfile = outfile

        self.h5file_path = infile  # Save the full path to the .h5 file



        self.basename = os.path.splitext(os.path.basename(self.outfile))[0]  # Properly initialize basename

        if os.path.exists(outfile):
            self.dispersionCurves = get_yaml_data(outfile)
        else:
            self.dispersionCurves = dict()
        self.root = master

        # root.attributes('-fullscreen', True)

        self.root.geometry('1200x800')

        self.indx = 0
        self.x = []
        self.y = []
        self.index = range(3,len(f),1)
        self.fp = f[self.index]
        self.F,self.C = np.meshgrid(self.f,self.c)
        
        self.fig, self.ax = plt.subplots(figsize=(8,6),dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas,self.root)
        toolbar.update()
        self.drawDS()
        #### set buttons
        self.buttonQuit = tkinter.Button(
            master=self.root, text = "Quit",command = self._quit
        )
        self.buttonNextPoint = tkinter.Button(
            master=self.root, text = "Next Point",command = self.nextPoint
        )
        self.buttonLastPoint = tkinter.Button(
            master=self.root, text = "Last Point",command = self.lastPoint
        )
        self.buttonPick = tkinter.Button(
            master=self.root, text = "Pick",command = self.Pick
        )
        self.buttonSearch = tkinter.Button(
            master=self.root, text = "Search",command = self.search
        )
        self.buttonRedraw = tkinter.Button(
            master=self.root, text = "Redraw",command = self.drawDS
        )
       
        #### buttons distribution
        self.buttonQuit.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.buttonNextPoint.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.buttonLastPoint.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.buttonPick.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.buttonSearch.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.buttonRedraw.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    
    

    def nextPoint(self):
        if self.indx < (self.NumP-1):
            self.indx = self.indx + 1
        else:
            self.indx = 0
        self.drawDS()

    def lastPoint(self):
        if self.indx > 0 :
            self.indx = self.indx - 1
        else:
            self.indx = self.NumP-1
        self.drawDS()

    def Pick(self):
        self.connect()

    # def _quit(self):
    #     self.writein()
    #     self.root.quit()
    #     self.root.destroy()
    # def _quit(self):
    #     # Save the current state of the window as an image before quitting
    #     x = self.root.winfo_rootx()
    #     y = self.root.winfo_rooty()
    #     h = self.root.winfo_height()
    #     w = self.root.winfo_width()
    #     x1 = x + w
    #     y1 = y + h

    #     # Capture and save the screenshot
    #     ImageGrab.grab().crop((x, y, x1, y1)).save(f"{self.basename}.png")

    #     # Write any final data to YAML
    #     self.writein()

    #     # Quit the application
    #     self.root.quit()
    #     self.root.destroy()
    


    def _quit(self):
        # 保存截图
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        h = self.root.winfo_height()
        w = self.root.winfo_width()
        x1 = x + w
        y1 = y + h






        # 保存配置到 YAML 文件
        self.writein()

 

        screenshot_path = f"{self.basename}.png"
        ImageGrab.grab().crop((x, y, x1, y1)).save(screenshot_path)

        # 定义目标文件夹路径
        target_directory = r"E:\lhyonedrive\OneDrive\sym\truck\process\surface\line1_p\shots_240508_processed_sgy_1267_yml"

        # 移动 h5 文件
        shutil.move(self.h5file_path, os.path.join(target_directory, os.path.basename(self.h5file_path)))

        # 移动 yml 文件
        shutil.move(self.outfile, os.path.join(target_directory, os.path.basename(self.outfile)))

        # 移动截图
        shutil.move(screenshot_path, os.path.join(target_directory, os.path.basename(screenshot_path)))

        # 退出应用程序
        self.root.quit()
        self.root.destroy()




    def drawDS(self):
        self.order = 0
        self.ax.clear()
        self.ax.set_xlim(0, 50)  # 设置x轴的范围从0到50Hz

        self.ax.pcolormesh(self.f,self.c,self.data[self.indx,:,:][0],vmin=0.0,vmax=1.0, cmap='jet')
        self.ax.set_xlabel('Frequency')
        self.ax.set_ylabel('Phase Velocity')
        self.ax.set_title('order:'+str(self.order))
        if self.indx in self.dispersionCurves:
            for tmpdict in self.dispersionCurves[self.indx]:
                tmpdict = self.dispersionCurves[self.indx][tmpdict]
                self.ax.plot(tmpdict['f'],tmpdict['c'],'w.')
        self.canvas.draw()
        #self.dc = DispersionCurve()
        self.x = []
        self.y = [] 
        title =  str(self.indx)+'/'+str(self.NumP)
        self.root.title(title)
    
    def connect(self):
        self.canvas.mpl_connect("button_press_event",self.on_button_click)
        self.canvas.mpl_connect("key_press_event",self.on_key_press)
    
    def disconnect(self):
        self.canvas.mpl_disconnect("button_press_event")
        self.canvas.mpl_disconnect("key_press_event")

    def on_button_click(self,event):
        x = round(event.xdata,3)
        y = round(event.ydata,3)
        self.ax.plot(x,y,'k.')
        self.x.append(x)
        self.y.append(y)
        self.canvas.draw()

    def on_key_press(self,event):
        valid_range = ["{:d}".format(i) for i in range(10)]
        if event.key in valid_range:
            self.order = int(event.key)
            self.ax.set_title('order:'+str(self.order))
            self.x = []
            self.y = []
        else:
            info = "Invalid key"
            self.ax.set_title(info)
        self.canvas.draw()

    def search(self):
        self.disconnect()
        i1 = find_closer(min(self.x),self.fp)
        i2 = find_closel(max(self.x),self.fp)
        inon, on = inpolygon(self.F,self.C,self.x,self.y)
        inon = np.array(inon)
        inon = inon.reshape(self.nf,self.nc)
        tmp = inon.astype(float)*np.abs(np.squeeze(self.data[self.indx,:,:]))
        self.ax.pcolormesh(self.f,self.c,tmp,vmin=0,vmax=1.0, cmap='jet')
        x = self.fp[i1:i2]
        y = []
        for i  in range(i1,i2):
            y.append(self.c[np.argmax(tmp[:,self.index[i]])])
        
        x = list(x)
        x = [float(t) for t in x]
        y = [float(t) for t in y]
        self.addDC(x,y)
        self.ax.plot(x,y,'w.')
        self.x.append(self.x[0])
        self.y.append(self.y[0])
        self.ax.plot(self.x,self.y,'r')
        self.x = []
        self.y = []
        self.canvas.draw()
        #self.dispersionCurves[str(self.loc[self.indx,:])] = self.dc.dc
        #print(self.dc.dc)

    def writein(self):
        with open(self.outfile,'w',encoding='utf-8') as f:
            yaml.dump(self.dispersionCurves,f)
    
    def addPoint(self):
        if self.indx in self.dispersionCurves:
            pass
        else:
            tmpdict = dict()
            tmpdict[0] = dict()
            tmpdict[0]['f'] = []
            tmpdict[0]['c'] = []
            self.dispersionCurves[self.indx] = tmpdict
    
    def addOrder(self):
        if self.order in self.dispersionCurves[self.indx]:
            pass
        else:
            self.dispersionCurves[self.indx][self.order] = dict()

    def addDC(self,x,y):
        self.addPoint()
        self.addOrder()
        self.dispersionCurves[self.indx][self.order]['f'] = x
        self.dispersionCurves[self.indx][self.order]['c'] = y



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description="Select dispersion spectrums")
#     parser.add_argument(
#         "--infile",
#         default="ds.h5",
#         help="input file[ds.h5]")
#     parser.add_argument(
#         "--outfile",
#         default="config.yml",
#         help="config file[config.yml]")
#     args = parser.parse_args()

#     filepath = args.infile
#     outfile  = args.outfile
#     h5file = h5py.File(filepath, 'r')
#     data = h5file["ds"][:]
#     f = h5file["f"][:]
#     c = h5file["c"][:]
#     h5file.close()


#     root = tkinter.Tk()
#     DispersionSpectrum(f, c, data,  outfile, root)

#     root.mainloop()







# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description="Select dispersion spectrums")
#     parser.add_argument(
#         "infile",  # 使得 infile 成为一个必需的位置参数
#         help="input file, must be a .h5 file")
#     args = parser.parse_args()

#     # 检查输入文件是否为 .h5 文件
#     if not args.infile.endswith('.h5'):
#         raise ValueError("Input file must be a .h5 file")
    
#     filepath = args.infile
#     # 从输入文件路径中提取文件名（不含扩展名），用于生成输出文件名
#     basename = os.path.splitext(os.path.basename(filepath))[0]
#     outfile = f"{basename}.yml"

#     # 读取 h5 文件
#     h5file = h5py.File(filepath, 'r')
#     data = h5file["ds"][:]
#     f = h5file["f"][:]
#     c = h5file["c"][:]
#     h5file.close()

#     # 初始化 Tkinter 和 DispersionSpectrum
#     root = tkinter.Tk()
#     DispersionSpectrum(f, c, data, outfile, root)
#     root.mainloop()




import os
import h5py
import tkinter
import glob
# 假设 DispersionSpectrum 是一个已定义的类或函数

if __name__ == '__main__':





    # # 搜索当前目录下的所有 .h5 文件
    # h5_files = glob.glob('*.h5')
    
    # if not h5_files:
    #     raise FileNotFoundError("No .h5 files found in the current directory.")
    
    # # 使用找到的第一个 .h5 文件
    # filepath = h5_files[0]
    # basename = os.path.splitext(os.path.basename(filepath))[0]
    # outfile = f"{basename}.yml"

    # # 读取 h5 文件
    # h5file = h5py.File(filepath, 'r')




    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Process .h5 file for dispersion curves")
    parser.add_argument("infile", help="input file, must be a .h5 file")
    args = parser.parse_args()

    # 使用命令行提供的文件路径
    filepath = args.infile
    if not filepath.endswith('.h5'):
        raise ValueError("Input file must be a .h5 file")

    basename = os.path.splitext(os.path.basename(filepath))[0]
    outfile = f"{basename}.yml"

    # 读取 h5 文件
    h5file = h5py.File(filepath, 'r')







    data = h5file["ds"][:]
    f = h5file["f"][:]
    c = h5file["c"][:]
    h5file.close()

    # 初始化 Tkinter 和 DispersionSpectrum
    root = tkinter.Tk()
    DispersionSpectrum(f, c, data, outfile, filepath, root)
    root.mainloop()



