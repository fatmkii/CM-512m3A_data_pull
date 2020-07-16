import serial
import serial.tools.list_ports
import time
import csv


class Ser(object):
    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    def __init__(self, baud_rate, port):
        self.port = serial.Serial(
            port=port,
            baudrate=baud_rate,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0
        )

    def send_cmd(self, cmd):
        self.port.write(bytes(cmd, encoding='utf-8'))

    def read_cmd(self):
        response = self.port.readline()
        return response

    def read_num(self, num):
        response = self.port.read(num)
        return response


def frame_to_row(Frame):
    # 将从色差计读取的8行数据，抽出有用的数据列为一行
    Row = [Frame[1].split()[0]]  # 数据序号"NO.?"
    for i in range(3, 6):  # i代表L/a/b行
        for j in range(1, 4):  # j代表25/45/75
            Row.append(Frame[i].split()[j])  # L/a/b值25/45/75数据
    Row.append(Frame[6].splitlines()[0][1:-1].replace('.', '/'))  # 测量时间，[1:-1]为文本切片，去掉头尾的[]
    return Row




if __name__ == '__main__':

    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])

    COM = Ser(19200, list(port_list[0])[0])

    while COM.port.is_open:
        if COM.port.in_waiting > 50:  # 当待读取数据＞50字节时才读取，以提高稳定性
            data_frame = []
            for i in range(8):
                data_frame.append(COM.read_cmd().decode('utf-8', "ignore"))
                time.sleep(0.1)
            data_row = frame_to_row(data_frame)
            print(data_row)
            with open('../色差数据.csv', 'wt', newline='') as fout:
                csvout = csv.writer(fout)
                csvout.writerow(data_row)
            break
        time.sleep(0.1)
