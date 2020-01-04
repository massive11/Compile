#类L语言的语义分析

#算符优先关系表
priority = {'++': '>', '+*': '<', '+^': '<', '+i': '<', '+(': '<', '+)': '>', '+#': '>',
            '*+': '>', '**': '>', '*^': '<', '*i': '<', '*(': '<', '*)': '>', '*#': '>',
            '^+': '>', '^*': '>', '^^': '<', '^i': '<', '^(': '<', '^)': '>', '^#': '>',
            'i+': '>', 'i*': '>', 'i^': '>', 'i)': '>', 'i#': '>',
            '(+': '<', '(*': '<', '(^': '<', '(i': '<', '((': '<', '()': '=',
            ')+': '>', ')*': '>', ')^': '>', '))': '>', ')#': '>',
            '#+': '<', '#*': '<', '#^': '<', '#i': '<', '#(': '<', '##': '=',}

def analize(str):
    #初始操作
    stack = ['#']
    inputT = ['#']
    for i in str:
        inputT.append(i)    #输入字符串进栈
    inputT.reverse()        #由于从输入串头部开始匹配，因此将输入串栈倒序
    fp_write = open('./resultS.txt', 'w')     #打开结果文件
    print('#'.ljust(20), "{}#".format(str).rjust(20), file=fp_write)     #把初始状态打印出来
    if len(inputT) == 1:    #对输入串进行判断，若输入串栈长度为1，表示输入串为空，对该文法而言无法匹配，直接失败，错误代码为Fail3
        print('Fail3!', file = fp_write)
    elif inputT[-2] == ')': #若输入串以右括号为第一个符号，则直接匹配失败，错误代码为Fail4
        print('Fail4!', file=fp_write)
    else:                   #排除两种显而易见的不匹配串之后，开始进行进一步的判断
        count = 100   #newtemp
        seman = {}    #用于存储place
        while True:
            p1 = ''     #p1，p2用于打印输出
            p2 = ''
            right = inputT[-2]       #right取输入串栈的第一个字符
            if stack[-1] != 'N':     #若stack的最后一个字符为终结符
                key = stack[-1] + right     #判断stack的栈顶符号和输入串第一个符号的优先级
            else:
                key = stack[-2] + right     #此文法不会出现两个连续的非终结符
            if key in priority.keys():
                if priority[key] == '<':   #无法规约，直接入栈
                    inputT.pop(-2)        #从输入串栈出来进入stack
                    stack.append(right)
                else:                      #能进行规约，先入栈再进行规约
                    inputT.pop(-2)
                    stack.append(right)
                    #对i进行规约
                    if stack[-2] == 'i':
                        stack[-2] = 'N'
                # 以下部分为了打印输出
                for i in stack:
                    p1 += i
                inputT.pop()
                out = inputT[::-1]
                out += '#'
                for i in out:
                    p2 += i
                inputT += '#'
                print("{}".format(p1).ljust(20), "{}".format(p2).rjust(20), file=fp_write)
                # 以上部分为了打印输出
            else:
                print('Fail1!', file=fp_write)    #此时输入串栈无法全部进入stack，直接失败，错误代码为fail1
                break
