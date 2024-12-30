import sys
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt

class InteractiveDispersionEditor(QMainWindow):
    def __init__(self, spectrum_files, dispersion_directory, fmin=1, fmax=50, vmin=100, vmax=600):
        super().__init__()
        self.spectrum_files = spectrum_files
        self.file_index = 0
        self.dispersion_directory = dispersion_directory
        self.fmin = fmin
        self.fmax = fmax
        self.vmin = vmin
        self.vmax = vmax
        self.file_label = QLabel("", self)
        self.file_label.setWordWrap(True)
        self.load_data(self.spectrum_files[self.file_index])
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus)

    def load_data(self, filepath):
        self.filepath = filepath
        self.spec = np.load(self.filepath)['data']
        txt_filename = os.path.splitext(os.path.basename(self.filepath))[0] + ".txt"
        txt_path = os.path.join(self.dispersion_directory, txt_filename)
        if os.path.exists(txt_path):
            all_dispersion_data = np.loadtxt(txt_path, delimiter=',')
            filtered_dispersion_data = all_dispersion_data[
                (all_dispersion_data[:, 0] >= 10) & (all_dispersion_data[:, 0] <= 32) &
                (all_dispersion_data[:, 1] >= 100) & (all_dispersion_data[:, 1] <= 600)
            ]
            self.dispersion_data = filtered_dispersion_data[::10]
        else:
            self.dispersion_data = np.empty((0, 2))
        self.file_label.setText(f"Current File: {os.path.basename(self.filepath)} ({self.file_index + 1} of {len(self.spectrum_files)})")

    def update_plot(self):
        self.ax.clear()
        self.ax.imshow(self.spec**5, cmap='viridis', aspect='auto', origin='lower', extent=[self.fmin, self.fmax, self.vmin, self.vmax])
        self.scatter = self.ax.scatter(self.dispersion_data[:, 0], self.dispersion_data[:, 1], color='red', picker=True)
        padding_factor = 0.1
        x_pad = (self.fmax - self.fmin) * padding_factor
        y_pad = (self.vmax - self.vmin) * padding_factor
        self.ax.set_xlim([self.fmin - x_pad, self.fmax + x_pad])
        self.ax.set_ylim([self.vmin - y_pad, self.vmax + y_pad])
        self.ax.set_title('Dispersion Data Visualization')
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Velocity (m/s)')
        self.canvas.draw_idle()

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333333;
                color: #ffffff;
            }
            QPushButton {
                background-color: #006699;
                color: #ffffff;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005577;
            }
            QLabel {
                font-size: 16px;
                color: #ffffff;
            }
        """)
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        self.ax = self.canvas.figure.subplots()
        self.ax.imshow(self.spec**5, cmap='viridis', aspect='auto', origin='lower', extent=[self.fmin, self.fmax, self.vmin, self.vmax])
        self.ax.set_title('Dispersion Data Visualization')
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Velocity (m/s)')
        plt.style.use('ggplot')
        self.ax.grid(True, linestyle='--', linewidth=0.5, color='gray')

        self.scatter = self.ax.scatter(self.dispersion_data[:, 0], self.dispersion_data[:, 1], color='red', picker=True)
        padding_factor = 0.1
        x_pad = (self.fmax - self.fmin) * padding_factor
        y_pad = (self.vmax - self.vmin) * padding_factor
        self.ax.set_xlim([self.fmin - x_pad, self.fmax + x_pad])
        self.ax.set_ylim([self.vmin - y_pad, self.vmax + y_pad])

        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.selector = RectangleSelector(self.ax, self.on_select, useblit=True,
                                          button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

        btn_save_quit = QPushButton('Save Data and Quit', self)
        btn_save_quit.clicked.connect(self.save_data_and_quit)
        btn_save_quit.setCursor(Qt.PointingHandCursor)
        btn_save_quit.setToolTip('Click to save the dispersion data and move to the next file')

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.canvas)
        layout.addWidget(btn_save_quit)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def on_pick(self, event):
        if event.mouseevent.button == 1 and len(event.ind) > 0:
            ind = event.ind[0]
            self.dispersion_data = np.delete(self.dispersion_data, ind, 0)
            self.update_plot()

    def on_click(self, event):
        if event.button == 3:
            x, y = event.xdata, event.ydata
            self.dispersion_data = np.append(self.dispersion_data, [[x, y]], axis=0)
            self.update_plot()

    def on_select(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.dispersion_data = np.array([point for point in self.dispersion_data
                                         if not (min(x1, x2) <= point[0] <= max(x1, x2) and min(y1, y2) <= point[1] <= max(y1, y2))])
        self.update_plot()

    def save_data_and_quit(self):
        self.save_data()
        self.next_file()

    def save_data(self):
        txt_new_path = os.path.join(os.path.dirname(self.dispersion_directory), os.path.basename(self.dispersion_directory) + "_modified")
        if not os.path.exists(txt_new_path):
            os.makedirs(txt_new_path)
        txt_filename = os.path.splitext(os.path.basename(self.filepath))[0] + ".txt"
        save_path = os.path.join(txt_new_path, txt_filename)
        np.savetxt(save_path, self.dispersion_data, fmt='%.6f', delimiter=',')
        print(f"Modified dispersion data sorted and saved to {save_path}")

    def next_file(self):
        self.file_index += 1
        if self.file_index < len(self.spectrum_files):
            self.load_data(self.spectrum_files[self.file_index])
            self.update_plot()
        else:
            self.close()

    def handle_exception(self, e):
        QMessageBox.critical(self, 'Error', str(e))

if __name__ == "__main__":
    try:
        spectrum_directory = r"I:\diff_dis_to_cavity\RESULTS_LHY_20241201_whole_line1_rolling_6_16marray\spectrum_C3"
        dispersion_directory = r"I:\diff_dis_to_cavity\RESULTS_LHY_20241201_whole_line1_rolling_6_16marray\curve_C3"
        spectrum_files = [os.path.join(spectrum_directory, f) for f in os.listdir(spectrum_directory) if f.endswith('.npz')]
        app = QApplication(sys.argv)
        editor = InteractiveDispersionEditor(spectrum_files, dispersion_directory)
        app.exec_()
    except Exception as e:
        print("An error occurred:", e)
