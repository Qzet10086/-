import re
import sys
from PyQt5.QtWidgets import QWidget, QTableView, QAbstractItemView, QToolTip, qApp, QPushButton, QLabel, QVBoxLayout, \
    QHBoxLayout, QApplication, QMainWindow, QHeaderView, QMessageBox

from PyQt5.QtCore import QStringListModel, QMetaObject, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor, QFont, QPainter

from mainWindows import *
from algorithm import *
import json

import io
from contextlib import redirect_stdout


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rowNum = 0
        self.realText = ''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.messagelist = []  # 展示信息
        self.messagelist2 = []  # 展示信息
        self.messagelist3 = []
        self.messagelist4 = []
        self.messagelist5 = []
        self.messagelist6 = []
        #self.messagelist7=[]
        self.messagelist8 = []
        self.messagelist9 = []
        self.messagelist10 = []
        self.messagelist11 = []
        self.messagelist12 = []


        self.slm = QStringListModel()               #输出框
        self.slm.setStringList(self.messagelist)
        self.ui.listView.setModel(self.slm)

        self.slm2 = QStringListModel()              #输出框
        self.slm2.setStringList(self.messagelist2)
        self.ui.listView_2.setModel(self.slm2)

        self.slm3 = QStringListModel()  # 输出框
        self.slm3.setStringList(self.messagelist3)
        self.ui.listView_3.setModel(self.slm3)

        self.slm4 = QStringListModel()  # 输出框
        self.slm4.setStringList(self.messagelist4)
        self.ui.listView_4.setModel(self.slm4)

        self.slm5 = QStringListModel()  # 输出框
        self.slm5.setStringList(self.messagelist5)
        self.ui.listView_5.setModel(self.slm5)

        self.slm6 = QStringListModel()  # 输出框
        self.slm6.setStringList(self.messagelist6)
        self.ui.listView_6.setModel(self.slm6)

        self.slm8=QStringListModel()
        self.slm8.setStringList(self.messagelist8)
        self.ui.listView_8.setModel(self.slm8)

        self.slm9 = QStringListModel()
        self.slm9.setStringList(self.messagelist9)
        self.ui.listView_9.setModel(self.slm9)

        self.slm10 = QStringListModel()
        self.slm10.setStringList(self.messagelist10)
        self.ui.listView_10.setModel(self.slm10)

        self.slm11 = QStringListModel()
        self.slm11.setStringList(self.messagelist11)
        self.ui.listView_11.setModel(self.slm11)

        self.slm12 = QStringListModel()
        self.slm12.setStringList(self.messagelist12)
        self.ui.listView_12.setModel(self.slm12)

        self.ui.pushButton_3.setObjectName("runBtn")
        self.ui.pushButton_4.setObjectName("cleanBtn")

        self.ui.pushButton_5.setObjectName("runBtn2")
        self.ui.pushButton_6.setObjectName("cleanBtn2")

        self.ui.pushButton_8.setObjectName("runBtn3")
        self.ui.pushButton_7.setObjectName("cleanBtn3")

        self.ui.pushButton_10.setObjectName("runBtn4")
        self.ui.pushButton_9.setObjectName("cleanBtn4")

        self.ui.pushButton_12.setObjectName("runBtn5")
        self.ui.pushButton_11.setObjectName("cleanBtn5")
        QMetaObject.connectSlotsByName(self)

        # 隐藏窗口
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

    # tab1  词法分析器
    @pyqtSlot()
    def on_runBtn_clicked(self):
        self.doAnalysis()

    @pyqtSlot()
    def on_cleanBtn_clicked(self):
        self.ui.textEdit.setPlainText('')
        self.messagelist.clear()
        self.slm.setStringList(self.messagelist)

    # tab2  NFA转换DFA
    @pyqtSlot()
    def on_runBtn2_clicked(self):
        self.doAnalysis2()


    @pyqtSlot()
    def on_cleanBtn2_clicked(self):
        self.ui.textEdit_2.setPlainText('')
        self.ui.textEdit_3.setPlainText('')
        self.ui.textEdit_4.setPlainText('')
        self.ui.textEdit_5.setPlainText('')
        self.ui.textEdit_6.setPlainText('')
        self.ui.textEdit_7.setPlainText('')
        self.messagelist2.clear()
        self.slm2.setStringList(self.messagelist2)

    #tab3   first集合计算
    @pyqtSlot()
    def on_runBtn3_clicked(self):
        self.doAnalysis3()

    @pyqtSlot()
    def on_cleanBtn3_clicked(self):
        self.ui.textEdit_8.setPlainText('')
        self.messagelist3.clear()
        self.slm3.setStringList(self.messagelist3)


    #tab4 算符优先表达式分析器
    @pyqtSlot()
    def on_runBtn4_clicked(self):
        self.doAnalysis4()

    @pyqtSlot()
    def on_cleanBtn4_clicked(self):
        self.ui.textEdit_10.setPlainText('')
        self.ui.listView_7.setPlainText('')

        self.messagelist4.clear()
        self.slm4.setStringList(self.messagelist4)
        self.messagelist5.clear()
        self.slm5.setStringList(self.messagelist5)
        self.messagelist6.clear()
        self.slm6.setStringList(self.messagelist6)


    @pyqtSlot()
    def on_runBtn5_clicked(self):
        self.doAnalysis5()

    @pyqtSlot()
    def on_cleanBtn5_clicked(self):
        self.ui.textEdit_11.setPlainText('')
        self.ui.textEdit_12.setPlainText('')

        self.messagelist8.clear()
        self.slm8.setStringList(self.messagelist8)
        self.messagelist9.clear()
        self.slm9.setStringList(self.messagelist9)
        self.messagelist10.clear()
        self.slm10.setStringList(self.messagelist10)
        self.messagelist11.clear()
        self.slm11.setStringList(self.messagelist11)
        self.messagelist12.clear()
        self.slm12.setStringList(self.messagelist12)

    def annotation5(self):
        text0=self.ui.textEdit_13.toPlainText()
        self.realText13=text0

        text1=self.ui.textEdit_12.toPlainText()
        self.realText12=text1


    def doAnalysis5(self):
        grammar = [
            ('S\'', 'E'),
            ('E', '(L)'),
            ('E', 'a'),
            ('L', 'L,E'),
            ('L', 'E')
        ]
        self.annotation5()
        self.analysis5=SLR(grammar)

        a1=io.StringIO()
        with redirect_stdout(a1):
            self.analysis5.print_follow_sets()
        output1 = a1.getvalue()
        a1.close()

        a2 = io.StringIO()
        with redirect_stdout(a2):
            self.analysis5.print_states()
        output2 = a2.getvalue()
        a2.close()

        a3 = io.StringIO()
        with redirect_stdout(a3):
            self.analysis5.print_goto_function()
        output3= a3.getvalue()
        a3.close()

        a4 = io.StringIO()
        with redirect_stdout(a4):
            self.analysis5.print_action_table()
        output4 = a4.getvalue()
        a4.close()

        a5 = io.StringIO()
        with redirect_stdout(a5):
            self.analysis5.print_goto_table()
        output5 = a5.getvalue()
        a5.close()

        a6 = io.StringIO()
        with redirect_stdout(a6):
            self.analysis5.slr1_parser(self.realText12)
        output6 = a6.getvalue()
        a6.close()

        self.messagelist9.append(output1)
        self.slm9.setStringList(self.messagelist9)

        self.messagelist11.append(output2)
        self.slm11.setStringList(self.messagelist11)

        self.messagelist8.append(output5)
        self.slm8.setStringList(self.messagelist8)

        self.messagelist10.append(output4)
        self.slm10.setStringList(self.messagelist10)

        self.messagelist12.append(output3)
        self.slm12.setStringList(self.messagelist12)

        self.ui.textEdit_11.setPlainText(output6)


    def annotation4(self):
        text1 = self.ui.textEdit_9.toPlainText()

        text2 = self.ui.textEdit_10.toPlainText()
        self.realText9=text1
        self.realText10=text2


    def doAnalysis4(self):
        self.annotation4()
        self.analysis4=Op()
        self.analysis4.data_input(self.realText9)

        a = io.StringIO()  # 重定向，将print内容存入output
        with redirect_stdout(a):
            self.analysis4.print_firstVT()
        output1 = a.getvalue()
        print(output1)
        a.close()

        b = io.StringIO()  # 重定向，将print内容存入output
        with redirect_stdout(b):
            self.analysis4.print_lastVT()
        output2 = b.getvalue()
        b.close()

        c = io.StringIO()  # 重定向，将print内容存入output
        with redirect_stdout(c):
            self.analysis4.print_Optable()
        output3 = c.getvalue()
        c.close()

        d = io.StringIO()  # 重定向，将print内容存入output
        with redirect_stdout(d):
            self.analysis4.input(self.realText10)
        output4 = d.getvalue()
        d.close()

        self.messagelist4.append(output1)
        self.slm4.setStringList(self.messagelist4)

        self.messagelist5.append(output2)
        self.slm5.setStringList(self.messagelist5)

        self.messagelist6.append(output3)
        self.slm6.setStringList(self.messagelist6)

        self.ui.listView_7.setPlainText(output4)



    def annotation3(self):
        text =self.ui.textEdit_8.toPlainText()

        # 初始化空的文法字典
        grammar = {}
        # E->TA
        # T->FB
        # A->~ | +TA
        # B->*FB | ~
        # F->(E) | i
        # 按行分割输入文本
        lines = text.strip().split('\n')

        # 遍历每一行
        for line in lines:
            # 分割非终结符和产生式
            non_terminal, productions_str = line.split('->')
            non_terminal = non_terminal.strip()
            # 按 '|' 分割不同的产生式
            productions = productions_str.strip().split('|')
            production_list = []
            # 处理每个产生式
            for production in productions:
                # 使用正则表达式分割产生式为符号列表
                symbols = re.findall(r'[a-zA-Z~+\-*/()i]', production.strip())
                production_list.append(symbols)
            # 将非终结符和对应的产生式列表添加到文法字典中
            grammar[non_terminal] = production_list
        self.realText8=grammar


    def doAnalysis3(self):
        self.annotation3()
        #print(self.realText8)
        # grammar = {
        #     'E': [['T', 'A']],
        #     'T': [['F', 'B']],
        #     'A': [['~'], ['+', 'T', 'A']],
        #     'B': [['*', 'F', 'B'], ['~']],
        #     'F': [['(', 'E', ')'], ['i']]
        # }
        #
        self.analysis3 = Calculate_First(self.realText8)
        self.analysis3.print_first()

        f = io.StringIO()  # 重定向，将print内容存入output
        with redirect_stdout(f):
            self.analysis3.print_first()
        output = f.getvalue()
        f.close()

        self.messagelist3.append(output)
        self.slm3.setStringList(self.messagelist3)




    def annotation2(self):
        text2 = self.ui.textEdit_2.toPlainText()        #状态集
        text3 = self.ui.textEdit_3.toPlainText()        #符号集
        text4 = self.ui.textEdit_4.toPlainText()        #终态
        text5 = self.ui.textEdit_5.toPlainText()        #初态
        text6 = self.ui.textEdit_6.toPlainText()        #弧数
        text7 = self.ui.textEdit_7.toPlainText()        #弧

        self.realText2 = text2
        self.realText3 = text3
        self.realText4 = text4
        self.realText5 = text5
        self.realText6 = text6
        self.realText7 = text7


    def doAnalysis2(self):
        self.annotation2()
        data2 = self.realText2.split()
        data3 = self.realText3.split()
        data4 = self.realText4.split()
        data5 = self.realText5.split()
        data6 = self.realText6.split()
        data7 = self.realText7.split()
        #print("开始分析", data2)
        self.analysis2 = NFAAnalyzer(data2,data3,data4,data5,data6,data7)
        self.analysis2.NFA2DFA()
        f=io.StringIO()                     #重定向，将print内容存入output
        with redirect_stdout(f):
            self.analysis2.print_DFA()
        output =f.getvalue()
        print(output)
        f.close()

        self.messagelist2.append(output)

        self.slm2.setStringList(self.messagelist2)


