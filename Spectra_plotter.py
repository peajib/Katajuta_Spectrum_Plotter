# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:38:02 2022

@author: Darren Hudson
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTextBrowser, QLabel, QComboBox, QMessageBox
from PyQt5.QtWidgets import QApplication
import numpy as np
import pandas as pd
import sys
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.style
import matplotlib as mpl
mpl.style.use('seaborn-bright')




class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi('Spectra_plotter.ui',self)
        self.show()
        self.title = 'Spectra Plotter'
        self.setWindowTitle(self.title)

        #self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1,3)
        #self.canvas.figure.subplots(1,3)
        self.figure = Figure(figsize=(16,9))      # we make a matplotlib figure
        self.figure.subplots_adjust(hspace=0.6)
        self.canvas = FigureCanvas(self.figure)   # we make a canvas and shove the figure into the canvas
        self.ax1 = self.figure.add_subplot(1,1,1)
        self.toolbar = NavigationToolbar(self.canvas,self)
        
        
        # setup the main figure plot for the data    
        self.figure = Figure(figsize=(26,9))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(1,1,1)
        self.ax.set_xlim([1000,1110])
        self.ax.set_ylim([-200,0])
        self.ax.set_xlabel('wavelength [nm]')
        self.ax.set_ylabel('power level')  
        self.toolbar = NavigationToolbar(self.canvas,self)
                
        
        # Magic happens here. The vertical layout contains the QWidget that will be our pyplot
        # Using .addWidget we add a pyplot object to the Widget, making a plottable thing.
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)
        
        # Draw the initial plots
        self.canvas.draw()
        self.canvas.flush_events()
   
        # Hook up buttons to functions
        self.offset.setText('0')
        self.legendButton.setCheckable(True) 
        self.persistButton.setCheckable(True)
        self.offsetButton.setCheckable(True)
        self.loadButton.clicked.connect(self.openf)
        self.clearButton.clicked.connect(self.clear)
        
        self.offset_counter = 0 


    def openf(self):
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"Select a spectrum to plot", "","All Files (*)", options=options)

            if fileName:     
                self.fname_loaded.setText(fileName)
                self.data = pd.read_csv(fileName,sep='\s+') #whitespace + separator
            
                # Now plot the data on that matplotlib plot
                if self.persistButton.isChecked() == True:
                    pass
                else: 
                    self.ax.clear()
    
                self.canvas.flush_events()
                
                if self.offsetButton.isChecked() == True:
                    self.ax.plot(self.data.iloc[:,0],self.data.iloc[:,1]+(self.offset_counter*float(self.offset.text())),linewidth = 0.75,label=fileName)
                    self.offset_counter = self.offset_counter+1
                else:
                    self.ax.plot(self.data.iloc[:,0],self.data.iloc[:,1],linewidth = 0.75,label=fileName)  
            
                self.ax.set_xlabel('wavelength [nm]')
                self.ax.set_ylabel('power level')
                self.ax.set_ylim([-100,0])
                if self.legendButton.isChecked() == True:
                    self.ax.legend()
                else:
                    self.ax.legend().set_visible(False)
                             
                self.canvas.draw()
            
            else:
                pass
       
     
        
       
    def clear(self):
        self.offset_counter = 0 
        self.ax.clear()
        self.canvas.draw()

    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Ui()
    myapp.show()
    sys.exit(app.exec_())


