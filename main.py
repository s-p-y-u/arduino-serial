from PySide6 import QtWidgets
import serial
import serial.tools.list_ports
import time
import sys
# import glob



# def serial_ports():
#  """ Lists serial port names
#
#      :raises EnvironmentError:
#          On unsupported or unknown platforms
#      :returns:
#          A list of the serial ports available on the system
#  """
#  if sys.platform.startswith('win'):
#   ports = ['COM%s' % (i + 1) for i in range(256)]
#  elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#   # this excludes your current terminal "/dev/tty"
#   ports = glob.glob('/dev/tty[A-Za-z]*')
#  elif sys.platform.startswith('darwin'):
#   ports = glob.glob('/dev/tty.*')
#  else:
#   raise EnvironmentError('Unsupported platform')
#
#  result = []
#  for port in ports:
#   try:
#    s = serial.Serial(port)
#    s.close()
#    result.append(port)
#   except (OSError, serial.SerialException):
#    pass
#  return result
#
# speeds = ('1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200')
# print(serial_ports())
# arduino = serial.Serial('COM6', int(speeds[3]))

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
arduino = serial.Serial('COM5', 9600)
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


 # # Открываем Serial порт ('COMX' замените на имя вашего порта)
 # ser = serial.Serial('COM6', 9600)
 # # Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
 # ser.write(b'0,1;')
 # # Читаем ответ от Arduino через Serial порт
 # response = ser.readline()
 # # Декодируем ответ из байтов в строку с использованием UTF-8
 # decoded_response = response.decode('utf-8')
 # # Закрываем порт
 # ser.close()
 # print(decoded_response)

# if __name__ == '__main__':
#     print_hi('PyCharm')


