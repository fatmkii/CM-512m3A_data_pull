import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTableWidget, QHBoxLayout, QTableWidgetItem, QComboBox, \
    QFrame
from PyQt5.QtGui import QFont, QColor, QBrush, QPixmap


class TableSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        horizontalHeader = ["工号", "姓名", "性别", "年龄", "职称"]

        self.table = QTableWidget()  # 也可以QTableWidget(5,2)
        self.table.setColumnCount(5)  # 5列
        self.table.setRowCount(2)  # 3行
        # 隐藏垂直的表头，self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(horizontalHeader)  # 水平表头，垂直表头setVerticalHeaderLabels()

        # 表格中的数据，默认只要双击就可以修改其中的数据。
        # 如果文档是处于预览状态或者不可编辑状态，那就需要对表格设定为不可编辑模式。
        # QTableWidget.NoEditTriggers 0 不能对表格内容进行修改
        # QTableWidget.CurrentChanged 1 任何时候都能对单元格修改
        # QTableWidget.DoubleClicked 2 双击单元格
        # QTableWidget.SelectedClicked 4 单击已选中的内容
        # QTableWidget.EditKeyPressed 8  编辑键被按下时，编辑开始
        # QTableWidget.AnyKeyPressed 16 按下任意键就能修改
        # QTableWidget.AllEditTriggers 31 以上条件全包括
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # QTableWidget.SelectItems 0 选中单个单元格
        # QTableWidget.SelectRows 1 选中一行
        # QTableWidget.SelectColumns 2 选中一列
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)

        # 设定的选择模式：
        # QTableWidget.NoSelection 不能选择
        # QTableWidget.SingleSelection 选中单个目标
        # QTableWidget.MultiSelection 选中多个目标
        # QTableWidget.ExtendedSelection shift键的连续选择
        # QTableWidget.ContiguousSelection ctrl键的不连续的多个选择
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        # 表头也是由多个item构成的，所以通过循环操作对每一个item进行操作
        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            # 单元格对齐方式：
            # 水平方向：
            # Qt.AlignLeft 0x000  左对齐
            # Qt.AlignRight 0x0002 右对齐
            # Qt.AlignHCenter 0x0004 居中对齐
            # Qt.AlignJustify 0x0008
            # 垂直方向：
            # Qt.AlignTop 0x0020 上对齐
            # Qt.AlignBottom 0x0040 下对齐
            # Qt.AlignVCenter 0x0080 居中
            headItem.setTextAlignment(0x000 | Qt.AlignVCenter)

        # 根据内容自动调整单元格大小
        # self.table.resizeColumnsToContents()
        # self.table.resizeRowsToContents()
        self.table.setColumnWidth(4, 200)  # 设置第5列宽度200
        self.table.setRowHeight(0, 40)  # 设置第一行高度40

        # self.table.setFrameShape(QFrame.HLine)#设定样式
        # self.table.setShowGrid(False)  # False不显示网格线，True显示网格线

        # 添加内容
        self.table.setItem(0, 0, QTableWidgetItem("001"))
        self.table.setItem(0, 1, QTableWidgetItem("Tom"))
        # 表项——添加自定义控件
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(0)
        self.table.setCellWidget(0, 2, genderComb)

        self.table.setItem(0, 3, QTableWidgetItem("30"))
        self.table.setItem(0, 4, QTableWidgetItem("产品经理"))

        self.table.setItem(1, 0, QTableWidgetItem("005"))
        self.table.setItem(1, 1, QTableWidgetItem("Kitty"))
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(1)
        self.table.setCellWidget(1, 2, genderComb)
        self.table.setItem(1, 3, QTableWidgetItem("24"))
        self.table.setItem(1, 4, QTableWidgetItem("程序猿安慰师"))

        # 动态插入行列 insertColumn()插入列
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        # 动态移除行列
        # removeColumn(int column) 移除column列及其内容。
        # removeRow(int row)移除第row行及其内容。
        # row_count = self.table.rowCount()
        # self.table.removeRow(row_count-1)

        # clear() 清除所有表项及表头
        # setSpan(int , int , int , int )，合并单元格

        # 获取单元格内容：
        # self.tableWidget.item(rowindex, colindex).text()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = TableSheet()
    table.setWindowTitle('TableWidget Usage')
    table.resize(700, 300)
    table.show()
    sys.exit(app.exec_())