import uart
import sqlite3
import cv2
import time
import os
import search
import picamera

class Detection:
    def __init__(self):
        pass

    def status_read_uart(self):
        ser = uart.aSerial('/dev/ttyUSB0', 9600)
        data = ser.read_with_block()
        return data

    def status_read_database(self, code):
        conn = sqlite3.connect('total.db')
        print("Opened database successfully");

        cursor = conn.execute("SELECT dname, code, type, sale FROM drinkcount WHERE=" + code)
        name = ""
        flag = False
        for row in cursor:
            print("dname = ", row[0])
            name = row[0]
        if name != "":
            print("exist")
            flag = True
        else:
            print("do not exist")
        return flag

    def status_sendCMD(self, flag):
        ser = uart.aSerial('/dev/ttyS0', 9600)
        if flag :
            ser.write('0')
        else :
            ser.write('1')
        ser.close_serial()

    def status_wait_response(self):
        ser = uart.aSerial('/dev/ttyS0', 9600)
        data = ser.read_with_block()
        if data == '0':
            return True
        else :
            return False

    def status_take_picture(self):
        camera = picamera.PiCamera()
        filename = os.path.join(os.path.abspath(__file__), 'testpicure', time.strftime("%Y%m%d_%H%M%S.jpg"))
        camera.capture(filename)
        return filename

    def status_match(self, filename):
        ret = search.match(filename)
        ser = uart.aSerial('/dev/ttyS0', 9600)
        ser.write(str(ret))
        ser.close_serial()


if __name__ == "__main__" :
    detect = Detection()
    while(True):
        code = detect.status_read_uart()
        isExist = detect.status_read_database(code)
        detect.status_sendCMD(isExist)

        doPicture = detect.status_wait_response()
        if doPicture:
            picture = detect.status_take_picture()
            detect.status_match(picture)
        else:
            continue



