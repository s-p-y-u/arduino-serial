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

new__port = Ports()
print(new__port.get__ports())
print(new__port.get__ports_quantities())
print(new__port.get__ports_info())
print(new__port.get__port_info(0))
print(new__port.get__speeds())
    
print("Enter 1 to turn ON LED and 0 to turn OFF LED")
arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(1)
while 1:
    datafromUser = input()
    if datafromUser == '1':
        arduino.write(b'0,1;')
        print("LED  turned ON")
    elif datafromUser == '0':
        arduino.write(b'0,0;')
        print("LED turned OFF")
    elif datafromUser == 'exit':
        break