####################################################################################################
            # 输入缓冲区为空，可进行stack内部的规约，此为第二阶段
            if len(inputT) == 1:
                #以下为了打印输出第二阶段的初始状态
                p1 = ''
                if stack[-1] == 'i':   #对i进行规约
                    stack[-1] = 'N'
                    for i in stack:
                        p1 += i
                    inputT.pop()
                    p2 = '#'
                    print("{}".format(p1).ljust(20), "{}".format(p2).rjust(20), file=fp_write)
                # 以上为了打印输出第二阶段的初始状态
                #为N编号
                c = 0
                no = 97     #a的ASCII
                for n in stack:
                    if n == 'N':
                        stack[c] = chr(no)
                        seman[stack[c]] = 'i'
                        no += 1
                    c += 1
                #以下为打印输出给N编号后的形式
                # p1 = ''
                # for i in stack:
                #     p1 += i
                # p2 = '#'
                # print("{}".format(p1).ljust(20), "{}".format(p2).rjust(20), file=fp_write)
                # 以上为打印输出给N编号后的形式
                stack += '#'   #将输入串栈变为 '#i+i*i#'的形式 ，方便进行后续的处理
                i = 1
                flag = False
                while True:
                    if i == len(stack):     #此时已从左至右遍历结束，判断此次是否有规约项
                        if flag == False:   #flag为False表示此次没有进行规约，即没有规约完，匹配失败，错误代码为fail2
                            print('Fail2!', file=fp_write)
                            break
                        else:               #否则表示此次遍历有规约项，重新进行新一轮的遍历，并将flag重置为false
                            i = 1
                            flag = False
                    if stack[i-1] == '(' and stack[i] >= 'a' and stack[i] <= 'z' and stack[i+1] == ')':       #若存在(N)， 对(N)进行规约
                        if stack[i] in seman.keys():
                            old = stack[i]
                            stack[i - 1:i + 2] = chr(no)
                            seman[stack[i-1]] = seman[old]
                        else:
                            stack[i - 1:i + 2] = chr(no)
                            seman[stack[i - 1]] = 'i'
                        no += 1
                        i = i - 1
                        # 以下为打印输出给N编号后的形式
                        # p1 = ''
                        # for s in stack:
                        #     p1 += s
                        # p2 = '#'
                        # print("{}".format(p1).ljust(20), "{}".format(p2).rjust(20), file=fp_write)
                        # 以上为打印输出给N编号后的形式
                        # 以下为了打印输出
                        # p1 = ''
                        # stack.pop()
                        # for p in stack:
                        #     p1 += p
                        # stack.append('#')
                        # print("{}".format(p1).ljust(20), "{}".format('#').rjust(20), file=fp_write)
                        # 以上为了打印输出
                        flag = True
                    if len(stack) == 3 and stack[1] >= 'a' and stack[1] <= 'z':   #判断成功的条件：stack中规约至 '#N#' 的形式
                        print('Success!', file=fp_write)
                        break
                    while stack[i] >= 'a' and stack[i] <= 'z':   #从左至右对stack中的内容进行规约，规约条件为相邻的三个终结符，其关系为 ileft<i>iright
                        i += 1
                    ileft = i-1
                    while stack[ileft] >= 'a' and stack[ileft] <= 'z':
                        ileft -= 1
                    key = stack[ileft] + stack[i]
                    if key in priority.keys():
                        if priority[key] == '<':    #在ileft<i的情况下继续向下做判断
                            iright = i+1
                            while stack[iright] >= 'a' and stack[iright] <= 'z':
                                iright += 1
                            key = stack[i] + stack[iright]
                            if key in priority.keys():
                                if priority[key] == '>':    #只有此时满足规约条件
                                    flag = True
                                    if stack[i] != 'i' and (stack[i] < 'a' or stack[i] > 'z'):
                                        print('(', stack[i], ', ', seman[stack[i-1]], ', ', seman[stack[i+1]], ',', count, ')', file=fp_write)
                                        count += 1
                                    stack[ileft+1:iright] = chr(no)   #对满足条件的部分进行规约
                                    seman[stack[ileft + 1]] = count-1
                                    no += 1
                                    i = ileft
                                    # 以下为打印输出给N编号后的形式
                                    # p1 = ''
                                    # for s in stack:
                                    #     p1 += s
                                    # p2 = '#'
                                    # print("{}".format(p1).ljust(20), "{}".format(p2).rjust(20), file=fp_write)
                                    # 以上为打印输出给N编号后的形式
                                    # 以下为了打印输出
                                    # p1 = ''
                                    # stack.pop()
                                    # for p in stack:
                                    #     p1 += p
                                    # stack.append('#')
                                    # print("{}".format(p1).ljust(20), "{}".format('#').rjust(20), file=fp_write)
                                    # 以上为了打印输出
                                else:    #不满足要求则持续向后推进
                                    i += 1
                                    continue
                            else:
                                i += 1
                                continue
                        else:
                            i += 1
                            continue
                    else:
                        i += 1
                        continue
                break

def main():
    analize('i*i+i^i+i')

if __name__ == '__main__':
    main()