#tab1
    def annotation(self):
        text = self.ui.textEdit.toPlainText()
        self.rowNum = 1
        start = 0
        while True:
            start = text.find('\\n', start)
            if start != -1:
                self.rowNum += 1
            else:
                break
        self.ui.label_5.setText(str(self.ui.textEdit.document().lineCount()))               #row
        # print("输入:", text)
        # showText = text
        # index1 = 0
        # index2 = 0
        # while index1 != -1 and index2 != -1:
        #     index1 = text.find('/*', index2)
        #     index2 = text.find('*/', index1)
        #     if index1 != -1 and index1 < index2:
        #         annotationStr = text[index1:index2 + 2]
        #         showText = showText.replace(annotationStr, "<font color=\"#00FF00\">" + annotationStr + "</font>")
        #         text = text.replace(annotationStr, ' ')
        # print("显示:", showText)
        # self.ui.textEdit.setPlainText(showText)
        self.realText = text

    def doAnalysis(self):
        self.annotation()
        data = self.realText.split()
        #print("开始分析", data)
        self.analysis = lexicalAnalyzer(data)
        self.analysis.scan()
        self.ui.label_6.setText(str(self.analysis.charNum))                 #char
        print(self.analysis.result)
        for res in self.analysis.result:
            print(res)
            message = '-----'.join(res)
            print(message)
            self.messagelist.append(message)
            self.slm.setStringList(self.messagelist)        #转换成字符串列表并分行显示


#实现窗口拖动事件
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UserWindow()
    sys.exit(app.exec_())
