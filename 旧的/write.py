import serial
import serial.tools.list_ports

class Ser(object):
    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    def __init__(self, port):
        self.port = serial.Serial(
            port=port,
            baudrate=19200,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.2
        )

    def send_cmd(self, cmd):
            self.port.write(bytes(cmd, encoding='utf-8'))

    def read_cmd(self):
        response = self.port.readline()
        return response.decode('utf-8')

    def read_num(self, num):
        response = self.port.read(num)
        return response


if __name__ == '__main__':
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])

    COM3 = Ser(list(port_list[1])[0])

    try:
        while True:
            msg = input("输入发送内容：")
            if msg == "":
                break
            COM3.send_cmd(msg+'\n')
    except Exception as e:
        print("---异常---：", e)
