import serial


class aSerial:
    def __init__(self, p, b):
        self.ser = serial.Serial(  # 下面这些参数根据情况修改
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
            if n:
                break;

        data += self.ser.read(n).decode()
        if data != '':
            print(data)
        self.ser.close()
        return data

    def write(self, data):
        self.ser.write(data)

    def close_serial(self):
        self.ser.close()
