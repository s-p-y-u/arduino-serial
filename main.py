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

        self.color__box = QtWidgets.QWidget()
        self.color__box.setMaximumHeight(90)
        self.color__layout_v = QtWidgets.QVBoxLayout()
        self.color__layout_h = QtWidgets.QHBoxLayout()
        self.color__layout_h2 = QtWidgets.QHBoxLayout()
        for i in range(16):
            print(i)
            i+=1
            color__btn = QtWidgets.QPushButton(f"{i}")
            color__btn.setObjectName(f"color №{i}")
            color__btn.clicked.connect(self.testtt)
            if(i < 9):            
                self.color__layout_h.addWidget(color__btn)
            else:
                self.color__layout_h2.addWidget(color__btn)
        self.pwm__led_rgbw = QtWidgets.QPushButton("pwm__led_rgbw")
        self.pwm__led_rgbw.setObjectName("pwm__led_rgbw")
        self.color__layout_h.addWidget(self.pwm__led_rgbw)
        self.color__layout_v.addLayout(self.color__layout_h)
        self.color__layout_v.addLayout(self.color__layout_h2)
        self.color__box.setLayout(self.color__layout_v)
        # self.color__box.setLayout(self.color__layout_h)
        # self.color__box.setLayout(self.color__layout_h2)

        self.btn__box = QtWidgets.QWidget()
        self.btn__box.setMaximumHeight(40)
        self.btn__layout_h = QtWidgets.QHBoxLayout()
        self.btn__led_4 = QtWidgets.QPushButton("on4")
        self.btn__led_4.setObjectName("4")
        self.btn__led_4.setCheckable(True)
        self.btn__led_8 = QtWidgets.QPushButton("on8")
        self.btn__led_8.setObjectName("8")
        self.btn__led_8.setCheckable(True)
        self.btn__led_9 = QtWidgets.QPushButton("on9")
        self.btn__led_9.setObjectName("9")
        self.btn__led_9.setCheckable(True)
        self.btn__layout_h.addWidget(self.btn__led_4)
        self.btn__layout_h.addWidget(self.btn__led_8)
        self.btn__layout_h.addWidget(self.btn__led_9)
        self.btn__box.setLayout(self.btn__layout_h)

        self.pwm__box = QtWidgets.QWidget()
        self.pwm__box.setMaximumHeight(40)
        self.pwm__layout = QtWidgets.QHBoxLayout()
        self.pwm__btn = QtWidgets.QPushButton("PWM-31.4")
        self.pwm__btn.setObjectName("pwm")
        self.pwm__btn.setCheckable(True)
        self.pwm__speed_min = QtWidgets.QLabel("80")
        self.pwm__speed_max = QtWidgets.QLabel("255")
        self.pwm__speed_total = QtWidgets.QLabel("80")
        self.pwm__speed = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.pwm__speed.setRange(80, 255)
        self.pwm__speed.valueChanged.connect(self.set__pwm_speed)
        self.pwm__layout.addWidget(self.pwm__btn)
        self.pwm__layout.addWidget(self.pwm__speed_min)
        self.pwm__layout.addWidget(self.pwm__speed)
        self.pwm__layout.addWidget(self.pwm__speed_max)
        self.pwm__layout.addWidget(self.pwm__speed_total)
        self.pwm__box.setLayout(self.pwm__layout)

        self.text = QtWidgets.QLabel(f"{self.ports}", alignment=QtCore.Qt.AlignCenter)

        # self.color__picker = QtWidgets.QColorDialog()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout__connect)
        self.layout.addWidget(self.text)
        # self.layout.addWidget(self.color__picker)
        self.layout.addWidget(self.color__box)
        self.layout.addWidget(self.btn__box)
        self.layout.addWidget(self.pwm__box)
        # self.layout.addWidget(self.btn__led_4)
        # self.layout.addWidget(self.btn__led_8)
        # self.layout.addWidget(self.btn__led_9)
        # self.layout.addLayout(self.pwm__layout)
        # self.layout.addWidget(self.btn__led_11)


        self.pwm__led_rgbw.clicked.connect(self.pwm__led_rgbw_set_color)
        # self.btn__led_3.clicked.connect(self.on)
        self.btn__led_4.clicked.connect(self.on)
        # self.btn__led_5.clicked.connect(self.on)
        # self.btn__led_6.clicked.connect(self.on)

        self.btn__led_8.clicked.connect(self.on)
        self.btn__led_9.clicked.connect(self.on)
        self.pwm__btn.clicked.connect(self.set__pwm)
        # self.btn__led_11.clicked.connect(self.on)


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

    def pwm__led_rgbw_set_color(self):
        name = str(self.sender().objectName())
        if(name == "pwm__led_rgbw"):
            color = QtWidgets.QColorDialog()
            rgb = color.getColor().getRgb()
            # print(rgb)
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            w = 0
            if(r == 255 and g == 255 and b == 255):
                w = 255
                r = 0
                g = 0
                b = 0
            set__data = f"0,{r},{g},{b},{w},100;" 
            self.serial.write(set__data.encode('utf-8'))
            self.text.setText(f"{set__data}")

    def set__pwm(self):
        btn__checked = self.sender().isChecked()
        match btn__checked:
            case True:
                pwm = f"10,{self.pwm__speed.value()};"         
            case False:
                pwm = "10,0;"
        self.serial.write(pwm.encode('utf-8'))

    def set__pwm_speed(self):
        self.pwm__speed_total.setText(str(self.pwm__speed.value()))
        if(self.pwm__btn.isChecked()):
            speed = f"10,{self.pwm__speed.value()};"
            self.serial.write(speed.encode('utf-8'))

    # def set__pwm_speed_total(self):
    #     self.pwm__speed_total.setText(str(self.pwm__speed.value()))

    @QtCore.Slot()
    def on(self):
        btn__checked = self.sender().isChecked()
        pin = str(self.sender().objectName())
        match btn__checked:
            case True:
                pin += ",1;"         
            case False:
                pin += ",0;"
        # print(pin)
        self.serial.write(pin.encode('utf-8'))
        # self.text.setText(f"{pin}")

    def ser__read(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(',')
        # temp__text = self.text.text()
        # self.text.setText(f"{temp__text} -> {data}")
        # print(data)
        self.text.setText(f"{data}")
    
    def testtt(self):
        print(self.sender().objectName())

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