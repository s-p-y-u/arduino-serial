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
        self.colors = ['0,0,0','255,255,255','255,0,255','128,0,128','255,0,0','128,0,0','255,255,0','0,255,0','0,128,0',
                      '0,255,255','0,128,128','0,0,255','0,0,128']

        self.red = 0
        self.green = 0
        self.blue = 0
        self.w = 0 
        self.brightness = 0

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
        self.box__ports_speeds.setCurrentIndex(7)
        self.btn__port_connect = QtWidgets.QPushButton("Подключение")
        self.btn__port_connect.setObjectName("btn__port_connect")
        self.btn__port_connect.clicked.connect(self.serial__port_connect)
        self.layout__connect.addWidget(self.box__ports_name)
        self.layout__connect.addWidget(self.box__ports_speeds)
        self.layout__connect.addWidget(self.btn__port_connect)

        self.color__box = QtWidgets.QWidget()
        self.color__box.setMaximumHeight(400)
        self.color__box.setMaximumWidth(200)
        self.color__box_v_layout = QtWidgets.QVBoxLayout()
        self.color__grid_layout = QtWidgets.QGridLayout()
        self.color__grid_layout.setVerticalSpacing(5)
        self.color__grid_layout.setHorizontalSpacing(5)
        index = 0
        # key = list(self.colors__dict.keys())
        # val = list(self.colors__dict.values())
        for row in range(3):
            for col in range(4):
                color__btn = QtWidgets.QPushButton()
                color__btn.setObjectName(f"{self.colors[index]}")
                color__btn.clicked.connect(self.color__set)
                color__btn.setStyleSheet(f"background-color:rgb({self.colors[index]});max-width:30px;max-height:30px;width:30px;height:30px; border:none; border-radius:3px")
                self.color__grid_layout.addWidget(color__btn, row, col)
                index += 1
        
        self.color__brightness_label = QtWidgets.QLabel("Яркость")
        self.color__brightness_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.color__brightness_slider.setRange(0, 100)
        self.color__brightness_slider.setValue(100)
        self.color__brightness_slider.valueChanged.connect(self.f_color__brightness)

        self.color__extended = QtWidgets.QPushButton("color__extended")
        self.color__extended.setObjectName("color__extended")
        self.color__extended.clicked.connect(self.color__set)
        
        self.color__extended_layout = QtWidgets.QVBoxLayout()
        self.color__extended_layout.addWidget(self.color__extended)
        self.color__extended_layout.addWidget(self.color__brightness_label)
        self.color__extended_layout.addWidget(self.color__brightness_slider)
        self.color__box_v_layout.addLayout(self.color__grid_layout)
        self.color__box_v_layout.addLayout(self.color__extended_layout)
        self.color__box.setLayout(self.color__box_v_layout)

        self.btn__box = QtWidgets.QWidget()
        self.btn__box.setMaximumHeight(40)
        self.btn__layout_h = QtWidgets.QHBoxLayout()
        # self.pwm__led_rgbw = QtWidgets.QPushButton("pwm__led_rgbw")
        # self.pwm__led_rgbw.setObjectName("pwm__led_rgbw")
        self.btn__led_4 = QtWidgets.QPushButton("on4")
        self.btn__led_4.setObjectName("4")
        self.btn__led_4.setCheckable(True)
        self.btn__led_8 = QtWidgets.QPushButton("on8")
        self.btn__led_8.setObjectName("8")
        self.btn__led_8.setCheckable(True)
        self.btn__led_9 = QtWidgets.QPushButton("on9")
        self.btn__led_9.setObjectName("9")
        self.btn__led_9.setCheckable(True)
        # self.btn__layout_h.addWidget(self.pwm__led_rgbw)
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

        # self.text = QtWidgets.QLabel(f"{self.ports}", alignment=QtCore.Qt.AlignCenter)
        # self.text = QtWidgets.QLabel("start", alignment=QtCore.Qt.AlignCenter)
        # self.color__picker = QtWidgets.QColorDialog()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout__connect)
        self.layout.addWidget(QtWidgets.QSplitter(QtCore.Qt.Vertical, self))
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.color__picker)
        self.layout.addWidget(self.color__box)
        self.layout.addWidget(self.btn__box)
        self.layout.addWidget(self.pwm__box)
        # self.layout.addWidget(self.btn__led_4)
        # self.layout.addWidget(self.btn__led_8)
        # self.layout.addWidget(self.btn__led_9)
        # self.layout.addLayout(self.pwm__layout)
        # self.layout.addWidget(self.btn__led_11)


        # self.pwm__led_rgbw.clicked.connect(self.color__set)
        
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

    def color__set(self):
        name = str(self.sender().objectName())
        set__data = ""
        self.brightness = self.color__brightness_slider.value()
        if(name == "color__extended"):
            color = QtWidgets.QColorDialog()
            rgb = color.getColor().getRgb()
            if(rgb[0] == 0 and rgb[1] == 0 and rgb[2] == 0): return
            self.red = rgb[0]
            self.green = rgb[1]
            self.blue = rgb[2]
            if(self.red == 255 and self.green == 255 and self.blue == 255):
                self.red = 0
                self.green = 0
                self.blue = 0
                self.w = 255
                set__data = f"0,{self.red},{self.green},{self.blue},{self.w},{self.brightness};" 
                self.serial.write(set__data.encode('utf-8'))
                self.color__extended.setStyleSheet(f"background-color: rgb(255,255,255)")
            else:
                self.w = 0
                set__data = f"0,{self.red},{self.green},{self.blue},{self.w},{self.brightness};"
                self.serial.write(set__data.encode('utf-8'))
                self.color__extended.setStyleSheet(f"background-color: rgb({self.red},{self.green},{self.blue})")
        else:
            rgb = name.split(',')
            self.red = int(rgb[0])
            self.green = int(rgb[1])
            self.blue = int(rgb[2])
            if(self.red == 255 and self.green == 255 and self.blue == 255):
                self.red = 0
                self.green = 0
                self.blue = 0
                self.w = 255
                set__data = f"0,{self.red},{self.green},{self.blue},{self.w},{self.brightness};"
                self.serial.write(set__data.encode('utf-8')) 
                self.color__extended.setStyleSheet(f"background-color: rgb(255,255,255)")
            else:
                self.w = 0
                set__data = f"0,{self.red},{self.green},{self.blue},{self.w},{self.brightness};"
                self.serial.write(set__data.encode('utf-8'))
                self.color__extended.setStyleSheet(f"background-color: rgb({self.red},{self.green},{self.blue})")

    def f_color__brightness(self):
        self.brightness = self.color__brightness_slider.value()
        set__data = f"0,{self.red},{self.green},{self.blue},{self.w},{self.brightness};"
        self.serial.write(set__data.encode('utf-8'))

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
        # self.text.setText(f"{data}")
        print(data)
    
    # def testtt(self):
    #     print(self.sender().objectName())
    #     rgb = self.sender().objectName().split(',')
    #     r = rgb[0]
    #     g = rgb[1]
    #     b = rgb[2]
    #     self.color__extended.setStyleSheet(f"background-color: rgb({r},{g},{b})")

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