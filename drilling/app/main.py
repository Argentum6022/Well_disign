import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from first_window import Ui_MainWindow
from CPG import CPG
from well_construction import construction
intervals = 0
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict

import traceback
class ImageDialog(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.get_data)
        self.ui.pushButton_2.clicked.connect(self.get_graph)
        self.ui.comboBox.currentTextChanged.connect(self.check_label)
        self.ui.pushButton_3.clicked.connect(self.calculate_table)

    def get_data(self):
        P =[]
        H=[]
        for row in range(0,self.ui.tableWidget.rowCount()):
            for column in range(0,self.ui.tableWidget.columnCount()):
                if self.ui.tableWidget.item(row,column) == None:
                    pass
                else:
                    if column == 0:
                        P.append(float(self.ui.tableWidget.item(row, column).text()))

                    elif column ==1:
                        H.append(float(self.ui.tableWidget.item(row, column).text()))
        print(H,P)
        return H,P

    def get_graph(self):
        global intervals
        H,P = self.get_data()
        try:
            H_intervals, intervals = CPG(H,P)
        except:
            print('ERROR',traceback.format_exc())
        print(H_intervals,intervals)
        self.ui.lineEdit_2.setText(str(intervals))

        for column in range(0, self.ui.tableWidget_3.columnCount()):
            for row in range(len(H_intervals)):
                self.ui.tableWidget_3.setItem(row, column, QTableWidgetItem(str(H_intervals[row])))




    def check_label(self):
        if self.ui.comboBox.currentText() == 'Нефтяная':
            self.ui.label_4.setText('т/сутки')
        else:
            self.ui.label_4.setText('м^3/сутки')


    def calculate_table(self):
        Q = int(self.ui.lineEdit.text())
        intervals = int(self.ui.lineEdit_2.text())
        Type = str(self.ui.comboBox.currentText())
        H_intervals = []
        try:
            for row in range(4):
                if self.ui.tableWidget_3.item(row, 0):
                    print(1)
                    H_intervals.append(float(self.ui.tableWidget_3.item(row, 0).text()))
        except:
            print('ЦИКЛ',traceback.format_exc())

        print('ИНТЕРВАЛЫ',H_intervals,intervals,Q,Type)
        print(H_intervals,intervals,Q,Type)
        try:
            data = construction(H_intervals,intervals,Q,Type)
        except:
            print(traceback.format_exc())
        print(data)

        N = [ i for i in data[0].values()]
        K = False
        E = [ i for i in data[-1].values()]
        P_1 = False
        P_2 = False
        if len(data) ==3:
            K = [ i for i in data[1].values()]

        if len(data) ==4:
            K = [i for i in data[1].values()]
            P_1 = [ i for i in data[2].values()]

        if len(data) ==5:
            K = [i for i in data[1].values()]
            P_1 = [ i for i in data[2].values()]
            P_2 = [i for i in data[3].values()]

        for column in range(0, self.ui.tableWidget_2.columnCount()):
            for row in range(0, self.ui.tableWidget_2.rowCount()):
                if column == 0:
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(N[row])))

                elif column == 1 and K:
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(K[row])))

                elif column == 4:
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(E[row])))

                elif column == 2 and P_1:
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(P_1[row])))

                elif column == 3 and P_2:
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(P_2[row])))















app = QApplication(sys.argv)
window = ImageDialog()

window.show()



print(window.ui.comboBox.currentText())
sys.exit(app.exec())






