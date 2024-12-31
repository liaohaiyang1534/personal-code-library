import os
import h5py
import tkinter
import argparse
import shutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib.path import Path
import numpy as np
from PIL import ImageGrab

def find_closel(a, x):
    return int((a - x[0]) / (x[1] - x[0]))

def find_closer(a, x):
    return int((a - x[0]) / (x[1] - x[0])) + 1


def inpolygon(xq, yq, xv, yv):
    vertices = np.vstack((xv, yv)).T
    path = Path(vertices)
    test_points = np.hstack([xq.reshape(xq.size, -1), yq.reshape(yq.size, -1)])
    _in = path.contains_points(test_points)
    _in_on = path.contains_points(test_points, radius=-1e-10)
    _on = _in ^ _in_on
    return _in_on, _on

class DispersionCurve():
    def __init__(self):
        self.norders = 0
        self.dc = dict()
    
    def addorder(self, order):
        self.norders += 1
        self.dc[order] = dict()

    def add(self, order, x, y):
        self.addorder(order)
        self.dc[order]['f'] = x
        self.dc[order]['c'] = y

class DispersionSpectrum():

    def __init__(self, f, c, data, outfile, infile, outdir, master):
        self.f = f
        self.c = c
        self.nf = len(f)
        self.nc = len(c)
        self.data = data
        self.NumP = len(data)
        self.outfile = outfile
        self.outdir = outdir
        self.h5file_path = infile
        self.basename = os.path.splitext(os.path.basename(self.outfile))[0]
        self.dispersionCurves = {}
        self.root = master
        self.order = 0  # 定义 order 属性
        # self.root.geometry('1000x800+100+50')
        self.root.attributes('-fullscreen', True)  # 设置全屏显示
        self.indx = 0
        self.x = []
        self.y = []
        self.index = range(2, len(f), 10)
        self.fp = f[self.index]
        self.F, self.C = np.meshgrid(self.f, self.c)
        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.drawDS()
        self.buttonQuit = tkinter.Button(master=self.root, text="Quit", command=self._quit)
        self.buttonNextPoint = tkinter.Button(master=self.root, text="Next Point", command=self.nextPoint)
        self.buttonLastPoint = tkinter.Button(master=self.root, text="Last Point", command=self.lastPoint)
        self.buttonPick = tkinter.Button(master=self.root, text="Pick", command=self.Pick)
        self.buttonSearch = tkinter.Button(master=self.root, text="Search", command=self.search)
        self.buttonRedraw = tkinter.Button(master=self.root, text="Redraw", command=self.drawDS)
        self.buttonQuit.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buttonNextPoint.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buttonLastPoint.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buttonPick.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buttonSearch.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buttonRedraw.pack(side=tkinter.RIGHT, fill=tkinter.Y)


    def nextPoint(self):
        if self.indx < (self.NumP - 1):
            self.indx += 1
        else:
            self.indx = 0
        self.drawDS()

    def lastPoint(self):
        if self.indx > 0:
            self.indx -= 1
        else:
            self.indx = self.NumP - 1
        self.drawDS()

    def Pick(self):
        self.connect()

    # def _quit(self):
    #     x = self.root.winfo_rootx()
    #     y = self.root.winfo_rooty()
    #     h = self.root.winfo_height()
    #     w = self.root.winfo_width()
    #     x1 = x + w
    #     y1 = y + h

    #     self.writein()

    #     screenshot_path = f"{self.basename}.png"
    #     ImageGrab.grab().crop((x, y, x1, y1)).save(screenshot_path)

    #     shutil.move(self.h5file_path, os.path.join(self.outdir, os.path.basename(self.h5file_path)))
    #     shutil.move(self.outfile, os.path.join(self.outdir, os.path.basename(self.outfile)))
    #     shutil.move(screenshot_path, os.path.join(self.outdir, os.path.basename(screenshot_path)))

    #     self.root.quit()
    #     self.root.destroy()

    def _quit(self):
        self.writein()

        screenshot_path = f"{self.basename}.png"
        ImageGrab.grab().save(screenshot_path)

        shutil.move(self.h5file_path, os.path.join(self.outdir, os.path.basename(self.h5file_path)))
        shutil.move(self.outfile, os.path.join(self.outdir, os.path.basename(self.outfile)))
        shutil.move(screenshot_path, os.path.join(self.outdir, os.path.basename(screenshot_path)))

        self.root.quit()
        self.root.destroy()


    def drawDS(self):
        # 确保数据形状正确
        if len(self.data.shape) == 2 and self.data.shape == (self.nc, self.nf):
            plot_data = self.data
        else:
            raise ValueError(f"Unexpected data shape: {self.data.shape}, expected ({self.nc}, {self.nf})")
        self.order = 0
        self.ax.clear()

        self.ax.pcolormesh(self.f, self.c, plot_data, vmin=0.0, vmax=1.0, cmap='jet')
        self.ax.set_xlabel('Frequency')
        self.ax.set_ylabel('Phase Velocity')
        self.ax.set_title('Dispersion Spectrum')
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 1200)  # 设置相速度的显示范围
        if self.indx in self.dispersionCurves:
            for tmpdict in self.dispersionCurves[self.indx]:
                tmpdict = self.dispersionCurves[self.indx][tmpdict]
                self.ax.plot(tmpdict['f'],tmpdict['c'],'w.')
        self.canvas.draw()
        self.x = []
        self.y = [] 
        title =  str(self.indx)+'/'+str(self.NumP)
        self.root.title(title)


    def connect(self):
        self.canvas.mpl_connect("button_press_event", self.on_button_click)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)
    
    def disconnect(self):
        self.canvas.mpl_disconnect("button_press_event")
        self.canvas.mpl_disconnect("key_press_event")

    def on_button_click(self, event):
        x = round(event.xdata, 3)
        y = round(event.ydata, 3)
        self.ax.plot(x, y, 'k.')
        self.x.append(x)
        self.y.append(y)
        self.canvas.draw()

    def on_key_press(self, event):
        valid_range = ["{:d}".format(i) for i in range(10)]
        if event.key in valid_range:
            self.order = int(event.key)
            self.ax.set_title('order:' + str(self.order))
            self.x = []
            self.y = []
        else:
            info = "Invalid key"
            self.ax.set_title(info)
        self.canvas.draw()


    # def search(self):
    #     self.disconnect()

    #     if not self.x or not self.y:
    #         print("No points have been picked yet.")
    #         return

    #     print("x points:", self.x)
    #     print("y points:", self.y)

    #     i1 = find_closer(min(self.x), self.fp)
    #     i2 = find_closel(max(self.x), self.fp)
        
    #     print("i1:", i1)
    #     print("i2:", i2)

    #     inon, on = inpolygon(self.F, self.C, self.x, self.y)

    #     # 调试输出
    #     print("inon shape:", inon.shape)
    #     print("on shape:", on.shape)
    #     print("self.F shape:", self.F.shape)
    #     print("self.C shape:", self.C.shape)
    #     print("data shape:", self.data[self.indx, :, :].shape)

    #     # 确保 inon 的形状与 self.data 的形状匹配
    #     inon_reshaped = inon.reshape(self.F.shape)
    #     print("reshaped inon shape:", inon_reshaped.shape)

    #     tmp = inon_reshaped.astype(float) * np.abs(np.squeeze(self.data[self.indx, :, :]))
        
    #     self.ax.pcolormesh(self.f, self.c, tmp, vmin=0, vmax=1.0, cmap='jet')
    #     x = self.fp[i1:i2]
    #     y = [self.c[np.argmax(tmp[:, self.index[i]])] for i in range(i1, i2)]
    #     self.addDC(list(x), y)
    #     self.ax.plot(x, y, 'w.')
    #     self.x.append(self.x[0])
    #     self.y.append(self.y[0])
    #     self.ax.plot(self.x, self.y, 'r')
    #     self.x = []
    #     self.y = []
    #     self.canvas.draw()

    # def search(self):
    #     self.disconnect()

    #     if not self.x or not self.y:
    #         print("No points have been picked yet.")
    #         return

    #     print("x points:", self.x)
    #     print("y points:", self.y)

    #     i1 = find_closer(min(self.x), self.fp)
    #     i2 = find_closel(max(self.x), self.fp)
        
    #     print("i1:", i1)
    #     print("i2:", i2)

    #     inon, on = inpolygon(self.F, self.C, self.x, self.y)

    #     # 调试输出
    #     print("inon shape:", inon.shape)
    #     print("on shape:", on.shape)
    #     print("self.F shape:", self.F.shape)
    #     print("self.C shape:", self.C.shape)
    #     print("data shape:", self.data.shape)

    #     # 确保 inon 的形状与 self.data 的形状匹配
    #     inon_reshaped = inon.reshape(self.F.shape)
    #     print("reshaped inon shape:", inon_reshaped.shape)

    #     tmp = inon_reshaped.astype(float) * np.abs(self.data)

    #     self.ax.pcolormesh(self.f, self.c, tmp, vmin=0, vmax=1.0, cmap='jet')
    #     x = self.fp[i1:i2]
    #     y = [self.c[np.argmax(tmp[:, self.index[i]])] for i in range(i1, i2)]
    #     self.addDC(list(x), y)
    #     self.ax.plot(x, y, 'w.')
    #     self.x.append(self.x[0])
    #     self.y.append(self.y[0])
    #     self.ax.plot(self.x, self.y, 'r')
    #     self.x = []
    #     self.y = []
    #     self.canvas.draw()

    def search(self):
        self.disconnect()

        if not self.x or not self.y:
            print("No points have been picked yet.")
            return

        print("x points:", self.x)
        print("y points:", self.y)

        i1 = find_closer(min(self.x), self.fp)
        i2 = find_closel(max(self.x), self.fp)
        
        print("i1:", i1)
        print("i2:", i2)

        inon, on = inpolygon(self.F, self.C, self.x, self.y)

        # 调试输出
        print("inon shape:", inon.shape)
        print("on shape:", on.shape)
        print("self.F shape:", self.F.shape)
        print("self.C shape:", self.C.shape)
        print("data shape:", self.data.shape)

        # 确保 inon 的形状与 self.data 的形状匹配
        inon_reshaped = inon.reshape(self.F.shape)
        print("reshaped inon shape:", inon_reshaped.shape)

        tmp = inon_reshaped.astype(float) * np.abs(self.data)

        self.ax.pcolormesh(self.f, self.c, tmp, vmin=0, vmax=1.0, cmap='jet')
        x = self.fp[i1:i2]
        # y = [self.c[np.argmax(tmp[:, self.index[i]])] for i in range(i1, i2)]
        y = []
        for i  in range(i1,i2):
            y.append(self.c[np.argmax(tmp[:,self.index[i]])])


        x = list(x)
        x = [float(t) for t in x]
        y = [float(t) for t in y]

        # self.addDC(list(x), y)
        self.addDC(x,y)
        self.ax.plot(x, y, 'w.')
        self.x.append(self.x[0])
        self.y.append(self.y[0])
        self.ax.plot(self.x, self.y, 'w')

        # # 保留选取的点
        # self.ax.plot(self.x[:-1], self.y[:-1], 'ko')

        self.x = []
        self.y = []
        self.canvas.draw()



    def writein(self):
        with open(self.outfile, 'w', encoding='utf-8') as f:
            for key1 in self.dispersionCurves:
                for key2 in self.dispersionCurves[key1]:
                    for freq, vel in zip(self.dispersionCurves[key1][key2]['f'], self.dispersionCurves[key1][key2]['c']):
                        vel_km_s = vel / 1000  # 转换为km/s
                        f.write(f"{freq} {vel_km_s} {key2}\n")
    
    def addPoint(self):
        if self.indx not in self.dispersionCurves:
            self.dispersionCurves[self.indx] = {0: {'f': [], 'c': []}}

    def addOrder(self):
        if self.order not in self.dispersionCurves[self.indx]:
            self.dispersionCurves[self.indx][self.order] = {}


    # def addOrder(self):
    #     if self.order not in self.dispersionCurves[self.indx]:
    #         self.dispersionCurves[self.indx][self.order] = {}

    def addDC(self, x, y):
        self.addPoint()
        self.addOrder()
        self.dispersionCurves[self.indx][self.order]['f'] = x
        self.dispersionCurves[self.indx][self.order]['c'] = y




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process .h5 file for dispersion curves")
    parser.add_argument("infile", help="input file, must be a .h5 file")
    parser.add_argument("outdir", help="output directory to save results")
    parser.add_argument("--dataset", help="specific dataset key within the .h5 file", default="ds10")
    args = parser.parse_args()

    filepath = args.infile
    if not filepath.endswith('.h5'):
        raise ValueError("Input file must be a .h5 file")

    basename = os.path.splitext(os.path.basename(filepath))[0]
    outfile = os.path.join(args.outdir, f"{basename}.txt")

    h5file = h5py.File(filepath, 'r')

    # 增加一个帮助函数来自动发现数据集键
    def discover_dataset_keys(h5file):
        keys = list(h5file.keys())
        print("Available datasets in the file:", keys)
        for key in keys:
            print(f"Dataset {key} shape: {h5file[key].shape}")
        return keys
    # 选择数据集
    if args.dataset:
        if args.dataset in h5file:
            data = h5file[args.dataset][:]
            print(f"Selected dataset '{args.dataset}' shape: {data.shape}")
        else:
            raise KeyError(f"Dataset {args.dataset} not found in the file.")
    else:
        # 自动检测数据集键
        dataset_keys = discover_dataset_keys(h5file)
        if not dataset_keys:
            raise ValueError("No datasets found in the .h5 file.")
        data = h5file[dataset_keys[0]][:]
        print(f"Selected dataset shape: {data.shape}")

    f = h5file["f"][:]
    c = h5file["c"][:]
    print(f"f shape: {f.shape}")
    print(f"c shape: {c.shape}")
    h5file.close()


    root = tkinter.Tk()
    DispersionSpectrum(f, c, data, outfile, filepath, args.outdir, root)
    root.mainloop()




# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Process .h5 file for dispersion curves")
#     parser.add_argument("infile", help="input file, must be a .h5 file")
#     parser.add_argument("outdir", help="output directory to save results")
#     parser.add_argument("--dataset", help="specific dataset key within the .h5 file", default=None)
#     args = parser.parse_args()

#     filepath = args.infile
#     if not filepath.endswith('.h5'):
#         raise ValueError("Input file must be a .h5 file")

#     basename = os.path.splitext(os.path.basename(filepath))[0]
#     outfile = os.path.join(args.outdir, f"{basename}.txt")





#     h5file = h5py.File(filepath, 'r')




#     # # 增加一个帮助函数来自动发现数据集键
#     # def discover_dataset_keys(h5file):
#     #     keys = list(h5file.keys())
#     #     print("Available datasets in the file:", keys)
#     #     return keys

#     # 增加一个帮助函数来自动发现数据集键
#     def discover_dataset_keys(h5file):
#         keys = list(h5file.keys())
#         print("Available datasets in the file:", keys)
#         for key in keys:
#             print(f"Dataset {key} shape: {h5file[key].shape}")
#         return keys


#     # # 选择数据集
#     # if args.dataset:
#     #     if args.dataset in h5file:
#     #         data = h5file[args.dataset][:]
#     #     else:
#     #         raise KeyError(f"Dataset {args.dataset} not found in the file.")
#     # else:
#     #     # 自动检测数据集键
#     #     dataset_keys = discover_dataset_keys(h5file)
#     #     if not dataset_keys:
#     #         raise ValueError("No datasets found in the .h5 file.")
#     #     data = h5file[dataset_keys[0]][:]

#     # data = h5file["ds"][:]







#     # f = h5file["f"][:]
#     # c = h5file["c"][:]




#     if args.dataset:
#         if args.dataset in h5file:
#             data = h5file[args.dataset][:]
#         else:
#             raise KeyError(f"Dataset {args.dataset} not found in the file.")
#     else:
#         # 自动检测数据集键
#         dataset_keys = discover_dataset_keys(h5file)
#         if not dataset_keys:
#             raise ValueError("No datasets found in the .h5 file.")
#         data = h5file[dataset_keys[0]][:]
#         print(f"Selected dataset shape: {data.shape}")

#     f = h5file["f"][:]
#     c = h5file["c"][:]





#     h5file.close()

#     root = tkinter.Tk()
#     DispersionSpectrum(f, c, data, outfile, filepath, args.outdir, root)
#     root.mainloop()
