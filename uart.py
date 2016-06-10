import serial
import time


class aSerial:
    def __init__(self, p, b):
        self.ser = serial.Serial(      
	    port=p,
            baudrate=b,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

    def read_with_block(self):
        flag = True
        data = ''
        while flag:
            n = self.ser.inWaiting()
            if n:break
            time.sleep(0.01)
                # try:
                #     data += self.ser.read(n).decode("ascii")
                #     print(data)
                #     break
                # except serial.SerialException as e:
                #     # There is no new data from serial port
                #     # print("SerialException")
                #     pass
                # except TypeError as e:
                #     # Disconnect of USB->UART occured
                #     # print("typeError")
                #     pass

        data += self.ser.read(n).decode()
        if data != '':
            print(data)
        self.ser.close()
        return data

    def write(self, data):
        self.ser.write(data)

    def close_serial(self):
        self.ser.close()
