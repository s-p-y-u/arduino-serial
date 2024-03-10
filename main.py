import sys
from PySide6 import QtCore, QtWidgets, QtGui
import serial
import serial.tools.list_ports
import time


class Ports:
    speeds = ('1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200')    # скорость портов в кортеже
    def __init__(self):
        self.__ports = list()    # создаем пустой список, можно было использовать []
        self.__ports = list(serial.tools.list_ports.comports())  # Получаем список доступных Serial портов
        self.__speed = ''

    def update__ports_list(self):
        self.__ports = list(serial.tools.list_ports.comports())  # Получаем список доступных Serial портов
    def get__ports(self):
        return self.__ports
    def get__ports_quantities(self):
        return len(self.__ports)

    def get__ports_info(self):
        # Выводим информацию о каждом порте
        info__list = []
        for index ,port in enumerate(self.__ports):
            info = f"Индекс: {index} / Порт: {port.device} / Описание: {port.description} / Производитель: {port.manufacturer}"
            info__list.append(info)
        return info__list
    def get__port_info(self, ind):
        # Выводим информацию о порте
        info = f"Порт: {self.__ports[ind].device} / Описание: {self.__ports[ind].description} / Производитель: {self.__ports[ind].manufacturer}"
        return info

    def get__speeds(self):
        return Ports.speeds

# new__port = Ports()
# print(new__port.get__ports())
# print(new__port.get__ports_quantities())
# print(new__port.get__ports_info())
# print(new__port.get__port_info(0))
# print(new__port.get__speeds())



# print("Enter 1 to turn ON LED and 0 to turn OFF LED")
# arduino = serial.Serial('/dev/ttyUSB0', 9600)
# time.sleep(1)
# while 1:
#     datafromUser = input()
#     if datafromUser == '1':
#         arduino.write(b'0,1;')
#         print("LED  turned ON")
#     elif datafromUser == '0':
#         arduino.write(b'0,0;')
#         print("LED turned OFF")
#     elif datafromUser == 'exit':
#         break


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.new__port = Ports()
        print("------------")
        print(self.new__port)
        print(self.new__port.get__ports())
        if(self.new__port.get__ports()):
            self.arduino__nano_v3 = serial.Serial('/dev/ttyUSB0', 9600)
        # self.new__port.get__ports()
        # self.new__port.get__ports_quantities()
        # self.new__port.get__ports_info()
        # self.new__port.get__port_info(0)
        # self.new__port.get__speeds()

        self.btn__led_2 = QtWidgets.QPushButton("on2")
        self.btn__led_3 = QtWidgets.QPushButton("on3")
        self.btn__led_4 = QtWidgets.QPushButton("on4")
        self.btn__led_5 = QtWidgets.QPushButton("on5")
        self.btn__led_6 = QtWidgets.QPushButton("on6")

        self.btn__led_8 = QtWidgets.QPushButton("on8")
        self.btn__led_9 = QtWidgets.QPushButton("on9")
        self.btn__led_10 = QtWidgets.QPushButton("on10")
        self.btn__led_11 = QtWidgets.QPushButton("on11")

        self.btn__led_2.setObjectName("2")
        self.btn__led_3.setObjectName("3")
        self.btn__led_4.setObjectName("4")
        self.btn__led_5.setObjectName("5")
        self.btn__led_6.setObjectName("6")

        self.btn__led_8.setObjectName("8")
        self.btn__led_9.setObjectName("9")
        self.btn__led_10.setObjectName("10")
        self.btn__led_11.setObjectName("11")

        self.text = QtWidgets.QLabel(f"{self.new__port.get__ports_info()}",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btn__led_2)
        self.layout.addWidget(self.btn__led_3)
        self.layout.addWidget(self.btn__led_4)
        self.layout.addWidget(self.btn__led_5)
        self.layout.addWidget(self.btn__led_6)

        self.layout.addWidget(self.btn__led_8)
        self.layout.addWidget(self.btn__led_9)
        self.layout.addWidget(self.btn__led_10)
        self.layout.addWidget(self.btn__led_11)


        # self.btn__led_1.clicked.connect(lambda: self.on(self.btn__led_1))

        self.btn__led_2.clicked.connect(self.on)
        self.btn__led_3.clicked.connect(self.on)
        self.btn__led_4.clicked.connect(self.on)
        self.btn__led_5.clicked.connect(self.on)
        self.btn__led_6.clicked.connect(self.on)

        self.btn__led_8.clicked.connect(self.on)
        self.btn__led_9.clicked.connect(self.on)
        self.btn__led_10.clicked.connect(self.on)
        self.btn__led_11.clicked.connect(self.on)

    @QtCore.Slot()
    def on(self):
        pin = str(self.sender().objectName())
        
        set = f"{pin},1;"
        self.text.setText(set)
        self.arduino__nano_v3.write(set.encode('utf-8'))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())