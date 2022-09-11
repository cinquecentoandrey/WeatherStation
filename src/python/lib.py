from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

app = QtWidgets.QApplication([])
ui = uic.loadUi('design.ui')
ui.setWindowTitle('Домашняя метеостанция')
serial = QSerialPort()
serial.setBaudRate(9600)
portList = []
ports = QSerialPortInfo.availablePorts()

for port in ports:
    portList.append(port.portName())
print(portList)

ui.com_list.addItems(portList)

listX = []
temp_listY = []
hum_listY = []
pres_listY = []

for x in range(100): listX.append(x)
for y in range(100): temp_listY.append(0)
for y in range(100): hum_listY.append(0)
for y in range(100): pres_listY.append(0)
  
def read_func():
    in_val = serial.readLine()
    in_vals = str(in_val, 'utf-8').strip()
    data = in_vals.split(',')
    global temp_listY
    global hum_listY
    global pres_listY
    if data[0] == '0':
        print('Температура: ' + str(data[1]))
        if float(data[1]) > 100:
            ui.temp_lbl.setStyleSheet("color: red;  background-color: black")
        else:
            ui.temp_lbl.setStyleSheet("color: black;  background-color: white")
        ui.temp_lbl.setText(data[1])
        temp_listY = temp_listY[1:]
        temp_listY.append(float(data[1]))
        ui.temp_wid.clear()
        ui.temp_wid.plot(listX, temp_listY)
    if data[0] == '1':
        print('Влажность: ' + str(data[1]))
        ui.hum_lbl.setText(data[1])
        hum_listY = hum_listY[1:]
        hum_listY.append(float(data[1]))
        ui.hum_wid.clear()
        ui.hum_wid.plot(listX, hum_listY)
    if data[0] == '2':
        print('Давление: '+ str(data[1]))
        ui.pres_lbl.setText(data[1])
        pres_listY = pres_listY[1:]
        pres_listY.append(float(data[1]))
        ui.pres_wid.clear()
        ui.pres_wid.plot(listX, pres_listY)
    if data[0] == '3':
        ui.met_cou.display(data[1])
        if int(data[1]) > 900:
            ui.label_6.setStyleSheet("color: red")
        elif int(data[1]) < 900:
            ui.label_6.setStyleSheet("color: black")
        print('Метан: ' + str(data[1]))
    if data[0] == '4':
        ui.co_cou.display(data[1])
        if int(data[1]) > 900:
            ui.label_9.setStyleSheet("color: red")
        elif int(data[1]) < 900:
            ui.label_9.setStyleSheet("color: black ")
        print('CO2: ' + str(data[1]))


def portOpen():
    print('open')
    serial.setPortName(ui.com_list.currentText())
    serial.open(QIODevice.ReadWrite)

def portClose():
    print('close')
    serial.close()

ui.open_button.clicked.connect(portOpen)
ui.close_button.clicked.connect(portClose)
ui.show()
app.exec()
