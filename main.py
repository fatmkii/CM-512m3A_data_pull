import tkinter as tk
import tkinter.messagebox
import serial
import serial.tools.list_ports
import time
import csv
import threading as th

VERSION = '0.83beta'
info = 'CM-512m3A色差计 数据提取  ' + VERSION + '\r\n' + '2020年7月' + '\r\n' + '作者:fat  邮箱:47155837@qq.com' + '\r\n' + '欢迎交流意见'


class window:
    flag = False  # 是否在处于收集状态的记号，非收集=false，收集中=true

    def __init__(self):
        self.Ser_read = ser_read(self)

        # 初始框的声明
        self.root = tk.Tk()
        self.root.title('CM-512m3A色差计 数据提取 ' + VERSION)
        self.root.geometry('900x450')
        self.root.resizable(False, False)
        self.com_var = tk.StringVar(value='auto')

        # 菜单栏
        menubar = tk.Menu(self.root)  # 在root添加菜单栏
        com_menu = tk.Menu(menubar, tearoff=0)  # 在菜单栏中添加菜单项
        menubar.add_cascade(label='端口选择', menu=com_menu)
        com_menu.add_radiobutton(label='自动获取', variable=self.com_var, value='auto', command=None)
        com_menu.add_separator()
        com_menu.add_radiobutton(label='COM1', variable=self.com_var, value='COM1', command=None)
        com_menu.add_radiobutton(label='COM2', variable=self.com_var, value='COM2', command=None)
        com_menu.add_radiobutton(label='COM3', variable=self.com_var, value='COM3', command=None)
        com_menu.add_radiobutton(label='COM4', variable=self.com_var, value='COM4', command=None)
        com_menu.add_radiobutton(label='COM5', variable=self.com_var, value='COM5', command=None)
        com_menu.add_radiobutton(label='COM6', variable=self.com_var, value='COM6', command=None)
        self.root.config(menu=menubar)
        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label='关于', command=self.show_info)

        # fm1包括3个按钮
        fm1 = tk.Frame(self.root)
        self.button1 = tk.Button(fm1, text="开始", command=self.read_button_click, height=1, width=10, font=('微软雅黑', 12))
        self.button1.pack(side='left', padx=10, pady=5)
        button2 = tk.Button(fm1, text="输出CSV", command=self.Ser_read.to_csv, height=1, width=10, font=('微软雅黑', 12))
        button2.pack(side='left', padx=10, pady=5)
        button3 = tk.Button(fm1, text="退出", command=self.root_exit, height=1, width=10, font=('微软雅黑', 12))
        button3.pack(side='right', padx=10, pady=5)
        fm1.pack(side='top', fill='x')

        # fm2是文本框
        fm2 = tk.Frame(self.root)
        self.text = tk.Text(fm2, width='85', height=16, font=('微软雅黑', 12))
        self.text.pack(fill='both', padx=10, pady=10)
        fm2.pack(side='top', fill='x')

        # fm3是最底部消息栏
        fm3 = tk.Frame(self.root)
        self.label1 = tk.Label(fm3, text='', font=('微软雅黑', 12), width=20, height=1, anchor='w', padx=5, pady=5)
        self.label1.pack(side='left', anchor='w')
        self.label2 = tk.Label(fm3, text='', font=('微软雅黑', 12), width=30, height=1, anchor='w', padx=5, pady=5)
        self.label2.pack(side='left', anchor='w')
        fm3.pack(side='top', fill='x')

        # 关联窗口x按钮，使设置flag=Flase
        self.root.protocol('WM_DELETE_WINDOW', self.root_exit)

    def start(self):
        self.root.mainloop()  # 进入消息循环

    def text_insert(self, list):
        for data in list:
            self.text.insert('end', str(data))
            self.text.insert('end', '\t')
        self.text.insert('end', '\n')
        self.text.see('end')

    def text_clear(self):
        self.text.delete('1.0', 'end')

    def read_button_click(self):
        if not self.flag:
            self.flag = True
            self.button1.configure(text='停止')
            proc1 = th.Thread(target=self.Ser_read.start)
            proc1.start()
        else:
            self.button1.configure(text='开始')
            self.set_label1('')
            self.set_label2('')
            self.Ser_read.stop()
            self.flag = False

    def root_exit(self):
        self.Ser_read.stop()
        self.root.destroy()

    def set_label1(self, str):
        self.label1.configure(text=str)

    def set_label2(self, str):
        self.label2.configure(text=str)

    def show_info(self):
        tk.messagebox.showinfo('', info)


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


class ser_read:
    flag = False  # 是否在处于收集状态的记号，非收集=false，收集中=true
    data_sheet = []  # 全部收集到的数据都写到这里，最后用于输出csv

    def __init__(self, window):
        self.GUI = window

    def start(self):
        self.flag = True
        self.GUI.text_clear()# 清空文本框
        # 在data_sheet中创建表头
        self.data_sheet = [['', 'L25', 'L45', 'L75', 'a25', 'a45', 'a75', 'b25', 'b45', 'b75', '时间']]
        # 在界面输入表头
        self.GUI.text_insert(self.data_sheet[0])

        if self.GUI.com_var.get() == 'auto':
            port_list = list(serial.tools.list_ports.comports())
            if len(port_list) == 0:
                tk.messagebox.showerror('错误', '未能找到端口，请检查线路或尝试手动选择')
                self.GUI.read_button_click()
                return
            else:
                port = list(port_list[0])[0]
                self.GUI.set_label1("使用端口:" + port)
                COM = Ser(19200, port)
        else:
            port = self.GUI.com_var.get()
            self.GUI.set_label1("使用端口:" + port)
            COM = Ser(19200, port)

        while COM.port.is_open:
            if COM.port.in_waiting > 50:  # 当待读取数据＞50字节时才读取，以提高稳定性
                data_frame = []
                self.GUI.set_label2('正在接受数据')
                for i in range(8):
                    data_frame.append(COM.read_cmd().decode('utf-8', "ignore"))
                    time.sleep(0.1)
                data_row = self.frame_to_row(data_frame)
                self.data_sheet.append(data_row)
                GUI.text_insert(data_row)
            if not self.flag:
                break
            self.gif()
            time.sleep(0.1)

    def stop(self):
        self.flag = False

    @staticmethod
    def frame_to_row(Frame):
        # 将从色差计读取的8行数据，抽出有用的数据列为一行
        Row = [Frame[1].split()[0]]  # 数据序号"NO.?"
        for i in range(3, 6):  # i代表L/a/b行
            for j in range(1, 4):  # j代表25/45/75
                Row.append(Frame[i].split()[j])  # L/a/b值25/45/75数据
        Row.append(Frame[6].splitlines()[0][1:-1].replace('.', '/'))  # 测量时间，[1:-1]为文本切片，去掉头尾的[]
        return Row

    def to_csv(self):
        with open('./色差数据.csv', 'wt', newline='') as fout:
            csvout = csv.writer(fout)
            csvout.writerows(self.data_sheet)
            tk.messagebox.showinfo('', '已保存CSV')

    def gif(self):
        if self.GUI.label2.cget('text') == '' or self.GUI.label2.cget('text') == '正在接受数据':
            self.GUI.set_label2("正在通讯")
        self.GUI.set_label2(self.GUI.label2.cget('text') + '…')
        if len(self.GUI.label2.cget('text')) > 15:
            self.GUI.set_label2("正在通讯")


if __name__ == '__main__':
    # TODO:输出exe
    GUI = window()
    GUI.start()
