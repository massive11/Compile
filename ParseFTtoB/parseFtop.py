# 类L语言的语法分析————自上而下的语法分析

# 预测分析表，其中A代表E'，B代表T'
forecast = {'E-i': 'TA', 'E-(': 'TA', 'A-+': '+TA', 'A-)': '', 'A-#': '', 'T-i': 'FB', 'T-(': 'FB', 'B-+': '',
            'B-*': '*FB', 'B-)': '', 'B-#': '', 'F-i': 'i', 'F-(': '(E)'}

def analize(str):
    # 初始操作
    fp_write = open('./resultP.txt', 'w')
    print('#E'.ljust(20), "{}#".format(str).rjust(20), file=fp_write)
    anaStack = ['E']  # 开始符号为E
    inputT = []
    for i in str:
        inputT.append(i)
    inputT.reverse()  # 待匹配输入串倒序入串
    # 循环操作
    if len(inputT) == 0:
        print('Fail1!', file=fp_write)
    else:
        while True:
            # 分析栈和输入串都为空，说明成功匹配
            if len(inputT) == 0 and len(anaStack) == 0:
                print('Success!', file=fp_write)
                break
                # 分析栈已经为空，但输入串尚未匹配完，可以认为匹配失败
            elif (len(inputT) != 0 and len(anaStack) == 0):
                print('Fail2!', file=fp_write)
                break
            else:  # 匹配尚未结束
                p1 = ""
                p2 = ""
                left = anaStack.pop()  # 取分析栈的栈顶符号
                if len(inputT) >= 1:  # 当输入串栈不为空时
                    # right取输入串栈的栈顶元素，但暂时先不删除
                    right = inputT[-1]
                    if left == right:  # 若能直接匹配
                        inputT.pop()  # 从输入串栈中删掉该符号
                        continue  # 继续匹配下一个字符
                    else:  # 不能直接匹配
                        key = left + '-' + right
                        # 看预测分析表是否有相应产生式
                        if key in forecast.keys():
                            answer = forecast[key]
                            if len(answer) >= 1:
                                answer = answer[::-1]
                                for i in answer:
                                    anaStack.append(i)
                            #以下为了输出
                            for i in anaStack:
                                if i == 'A':
                                    p1 += 'E\''
                                elif i == 'B':
                                    p1 += 'T\''
                                else:
                                    p1 += i
                            if len(inputT) >= 1:
                                reInputT = inputT[::-1]
                                for i in reInputT:
                                    p2 += i
                            print("#{}".format(p1).ljust(20), "{}#".format(p2).rjust(20), file=fp_write)
                            # 以上为了输出
                        else:
                            print('Fail3!', file=fp_write)
                            break
                else:  # 当输入串栈为空时
                    flag = False
                    while len(anaStack) != 0:  # 当分析栈不为空时循环
                        key = left + '-#'
                        if key in forecast.keys():  # 若当前字符能导出栈底符号
                            answer = forecast[key]
                            if len(answer) >= 1:  # 该产生式不是导出空串
                                answer = answer[::-1]
                                for i in answer:
                                    anaStack.append(i)
                            # 以下为了输出
                            for i in anaStack:
                                if i == 'A':
                                    p1 += 'E\''
                                elif i == 'B':
                                    p1 += 'T\''
                                else:
                                    p1 += i
                            print("#{}".format(p1).ljust(20), "{}#".format(p2).rjust(20), file=fp_write)
                            # 以上为了输出
                            if len(anaStack) >= 1:
                                left = anaStack.pop()
                        else:
                            print('Fail4!', file=fp_write)
                            flag = True
                            break
                    if flag == True:
                        break

def main():
    analize('(i)+i^i')

if __name__ == '__main__':
    main()