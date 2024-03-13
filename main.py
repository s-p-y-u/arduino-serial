import sys
import os
import time
# import serial
# import serial.tools.list_ports

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QTimer, QIODevice



PATH__DIR = os.path.dirname(os.path.abspath(__file__))


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ports = []
        self.speeds = ('1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200')

        self.serial__ports = QSerialPortInfo.availablePorts()       #получаем информацию о порте
        if(self.serial__ports):
            for portInfo in self.serial__ports:
                # print("--------------------")
                # print(f"Port:{portInfo.portName()}")
                # print(f"Location:{portInfo.systemLocation()}")
                # print(f"Description:{portInfo.description()}")
                # print(f"Manufacturer:{portInfo.manufacturer()}")
                # print(f"Serial number:{portInfo.serialNumber()}")
                # print("--------------------")                
                self.ports.append(portInfo.portName()) 

        self.layout__connect = QtWidgets.QHBoxLayout()
        self.box__ports_name = QtWidgets.QComboBox()
        self.box__ports_name.setObjectName("box__ports_name")
        self.box__ports_name.addItems(self.ports)
        self.box__ports_speeds = QtWidgets.QComboBox()
        self.box__ports_speeds.setObjectName("box__ports_speeds")
        self.box__ports_speeds.addItems(self.speeds)
        self.box__ports_speeds.setCurrentIndex(3)
        self.btn__port_connect = QtWidgets.QPushButton("Подключение")
        self.btn__port_connect.setObjectName("btn__port_connect")
        self.btn__port_connect.clicked.connect(self.serial__port_connect)
        self.layout__connect.addWidget(self.box__ports_name)
        self.layout__connect.addWidget(self.box__ports_speeds)
        self.layout__connect.addWidget(self.btn__port_connect)

        self.btn__led_2 = QtWidgets.QPushButton("on2")
        self.btn__led_2.setCheckable(True)
        self.btn__led_3 = QtWidgets.QPushButton("on3")
        self.btn__led_3.setCheckable(True)
        self.btn__led_4 = QtWidgets.QPushButton("on4")
        self.btn__led_4.setCheckable(True)
        self.btn__led_5 = QtWidgets.QPushButton("on5")
        self.btn__led_5.setCheckable(True)
        self.btn__led_6 = QtWidgets.QPushButton("on6")
        self.btn__led_6.setCheckable(True)
        self.btn__led_8 = QtWidgets.QPushButton("on8")
        self.btn__led_8.setCheckable(True)
        self.btn__led_9 = QtWidgets.QPushButton("on9")
        self.btn__led_9.setCheckable(True)
        self.btn__led_10 = QtWidgets.QPushButton("on10")
        self.btn__led_10.setCheckable(True)
        self.btn__led_11 = QtWidgets.QPushButton("on11")
        self.btn__led_11.setCheckable(True)

        self.btn__led_2.setObjectName("2")
        self.btn__led_3.setObjectName("3")
        self.btn__led_4.setObjectName("4")
        self.btn__led_5.setObjectName("5")
        self.btn__led_6.setObjectName("6")
        self.btn__led_8.setObjectName("8")
        self.btn__led_9.setObjectName("9")
        self.btn__led_10.setObjectName("10")
        self.btn__led_11.setObjectName("11")

        self.text = QtWidgets.QLabel(f"{self.ports}", alignment=QtCore.Qt.AlignCenter)

        # self.color__picker = QtWidgets.QColorDialog()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout__connect)
        self.layout.addWidget(self.text)
        # self.layout.addWidget(self.color__picker)
        self.layout.addWidget(self.btn__led_2)
        self.layout.addWidget(self.btn__led_3)
        self.layout.addWidget(self.btn__led_4)
        self.layout.addWidget(self.btn__led_5)
        self.layout.addWidget(self.btn__led_6)

        self.layout.addWidget(self.btn__led_8)
        self.layout.addWidget(self.btn__led_9)
        self.layout.addWidget(self.btn__led_10)
        self.layout.addWidget(self.btn__led_11)


        self.btn__led_2.clicked.connect(self.on)
        self.btn__led_3.clicked.connect(self.on)
        self.btn__led_4.clicked.connect(self.on)
        self.btn__led_5.clicked.connect(self.on)
        self.btn__led_6.clicked.connect(self.on)

        self.btn__led_8.clicked.connect(self.on)
        self.btn__led_9.clicked.connect(self.on)
        self.btn__led_10.clicked.connect(self.on)
        self.btn__led_11.clicked.connect(self.on)


    def serial__port_connect(self):
        # if(self.serial.isOpen()):
        #     self.serial.close()
        self.serial = QSerialPort()                                         #создаем объект порта
        self.serial.setBaudRate(int(self.box__ports_speeds.currentText()))  #устанавливаем скорость работы порта
        self.serial.setPortName(str(self.box__ports_name.currentText()))    #устанавливаем имя порта для подключения
        self.serial.setDataBits(QSerialPort.Data8)
        self.serial.setParity(QSerialPort.NoParity)
        self.serial.setStopBits(QSerialPort.OneStop)
        self.serial.setFlowControl(QSerialPort.NoFlowControl)
        self.serial.open(QIODevice.ReadWrite)                               #открываем порт для работы
        time.sleep(0.5)                                           
        self.serial.readyRead.connect(self.ser__read)                       #при событии в порте вызываем функцию
        # self.serial.setDataTerminalReady(True)   

    @QtCore.Slot()
    def on(self):
        btn__checked = self.sender().isChecked()
        pin = str(self.sender().objectName())
        match btn__checked:
            case True:
                pin += ",1;"         
            case False:
                pin += ",0;"
        print(pin)
        self.serial.write(pin.encode('utf-8'))
        self.text.setText(f"{pin}")

    def ser__read(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(',')
        temp__text = self.text.text()
        self.text.setText(f"{temp__text} -> {data}")
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    qss__file = QtCore.QFile(rf"{PATH__DIR}/main.qss")
    qss__file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(qss__file)
    app.setStyleSheet(stream.readAll())
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())



# self.timer = QTimer()
# self.timer.setInterval(500)
# self.timer.timeout.connect(self.recurring_timer)
# self.timer.start()

# def recurring_timer(self):
    # self.serial.readyRead.connect(self.ser__read)
    # rx = self.serial.readAll()
    # rxs = str(rx, 'utf-8').strip()
    # data = rxs.split(',')
    # print(data)