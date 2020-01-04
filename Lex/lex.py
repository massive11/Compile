#类L语言的词法分析

#关键字
keyWord = {'begin' : 1, 'end' : 2, 'integer' : 3, 'char' : 4, 'bool' : 5, 'real' : 6, 'input' : 7, 'output' : 8, 'program' : 9,
           'read' : 10, 'write' : 11, 'for' : 12, 'to' : 13, 'while' : 14, 'do' : 15, 'repeat' : 16, 'until' : 17, 'if' : 18, 'then' : 19,
           'else' : 20, 'true' : 21, 'false' : 22, 'var' : 23, 'const' : 24, 'and' : 32, 'or' : 33, 'not' : 34}
#算符
operator  = {'+' : 25, '-' : 26, '*' : 27, '/' : 28, '=' : 29, '<' : 30, '>' : 31, '<=' : 35, '>=' : 36, '<>' : 37, ':=' : 38}
#界符
delimiters = {'(' : 44, ')': 45, ':' : 46, '.' : 47, ';' : 48, ',' : 49, '_' : 50, '\'' : 51, '\"' : 52}

#预处理函数，去掉多余的空格、注释
def preProcess(fileName):
    try:  # 避免程序因异常而中断
        fp_read = open(fileName, 'r')
        # 写入新文件中，preProcess为预处理后的文本
        fp_write = open('./Lex/preProcess.txt', 'w')
        sign = 0
        while True:
            read = fp_read.readline()
            if not read:
                break
            length = len(read)
            i = -1
            while i < length - 1:
                i += 1
                if read[i] == ' ':
                    if sign == 1:
                        continue
                    # sign不为1说明上一个字符不是空格，输出当前空格
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '\t':
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write('')
                elif read[i] == '\n':
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '/' and read[i + 1] == '*':
                    i = i + 2
                    # 从注释后的第一个字符开始遍历直到读取到注释结束
                    while True:
                        if read[i] == '*' and read[i + 1] == '/':
                            break
                        i = i + 1
                    i = i + 1
                else:
                    fp_write.write(read[i])
                    sign = 0
        fp_write.write('#')
    except Exception:
        print('Errors')

#标识符为39
def process(fileName):
    try:
        fp_read=open(fileName,'r')
        fp_write=open('./Lex/result.txt','w')
        lines = fp_read.readlines()
        i = -1
        for line in lines:
            length = len(line)
            while  i < length - 1:
                i+=1
                # 当前字符为空格则跳过
                if line[i] == ' ':
                    continue
                # 当前字符为界符
                if line[i] in delimiters.keys():
                    print('(', delimiters[line[i]], ', "', line[i], '" )', file = fp_write)
                    continue
                    # 当前字符为算符
                if line[i] in operator.keys():
                    # 判断是否为两位的算符的第二位，若是第二位则直接跳过，因为二位算符在第一位运算符的时候已经输出过
                    if line[i-1] in operator:
                        continue
                    if line[i+1] in operator:
                        cal = line[i] + line[i+1]
                        print('(', operator[cal], ', "', cal, '" )', file = fp_write)
                    else:
                        print('(', operator[line[i]], ', "', line[i], '" )', file = fp_write)
                        continue
                        # 判断常数，在数字第一位对其进行了处理，后续直接跳过
                if line[i-1].isdigit():
                    continue
                # 判断常数
                if line[i].isdigit():
                    t = i
                    while line[i].isdigit():
                        i+=1
                    # 小数
                    if line[i] == '.':
                        print('( 41 , " ', end='', file = fp_write)
                    else:
                        print('( 40 , " ', end='', file = fp_write)
                    i = t
                    while line[i].isdigit() or line[i] == '.':
                        print(line[i], end='', file=fp_write)
                        i+=1
                    print(' " )', file=fp_write)
                    i -= 1
                    continue
                # 判断关键字和标识符
                j = 0
                temp = ''
                while True:
                    if  line[i] == ' ' or line[i] in operator.keys() or line[i] in delimiters.keys():
                        break
                    else:
                        j+=1
                    i+=1
                    if i > length-1:
                        break
                temp = line[i-j:i]
                if temp in keyWord.keys():
                    print('(', keyWord[temp], ', "', temp, '" )', file=fp_write)
                else:
                    # 程序结束
                    if temp == '#':
                       break
                    print('( 39 , "', temp, '" )', file=fp_write)
                i -= 1
    except Exception:
        print('Error')

def main():
    preProcess('./Lex/importT.txt')
    process('./Lex/preProcess.txt')

if __name__ == '__main__':
    main()