import io
from contextlib import redirect_stdout
import re
#实验一 tab1
# 词法分析器的逻辑实现
class lexicalAnalyzer:
    def __init__(self, words):
        self.charNum = 0
        self.state = 0  # 编辑状态 0; 注释状态 -1; 结束状态: 1
        self.keyWord = ["auto", "break", "case", "char", "const", "continue",
                        "default", "do", "double", "else", "enum", "extern",
                        "float", "for", "goto", "if", "int", "long",
                        "register", "return", "short", "signed", "sizeof", "static",
                        "struct", "switch", "typedef", "union", "unsigned", "void",
                        "volatile", "while"]  # 关键字
        self.punctuation = [";", ",", "\"", "\'", "#", "\\", ".", ":"]  # 一般标点符号

        self.Operator = [',', '.', '/', '<', '>', '?', ';', '\'', ':', '\"', '!', '%', '&', '*',
                         '_', '+', '=', '\\', '|', '^', '~', '#']
        self.allOperator = [',', '.', '/', '<', '>', '?', ';', '\'', ':', '\"', '!', '%', '&', '*',
                            '_', '+', '=', '\\', '|', '^', '~', '[', ']', '{', '}', '(', ')', '#']
        self.allOperator2 = [',', '/', '<', '>', '?', ';', '\'', ':', '\"', '!', '%', '&', '*',
                            '_', '+', '=', '\\', '|', '^', '~', '[', ']', '{', '}', '(', ')', '#']
        self.bracket = ['[', ']', '{', '}', '(', ')']

        self.state = 0
        self.words = words  # 初步分组的单词
        self.word = ""  # 得到的单词
        self.stack = []  # 存储扫描到的字符组成单词
        self.typeStatistic = {'keyWord': 0, "digit": 0, "punctuation": 0, "arithmeticOpe": 0, "relationOpe": 0,
                              "identifier": 0, "assigningOpe": 0, "error": 0, "annotation": 0, "bitOpe": 0,
                              "logicOpe": 0, "bracket": 0}  # 类型数量统计
        self.info = {'row': 0, 'charNum': 0, }  # 代码信息
        self.result = []

    def isKeyWord(self, word):
        if word in self.keyWord:
            return True
        else:
            return False

    def isidentifier(self, index, Str):
        if len(Str) == 0:
            self.result.append(['identifier', self.word])
            self.typeStatistic['identifier'] += 1
            self.word = ''
            return

        else:
            i = 0
            for char in Str:
                self.charNum += 1
                if self.state == 1 and (char.isalpha() or char.isdigit() or char == '_'):
                    self.word += char
                elif char in self.allOperator:
                    if self.isKeyWord(self.word):
                        self.result.append(['keyWord', self.word])
                        self.typeStatistic['keyWord'] += 1
                        self.word = ''
                    else:
                        self.result.append(['identifier', self.word])
                        self.typeStatistic['identifier'] += 1
                        self.word = ''
                    self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                    return
                else:
                    self.result.append(['error', char])
                    self.typeStatistic['error'] += 1
                    self.word = ''
                    return
                i += 1

            if self.isKeyWord(self.word):
                self.result.append(['keyWord', self.word])
                self.typeStatistic['keyWord'] += 1
                self.word = ''
            else:
                self.result.append(['identifier', self.word])
                self.typeStatistic['identifier'] += 1
                self.word = ''
            return

    def isDigit(self, index, Str):
        if len(Str) == 0:
            self.result.append(['digit', self.word])
            self.typeStatistic['digit'] += 1
            self.word = ''
            return
        else:
            i = 0
            for char in Str:
                self.charNum += 1
                if (self.state == 2 or self.state == 4 or self.state == 7) and char.isdigit():
                    self.word += char

                elif self.state == 2 and char == '.':
                    self.state = 3
                    self.word += char

                elif self.state == 2 and char == 'E':
                    self.state = 5
                    self.word += char

                elif self.state == 3 and char.isdigit():
                    self.state = 4
                    self.word += char

                elif self.state == 4 and char == 'E':
                    self.state = 5
                    self.word += char
                elif self.state == 5 and (char == '+' or char == '-'):
                    self.state = 6
                    self.word += char
                elif (self.state == 5 or self.state == 6) and char.isdigit():
                    self.state = 7
                    self.word += char
                elif (self.state == 2 or self.state == 4 or self.state == 7) and char in self.allOperator2:
                    self.result.append(['digit', self.word])
                    self.typeStatistic['digit'] += 1
                    self.word = ''
                    self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                    return
                else:
                    self.result.append(['error', char])
                    self.typeStatistic['error'] += 1
                    self.word = ''
                    return
                i += 1
            self.result.append(['digit', self.word])
            self.typeStatistic['digit'] += 1
            self.word = ''
            return

    def isOpe(self, index, Str):
        i = 0
        for char in Str:
            self.charNum += 1
            if self.state == 0 and char == '+':
                self.state = 8
                self.word += char
            elif self.state == 0 and char == '-':
                self.state = 11
                self.word += char
            elif self.state == 0 and char in ['*', '/', '%']:
                self.state = 24
                self.word += char

            elif self.state == 8 and char == '=':
                self.state = 9
                self.word += char
            elif self.state == 8 and char == '+':
                self.state = 10
                self.word += char
            elif self.state == 11 and char == '=':
                self.state = 12
                self.word += char
            elif self.state == 11 and char == '-':
                self.state = 13
                self.word += char
            elif self.state == 24 and char == '=':
                self.state = 25
                self.word += char

            elif self.state == 0 and char == '=':
                self.state = 14
                self.word += char
            elif self.state == 14 and char == '=':
                self.state = 15
                self.word += char
            elif self.state == 0 and char == '!':
                self.state = 36
                self.word += char
            elif self.state == 36 and char == '=':
                self.state = 37
                self.word += char
            elif self.state == 0 and char == '>':
                self.state = 16
                self.word += char
            elif self.state == 0 and char == '<':
                self.state = 19
                self.word += char
            elif self.state == 16 and char == '=':
                self.state = 17
                self.word += char
            elif self.state == 16 and char == '>':
                self.state = 18
                self.word += char
            elif self.state == 18 and char == '=':
                self.state = 22
                self.word += char

            elif self.state == 19 and char == '=':
                self.state = 20
                self.word += char
            elif self.state == 19 and char == '<':
                self.state = 21
                self.word += char
            elif self.state == 21 and char == '=':
                self.state = 23
                self.word += char

            elif self.state == 0 and char == '^':
                self.state = 26
                self.word = char
            elif self.state == 26 and char == '=':
                self.state = 27
                self.word = char

            elif self.state == 0 and char == '&':
                self.state = 28
                self.word = char
            elif self.state == 28 and char == '=':
                self.state = 29
                self.word = char
            elif self.state == 28 and char == '&':
                self.state = 30
                self.word = char

            elif self.state == 0 and char == '|':
                self.state = 31
                self.word = char
            elif self.state == 31 and char == '=':
                self.state = 32
                self.word = char
            elif self.state == 31 and char == '&':
                self.state = 33
                self.word = char

            elif self.state == 0 and char == '~':
                self.state = 34
                self.word = char

            elif self.state == 0 and char in self.punctuation:
                self.state = 35
                self.word = char


            elif self.state in [8, 10, 11, 13, 24] and (char.isdigit() or char.isalpha() or char in self.bracket):
                self.result.append(['arithmeticOpe', self.word])
                self.typeStatistic['arithmeticOpe'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            elif self.state in [9, 12, 14, 25, 22, 23, 27, 29, 32] and (
                    char.isdigit() or char.isalpha() or char in self.bracket):  # 赋值操作符
                self.result.append(['assigningOpe', self.word])
                self.typeStatistic['assigningOpe'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return

            elif self.state in [16, 17, 19, 20] and (char.isdigit() or char.isalpha() or char in self.bracket):
                self.result.append(['relationOpe', self.word])
                self.typeStatistic['relationOpe'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            elif self.state in [18, 21, 26, 28, 31, 34] and (char.isdigit() or char.isalpha() or char in self.bracket):
                self.result.append(['bitOpe', self.word])
                self.typeStatistic['bitOpe'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            elif self.state in [15, 30, 33, 36, 37] and (char.isdigit() or char.isalpha() or char in self.bracket):
                self.result.append(['logicOpe', self.word])
                self.typeStatistic['logicOpe'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            elif self.state == 35 and (char.isdigit() or char.isalpha() or char in self.bracket):
                self.result.append(['punctuation', self.word])
                self.typeStatistic['punctuation'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            else:
                self.result.append(['error', ''.join(Str)])
                self.typeStatistic['error'] += 1
                self.word = ''
                return
            i += 1
        if self.state in [8, 10, 11, 13, 24]:
            self.result.append(['arithmeticOpe', self.word])
            self.typeStatistic['arithmeticOpe'] += 1
            self.word = ''
        elif self.state in [9, 12, 14, 25, 22, 23]:
            self.result.append(['assigningOpe', self.word])
            self.typeStatistic['assigningOpe'] += 1
            self.word = ''

        elif self.state in [16, 17, 19, 20]:
            self.result.append(['relationOpe', self.word])
            self.typeStatistic['relationOpe'] += 1
            self.word = ''

        elif self.state in [18, 21]:
            self.result.append(['bitOpe', self.word])
            self.typeStatistic['bitOpe'] += 1
            self.word = ''
        elif self.state in [15, 30, 33, 36, 37]:
            self.result.append(['logicOpe', self.word])
            self.typeStatistic['logicOpe'] += 1
            self.word = ''
        elif self.state == 35:
            self.result.append(['punctuation', self.word])
            self.typeStatistic['punctuation'] += 1
            self.word = ''
        return

    def isBracket(self, index, Str):
        i = 0
        for char in Str:
            self.charNum += 1
            if self.state == 0 and char in self.bracket:
                self.state = 38
                self.word = char
            else:
                self.result.append(['bracket', self.word])
                self.typeStatistic['bracket'] += 1
                self.word = ''
                self.words.insert(index + 1, Str[i:])  # 插入剩下的单词
                return
            i += 1
        self.result.append(['bracket', self.word])
        self.typeStatistic['bracket'] += 1
        self.word = ''

    # def isBitOpe(self,index,Str):
    #     i = 0
    #     for char in Str
    #         if

    def scan(self):
        index = 0
        flag = 0
        self.charNum = 0
        for word in self.words:
            self.state = 0
            word = list(word)
            if word[0].isalpha():
                self.word += word[0]
                self.state = 1
                self.charNum += 1
                self.isidentifier(index, word[1:])

            elif word[0].isdigit():
                self.word += word[0]
                self.state = 2
                self.charNum += 1
                self.isDigit(index, word[1:])

            elif word[0] in self.Operator:
                self.isOpe(index, word)

            elif word[0] in self.bracket:
                self.isBracket(index, word)
            else:
                self.charNum += 1
                self.result.append(['error', ' '.join(word)])
                self.typeStatistic['error'] += 1
                self.word = ''

            index += 1

#实验二 tab2
# 输入NFA
class NFAAnalyzer:
    def __init__(self,K,E,Z,S,n,F):
        self.K = K
        self.E = [e for e in E if e != "$"]
        self.F = F
        self.S = S
        self.Z = Z
        self.n = n
        self.K_DFA = []  # DFA状态集
        self.fx = []  # 状态转换函数
        self.result=[]
        #print("这里是函数",K,E,F,S,n,Z)
    # def input_NFA(self):
    #     a = input('请输入NFA状态集(以空格区分,以换行结束): ')
    #     K.extend(a.split(' '))
    #     a = input('请输入NFA输入符号集(以空格区分,以换行结束): ')
    #     E.extend(a.split(' '))
    #     a = input('请输入NFA初态集(以空格区分,以换行结束): ')
    #     S.extend(a.split(' '))
    #     a = input('输入NFA终态集(以空格区分,以换行结束): ')
    #     Z.extend(a.split(' '))
    #     print('请输入NFA弧的条数: ')
    #     n = int(input())
    #     print('请输入这些弧(分别输入状态1,输入符号,状态2,以空格区分换行结束,ε表示为$)')
    #     for i in range(n):
    #         a = input()
    #         t = a.split(' ')
    #         F.append(t)
    # ε-closure函数
    def closure(self,I):
        # for i in I:
        #     for f in self.F:
        #         if f[0] == i and f[1] == "$":
        #             if f[2] not in I:
        #                 I.append(f[2])
        # return sorted(I)  # 从小到大排序（按字典）
        closure_set = list(I)
        queue = list(closure_set)
        while queue:
            state = queue.pop(0)
            for f in self.F:
                if f[0] == state and f[1] == "$" and f[2] not in closure_set:
                    closure_set.append(f[2])
                    queue.append(f[2])
        return sorted(closure_set)
    # move(I, a)函数

    def move(self,I, a):
        self.new_I = []
        for i in I:
            for f in self.F:
                if f[0] == i and f[1] == a:
                    if f[2] not in self.new_I:
                        self.new_I.append(f[2])
        return sorted(self.new_I)  # 从小到大排序（按字典）

    # 判断新生成的子集是否存在,存在返回位置，不存在返回-1
    def is_inDFA(self,new_k):
        new_set = set(new_k)
        index = 0
        for k in self.K_DFA:
            old_set = set(k)
            if old_set == new_set:
                return index
            index = index + 1
        return -1

    # 添加到转换函数中
    def myAppend(self,k,e, new_k):
        self.t = []
        self.t.append(k)
        self.t.append(e)
        self.t.append(new_k)
        self.fx.append(self.t)

    # NFA转DFA
    def NFA2DFA(self):
        self.J = self.closure(self.S)  # NFA的初态
        self.K_DFA.append(self.J)
        for k in self.K_DFA:
            for e in self.E:
                self.new_k = self.closure(self.move(k, e))
                if self.new_k is not None:  # 不存在于当前子集中，则加入
                    if self.is_inDFA(self.new_k) == -1:
                        self.K_DFA.append(self.new_k)
                        self.myAppend(self.is_inDFA(k), e, self.is_inDFA(self.new_k))
                    else:  # 存在于当前子集中，则不加入
                        self.myAppend(self.is_inDFA(k), e, self.is_inDFA(self.new_k))

    # 打印DFA
    def print_DFA(self):
        print("NFA子集构造法构造出的子集：")
        for k in self.K_DFA:
            print(self.K_DFA.index(k), end=": ")
            #self.result.append(k,':',self.K_DFA.index(k))
            print(k)
        # 矩阵形式
        print("DFA矩阵表示：",self.E)
        print("\\", end="\t")
        for e in self.E:
            print(e, end="\t")
        print()
        for i in range(len(self.K_DFA)):
            print(i, end="\t")
            for e in self.E:
                for f in self.fx:
                    if i == f[0] and e == f[1]:
                        print(f[2], end="\t")
                        break
                    if self.fx.index(f) == len(self.fx) - 1:
                        print("", end="\t")
            for j in self.K_DFA[i]:
                if j in self.Z:
                    print("(终态)", end=" ")
                    break
            print()

#实验三 tab3
# 计算First集
class Calculate_First:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = {key: set() for key in grammar.keys()}
        self.calculated = {key: False for key in grammar.keys()}
        # 计算所有符号的First集

    def print_first(self):
        for symbol in self.grammar.keys():
            self.calculate_first(symbol)
        # 打印First集
        print("First集:")
        for key, value in self.first_sets.items():
            print(f"First({key}) = {value}")

    def calculate_first(self, symbol):
        # 如果已经计算过，直接返回
        if self.calculated[symbol]:
            return self.first_sets[symbol]

        for production in self.grammar.get(symbol, []):
            for sym in production:
                if sym == '~':
                    self.first_sets[symbol].add('~')
                    break
                elif sym.islower() or sym in('(',')','+','*','i'):  # 终结符
                    self.first_sets[symbol].add(sym)
                    break
                else:  # 非终结符
                    first_of_sym = self.calculate_first(sym)
                    self.first_sets[symbol].update(first_of_sym - {'~'})
                    if '~' not in first_of_sym:  # 如果没有空串，停止推导
                        break
            else:
                self.first_sets[symbol].add('~')  # 如果全都是ε，加入空串

        self.calculated[symbol] = True
        return self.first_sets[symbol]


#实验四 tab4
#算符优先语法分析
class Op:
    def __init__(self):
        self.grammarElement = {}
        self.terSymblo = ['#']  # 终结符列表
        self.non_ter = []  # 非终结符
        self.Start = 'E'  # 开始符号
        self.allSymbol = []  # 所有符号
        self.firstVT = {}  # FIRSTVT集
        self.lastVT = {}  # lastVT集
        self.formules = []
        self.data = {}  # 算符优先分析表
        self.sym = []
        self.sentencePattern = ["N+N", "N*N", "N/N", "(N)", "i", "N^N", "N,N", "N-N", "a"]
        self.analyzeResult = False
        self.analyzeStep = 0
        self.form={
            '#': {'#': '=', 'i': '<'},
            'i': {'+': '>', '#': '>'}
        }
        self.stP = {'i': 'N'}

    def data_input(self,text):  # 读取文法
        try:
            # with open("3.txt", 'r+', encoding="utf-8") as f:
            temp=text.split('\n')
            for i in temp:
                line = str(i.strip("\n"))  # 获取当前行的字符串内容，并移除其尾部的换行符
                self.formules.append(line)  # 将当前文法规则添加到一个名为formules的列表中
                if line[0] not in self.non_ter:  # 检查当前规则的首字符是否已经在non_ter（非终结符号）列表中
                    self.non_ter.append(line[0])
                    # 在grammarElement字典中设置一个键值对。键是当前规则的首字符，值是该规则的右侧部分（从第五个字符开始）。
                    # 如果这个键已经存在于字典中，那么它的值将被更新为当前规则的右侧部分。
                    self.grammarElement.setdefault(line[0], line[5:])
                else:
                    self.grammarElement[line[0]] += "|" + line[5:]
            for i in temp:
                line = str(i.strip("\n")).replace(" -> ", "")
                for j in line:
                    if j not in self.non_ter and j not in self.terSymblo:
                        self.terSymblo.append(j)
            if 'ε' in self.terSymblo:
                self.terSymblo.remove('ε')  # 如果ε存在终结符列表中，则从列表中移除它
            # 初始化FIRSTVT和LASTVT集合
            for i in self.non_ter:
                self.firstVT.setdefault(i, "")
                self.lastVT.setdefault(i, "")
            # 初始化算符优先分析表
            for i in self.terSymblo:
                for j in self.terSymblo:
                    self.addtodict2(self.data, i, j, '')
            self.sym = self.non_ter + self.terSymblo  # 创建一个新的列表sym，它是将non_ter和terSymblo两个列表连接在一起的结果
        # except FileNotFoundError:
        #     print("文件 '3.txt' 未找到，请检查文件路径。")
        except Exception as e:
            print(f"输入处理出错: {e}")

    def get_fistVT(self, formule):
        x = formule[0]  # 获取文法规则的首字符，并将其赋值给变量x
        i = 5
        if formule[i] in self.terSymblo and formule[i] not in self.firstVT[x]:  # 首位为终结符 P->a...
            self.firstVT[x] += formule[i]
        elif formule[i] in self.non_ter:  # 首位为非终结符  P->Q...
            for f in self.firstVT[formule[i]]:  # 如果a属于FIRSTVT(Q)
                if f not in self.firstVT[x]:
                    self.firstVT[x] += f
            if i + 1 < len(formule):  # 非终结符后面一个字符
                if formule[i + 1] in self.terSymblo and formule[i + 1] not in self.firstVT[x]:  # P->Qa...
                    self.firstVT[x] += formule[i + 1]

    def get_lastVT(self, formule):
        x = formule[0]
        i = len(formule) - 1
        if formule[i] in self.terSymblo and formule[i] not in self.lastVT[x]:  # P->...a
            self.lastVT[x] += formule[i]
        elif formule[i] in self.non_ter:  # P->...Q
            for f in self.lastVT[formule[i]]:  # 遍历LastVT(Q)
                if f not in self.lastVT[x]:  # 若a属于LastVT(Q)
                    self.lastVT[x] += f
            if i - 1 >= 0 and formule[i - 1] in self.terSymblo and formule[i - 1] not in self.lastVT[x]:  # P->...aQ
                self.lastVT[x] += formule[i - 1]

    def addtodict2(self, thedict, key_a, key_b, val):  # 设置二维字典的函数
        if key_a in thedict.keys():
            thedict[key_a].update({key_b: val})
        else:
            thedict.update({key_a: {key_b: val}})

    def analy(self, formule):  # 算符优先分析表
        start = 5
        end = len(formule) - 2
        if start == end:
            return
        for i in range(start, end):  # 每个形如 P->X1X2…Xn的产生式
            if formule[i] in self.terSymblo and formule[i + 1] in self.terSymblo:  # Xi和Xi+1都是终结符
                self.addtodict2(self.data, formule[i], formule[i + 1], "=")
            # Xi和Xi+2 是终结符, 但Xi+1 为非终结符
            if i + 2 < len(formule) and formule[i] in self.terSymblo and formule[i + 1] in self.non_ter and formule[i + 2] in self.terSymblo:
                self.addtodict2(self.data, formule[i], formule[i + 2], "=")
            # Xi为终结符, Xi+1为非终结符 ...aP...
            if formule[i] in self.terSymblo and formule[i + 1] in self.non_ter:
                for j in self.firstVT[formule[i + 1]]:  # FirstVT 中的每个元素 b
                    self.addtodict2(self.data, formule[i], j, "<")  # a<b
            # Xi为非终结符, Xi+1为终结符...Pb...
            if formule[i] in self.non_ter and formule[i + 1] in self.terSymblo:
                for j in self.lastVT[formule[i]]:  # LastVT 中的每个元素 a
                    self.addtodict2(self.data, j, formule[i + 1], ">")  # a>b
            if i + 2 < len(formule) and formule[i + 1] in self.terSymblo and formule[i + 2] in self.non_ter:
                for j in self.firstVT[formule[i + 2]]:
                    self.addtodict2(self.data, formule[i + 1], j, "<")
            if i + 2 < len(formule) and formule[i + 1] in self.non_ter and formule[i + 2] in self.terSymblo:
                for j in self.lastVT[formule[i + 1]]:
                    self.addtodict2(self.data, j, formule[i + 2], ">")

    def reverseString(self, string):
        return string[::-1]  # 选择了从末尾到开头的所有字符，从而得到了一个反向的字符串

    # 初始化两个栈
    def initStack(self, string):
        # 分析栈，入栈#
        analysisStack = "#"
        # 当前输入串入栈，即string逆序入栈
        currentStack = self.reverseString(string)
        # 调用分析函数
        self.toAnalyze(analysisStack, currentStack)

    # 寻找分析栈最顶终结符元素，返回该元素及其下标
    def findVTele(self, string):
        ele = '\0'
        ele_index = 0

        for i in range(len(string)):
            if (string[i] in self.terSymblo):
                ele = string[i]
                ele_index = i
        return ele, ele_index

    # 根据栈中内容进行分析,构造算符优先分析表
    def toAnalyze(self, analysisStack, currentStack):
        # global analyzeResult
        # global analyzeStep
        self.analyzeStep += 1
        analysisStack_top, analysisStack_index = self.findVTele(analysisStack)  # 分析栈最顶终结符元素及下标
        currentStack_top = currentStack[-1]  # 当前输入串栈顶
        # relation = data[analysisStack_top][currentStack_top]
        # 根据分析栈顶和当前输入串栈顶，从data中获取对应的关系。
        relation = self.data.get(analysisStack_top, {}).get(currentStack_top, None)
        format_str=" {:^0} {:^15} {:^10} {:^15} {:^20} "
        if relation == '<':
            print(format_str.format(self.analyzeStep, analysisStack, relation,
                                    self.reverseString(currentStack), '移进'))
            # 将当前输入串栈顶的元素添加到分析栈，并从当前输入串中移除栈顶元素。
            analysisStack += currentStack_top
            currentStack = currentStack[:-1]
            self.toAnalyze(analysisStack, currentStack)
        elif relation == '>':
            print(format_str.format(self.analyzeStep, analysisStack, relation,
                                   self.reverseString(currentStack), '归约'))
            currentChar = analysisStack_top  # 初始化变量currentChar为分析栈顶的元素
            temp_string = ""
            for i in range(len(analysisStack) - 1, -1, -1):  # 从分析栈的最后一个元素开始往前循环（倒序）
                if (analysisStack[i] >= 'A' and analysisStack[i] <= 'Z'):
                    temp_string = analysisStack[i] + temp_string  # 将当前元素加到temp_string的开头
                    continue
                elif (self.data[analysisStack[i]][currentChar] == '<'):
                    break  # 最左素短语，跳出
                temp_string = analysisStack[i] + temp_string
                currentChar = analysisStack[i]
            if (temp_string in self.sentencePattern):
                analysisStack = analysisStack[0:i + 1]  # 截取分析栈，使其只包含归约后的部分
                analysisStack += 'N'
                self.toAnalyze(analysisStack, currentStack)
            else:
                print("归约出错！待归约串为：", temp_string, "--->产生式右部无此句型！")
                self.analyzeResult = False
                return
        elif (relation == '='):
            if (analysisStack_top == '#' and currentStack_top == '#'):
                print(format_str.format(self.analyzeStep, analysisStack, relation,
                                        self.reverseString(currentStack), '完成'))
                self.analyzeResult = True
                return
            else:
                print(format_str.format(self.analyzeStep, analysisStack, relation,
                                        self.reverseString(currentStack), '移进'))
                # 将当前输入串栈顶的元素添加到分析栈，并从当前输入串中移除栈顶元素
                analysisStack += currentStack_top
                currentStack = currentStack[:-1]
                self.toAnalyze(analysisStack, currentStack)
        elif (relation == None):
            print(format_str.format(self.analyzeStep, analysisStack, 'None',
                                    self.reverseString(currentStack), '报错'))
            self.analyzeResult = False
            return

    # 输出firstVT集合、lastVT集合：
    def calculate_firAndlast(self):
        # 计算FIRSTVT和LASTVT集合，直到收敛
        changed = True
        while changed:
            changed = False
            old_firstVT = self.firstVT.copy()
            old_lastVT = self.lastVT.copy()
            for i in self.formules:
                self.get_fistVT(i)
                self.get_lastVT(i)
            if self.firstVT != old_firstVT or self.lastVT != old_lastVT:
                changed = True
    def print_firstVT(self):
        self.calculate_firAndlast()
        print("firstVT集合：")
        for i in self.non_ter:
            print(i + " : " + self.firstVT[i])

    def print_lastVT(self):
        self.calculate_firAndlast()
        print("lastVT集合：")
        for i in self.non_ter:
            print(i + " : " + self.lastVT[i])

    def print_Optable(self):
        self.calculate_firAndlast()
        temp2 = self.Start + " -> #" + self.Start + "#"
        self.formules.append(temp2)  # 在前后加上井号
        for i in self.formules:
            self.analy(i)
        print("算符优先分析表")
        for i in self.terSymblo:
            print("\t" + i.ljust(1), end="")
        print()
        for i in self.terSymblo:
            print(i.ljust(1), end="")  # i.ljust(4)：如果i的长度小于4，那么它将在i的左侧添加空格，使其总宽度为4。
            for j in self.terSymblo:
                if j in self.data[i]:
                    print(self.data[i][j].rjust(18), end="")
                else:
                    print("\t\t", end="")
            print()
    def input(self,message):
        try:
            #print("请输入待分析的字符串：")
            string = message
            string = string.replace(" ", "")
            # 将数字转化成字符i
            string = re.sub(r'\d', 'i', string)

            string += "#"

            print(" {:^2} {:^10} {:^6} {:^12} {:^10} ".format('步骤', '分析栈', '优先关系', '当前输入串', '移进或归约'))
            self.initStack(string)
            if (self.analyzeResult):
                print("该字符串是文法的合法句子。\n")
            else:
                print("该字符串不是文法的合法句子。\n")
        except Exception as e:
            print(f"输入处理出错：{e}")


#实验五 tab5

class SLR:
    def __init__(self, grammar):
        self.grammar = grammar
        self.lr0 = self.lr0_items()
        self.table = self.slr1_table()

    def first(self, symbol):
        if symbol.islower() or symbol in ('(', ')', ','):
            return {symbol}
        first_set = set()
        for prod in self.grammar:
            if prod[0] == symbol:
                right = prod[1]
                if right == 'ε':
                    first_set.add('ε')
                else:
                    for char in right:
                        char_first = self.first(char)
                        first_set.update(char_first - {'ε'})
                        if 'ε' not in char_first:
                            break
                    else:
                        first_set.add('ε')
        return first_set

    def follow(self, symbol):
        follow_set = set()
        if symbol == 'S\'':
            follow_set.add('$')
        for prod in self.grammar:
            left, right = prod
            for i in range(len(right)):
                if right[i] == symbol:
                    if i < len(right) - 1:
                        next_symbol = right[i + 1]
                        next_first = self.first(next_symbol)
                        follow_set.update(next_first - {'ε'})
                        if 'ε' in next_first:
                            if left != symbol:
                                follow_set.update(self.follow(left))
                    else:
                        if left != symbol:
                            follow_set.update(self.follow(left))
        return follow_set

    def closure(self, items):
        new_items = set(items)
        while True:
            old_items = set(new_items)
            for item in old_items:
                dot_pos = item.index('.')
                if dot_pos < len(item) - 1:
                    next_symbol = item[dot_pos + 1]
                    if next_symbol.isupper():
                        for prod in self.grammar:
                            if prod[0] == next_symbol:
                                new_item = f'{prod[0]} -> .{prod[1]}'
                                new_items.add(new_item)
            if new_items == old_items:
                break
        return new_items

    def goto(self, items, symbol):
        new_items = set()
        for item in items:
            dot_pos = item.index('.')
            if dot_pos < len(item) - 1 and item[dot_pos + 1] == symbol:
                new_item = item[:dot_pos] + symbol + '.' + item[dot_pos + 2:]
                new_items.add(new_item)
        return self.closure(new_items)

    def lr0_items(self):
        start_item = f'{self.grammar[0][0]} -> .{self.grammar[0][1]}'
        start_set = self.closure({start_item})
        items = [start_set]
        stack = [start_set]
        while stack:
            current_set = stack.pop()
            symbols = set()
            for item in current_set:
                dot_pos = item.index('.')
                if dot_pos < len(item) - 1:
                    symbols.add(item[dot_pos + 1])
            for symbol in symbols:
                next_set = self.goto(current_set, symbol)
                if next_set not in items:
                    items.append(next_set)
                    stack.append(next_set)
        return items

    def slr1_table(self):
        table = {}
        for i, state in enumerate(self.lr0):
            for item in state:
                dot_pos = item.index('.')
                if dot_pos == len(item) - 1:
                    if item == f'{self.grammar[0][0]} -> {self.grammar[0][1]}.':
                        table[(i, '$')] = 'acc'
                    else:
                        prod_index = self.grammar.index((item.split(' -> ')[0], item.split(' -> ')[1][:-1]))
                        left_symbol = item.split(' -> ')[0]
                        follow_set = self.follow(left_symbol)
                        for symbol in follow_set:
                            table[(i, symbol)] = f'r{prod_index}'
                else:
                    next_symbol = item[dot_pos + 1]
                    next_state = self.lr0.index(self.goto(state, next_symbol))
                    if next_symbol.islower() or next_symbol in ('(', ')', ','):
                        table[(i, next_symbol)] = f's{next_state}'
                    else:
                        table[(i, next_symbol)] = next_state
        return table

    def print_follow_sets(self):
        print("Follow 集合:")
        non_terminals = set(prod[0] for prod in self.grammar)
        for nt in non_terminals:
            print(f"Follow({nt}) = {self.follow(nt)}")

    def print_states(self):
        print("状态集合:")
        for i, state in enumerate(self.lr0):
            print(f"状态 {i}:")
            for item in state:
                print(f"  {item}")

    def print_goto_function(self):
        print("状态转移函数:")
        for i, state in enumerate(self.lr0):
            symbols = set()
            for item in state:
                dot_pos = item.index('.')
                if dot_pos < len(item) - 1:
                    symbols.add(item[dot_pos + 1])
            for symbol in symbols:
                next_state = self.lr0.index(self.goto(state, symbol))
                print(f"状态{i}-->{symbol}-->状态{next_state}")

    def print_action_table(self):
        print("SLR(1) Action 表:")
        terminals = set([symbol for prod in self.grammar for symbol in prod[1] if symbol.islower() or symbol in ('(', ')', ',')])
        terminals.add('$')
        print("State", end="\t")
        for terminal in sorted(terminals):
            print(terminal, end="\t")
        print()
        max_state = max([state for state, _ in self.table.keys()])
        for state in range(max_state + 1):
            print(state, end="\t")
            for terminal in sorted(terminals):
                action = self.table.get((state, terminal), '')
                print(action, end="\t")
            print()

    def print_goto_table(self):
        print("SLR(1) Goto 表:")
        non_terminals = set(prod[0] for prod in self.grammar) - {'S\''}
        print("State", end="\t")
        for non_terminal in sorted(non_terminals):
            print(non_terminal, end="\t")
        print()
        max_state = max([state for state, _ in self.table.keys()])
        for state in range(max_state + 1):
            print(state, end="\t")
            for non_terminal in sorted(non_terminals):
                goto_entry = self.table.get((state, non_terminal), '')
                print(goto_entry, end="\t")
            print()

    def slr1_parser(self, input_string):
        state_stack = [0]
        symbol_stack = ['$']
        input_string += '$'
        index = 0
        print("{:^15} {:^10} {:^15} {:^15}".format('状态栈', '符号栈', '剩余输入符号串', '当前动作'))

        while True:
            state = state_stack[-1]
            symbol = input_string[index]
            action = self.table.get((state, symbol))
            if action is None:
                action_str = "错误：无有效动作"
            elif action.startswith('s'):
                next_state = int(action[1:])
                action_str = f"shift {next_state}"
                state_stack.append(next_state)
                symbol_stack.append(symbol)
                index += 1
            elif action.startswith('r'):
                prod_index = int(action[1:])
                left, right = self.grammar[prod_index]
                action_str = f"reduce {left}->{right}"
                for _ in range(len(right)):
                    state_stack.pop()
                    symbol_stack.pop()
                prev_state = state_stack[-1]
                next_state = self.table[(prev_state, left)]
                state_stack.append(next_state)
                symbol_stack.append(left)
            elif action == 'acc':
                action_str = "接受"

            print("{:^15} {:^15} {:^15} {:^20}".format(str(state_stack), str(symbol_stack), input_string[index:], action_str))
            if action is None:
                print("错误：输入符号串不是正确的句子")
                break
            elif action == 'acc':
                print("输入符号串是正确的句子")
                break


# if __name__ == "__main__":
#     grammar = [
#         ('S\'', 'E'),
#         ('E', '(L)'),
#         ('E', 'a'),
#         ('L', 'L,E'),
#         ('L', 'E')
#     ]
#     slr = SLR(grammar)
#     slr.print_follow_sets()
#     print()
#     slr.print_states()
#     print()
#     slr.print_goto_function()
#     print()
#     slr.print_action_table()
#     print()
#     slr.print_goto_table()
#     print()
#
#     input_string = input("请输入符号串：")
#     slr.slr1_parser(input_string)

# 主函数
# if __name__ == "__main__":
#     # 初始化NFA分析器
#     nfa = NFAAnalyzer(
#         K=["A", "B", "C"],
#         E=["0", "1"],
#         Z=["C"],
#         S=["A"],
#         n=5,
#         F=[
#             ["A", "$", "B"],
#             ["B", "0", "B"],
#             ["B", "1", "B"],
#             ["B", "1", "C"],
#             ["C", "$", "B"]
#         ]
#     )
#
#     # 执行转换并打印结果
#     nfa.NFA2DFA()
#     nfa.print_DFA()
#     lr0 = lr0_items()
#     table = slr1_table()
#
#     print_follow_sets()
#     print()
#     print_states(lr0)
#     print()
#     print_goto_function(lr0)
#     print()
#     print_action_table(table)
#     print()
#     print_goto_table(table)
#     print()
#
#     input_string = input("请输入符号串：")
#     slr1_parser(input_string, table)

# if __name__ == "__main__":
#     m1=Op()
#     m1.data_input()
#     m1.print_firstVT()
#     m1.print_lastVT()
#     m1.print_Optable()
#     # 定义文法
#     grammar = {
#         'E': [['T','A']],
#         'T': [['F', 'B']],
#         'A': [['~'], ['+','T','A']],
#         'B': [['*','F','B'],['~']],
#         'F': [['(','E',')'],['i']]
#     }
#     print(grammar)
#     C = Calculate_First(grammar)
#     C.print_first()

# #
# if __name__ == "__main__":
#     # 定义文法
#     grammar = {
#         'S': [['A', 'B'], ['a']],
#         'A': [['ε'], ['b']],
#         'B': [['c']],
#     }
#
#     C=Calculate_First(grammar)
#     data = "；"
#     data = data.split()
#     myAnalyzer = lexicalAnalyzer(data)
#     myAnalyzer.scan()
#
#     myAnalyzer2=NFAAnalyzer('K', 'E', 'Z', 'S', 'n','F')
#     myAnalyzer2.print_DFA()
#     # print(myAnalyzer.result)
#     # print(myAnalyzer.typeStatistic)
#     #NFAAnalyzer.input_NFA()
#     # NFAAnalyzer.NFA2DFA()
#     # NFAAnalyzer.print_DFA()


