#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author：hx
#运行环境 python2.7

__authors__ = "he xi"


from Tkinter import *
import tkMessageBox
import ttk
from PIL import ImageTk, Image
import random


root = Tk()
root.title('谁是卧底')
root.resizable(width=False, height=False)

# 容器
frame = Frame(root, bg='#08a62b', width=400, height=200)

#设置背景图片
image = Image.open('img/img5.gif')
background_image = ImageTk.PhotoImage(image)
label_img = Label(frame, image=background_image, heigh=300, width=300, bg='#08a62b')
label_img.pack(anchor=CENTER)

# 标签，显示信息。
labelvar = StringVar()
label = Label(frame, text='谁是卧底', textvariable=labelvar, width=80, height=2, fg='white', bg='#08a62b')
label.pack()
labelvar.set('谁是卧底')


# 文本，显示信息
textvar = StringVar
text = Text(frame, height=10,  bg='#dfdada')
text.pack()


#人数选定
players_num = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
num_list = StringVar()
choice_player = ttk.Combobox(frame, width=15, textvariable=num_list)
choice_player['values'] = players_num   # 设置下拉列表的值
choice_player.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


#投票选择框
all_players = ['1号', '2号', '3号', '4号', '5号', '6号', '7号', '8号',
               '9号', '10号', '11号', '12号', '13号', '14号', '15号']
code_list = StringVar()
choice_code = ttk.Combobox(frame, width=15, textvariable=code_list)
choice_code['values'] = all_players    # 设置下拉列表的值
# choice_code.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
choice_code.insert(END, '选择玩家号码')




# 读取文本中的单词信息
def get_words_lsit():
    words_list = []
    with open('doc/words.txt', 'r+')as f:
       content = f.read().split('\n')
       for j in content:
          word_list = []
          for i in j.split('--'):
             word_list.append(i)
          words_list.append(word_list)
    return words_list
words_list = get_words_lsit()

#读取游戏规则和软件介绍
def get_game_rule():
    with open('README.md', 'r+')as f:
        content = f.read()
        text.insert(END, content)
get_game_rule()




#分配卧底人数函数
def allot_undercover():
    global undercover_num, players_code, undercover_code, all_players, players_num, choice_num

    choice_num = choice_player.get()
    choice_num = int(choice_num)

    if choice_num <= 5:
        undercover_num = 1
        players_code = all_players[0:choice_num]
        undercover_code = random.sample(players_code, undercover_num)

    elif choice_num <= 10:
        undercover_num = 2
        players_code = all_players[0:choice_num]
        undercover_code = random.sample(players_code, undercover_num)

    elif choice_num <= 15:
        undercover_num = 3
        players_code = all_players[0:choice_num]
        undercover_code = random.sample(players_code, undercover_num)

    # 测试
    for i in undercover_code:
        print '卧底：' +i

#分配词语函数
def allot_words():
    global choice_num, undercover_num, players_code, undercover_code, u_word, c_word, players

    #卧底单词
    words = random.choice(words_list)
    words_list.remove(words)
    u_word = random.choice(words)
    #平民单词
    words.remove(u_word)
    c_word = random.choice(words)

    #分配单词
    for j in players_code:
        if j in undercover_code:
            #卧底
            players[j] = u_word
        else:
            #平民
            players[j] = c_word


    #测试
    # print players_code
    for i, j in players.items():
        print i, j

#获得票数函数
def get_votes():
    global players_ticket, players_code, vote_num
    global num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15

    selected = choice_code.get()
    selected = selected.encode('utf-8')

    # 测试
    print selected

    if selected in players_code:
        if selected == '1号':
            num1 += 1
            players_ticket['1号'] = num1
        elif selected == '2号':
            num2 += 1
            players_ticket['2号'] = num2
        elif selected == '3号':
            num3 += 1
            players_ticket['3号'] = num3
        elif selected == '4号':
            num4 += 1
            players_ticket['4号'] = num4
        elif selected == '5号':
            num5 += 1
            players_ticket['5号'] = num5
        elif selected == '6号':
            num6 += 1
            players_ticket['6号'] = num6
        elif selected == '7号':
            num7 += 1
            players_ticket['7号'] = num7
        elif selected == '8号':
            num8 += 1
            players_ticket['8号'] = num8
        elif selected == '9号':
            num9 += 1
            players_ticket['9号'] = num9
        elif selected == '10号':
            num10 += 1
            players_ticket['10号'] = num10
        elif selected == '11号':
            num11 += 1
            players_ticket['11号'] = num11
        elif selected == '12号':
            num12 += 1
            players_ticket['12号'] = num12
        elif selected == '13号':
            num13 += 1
            players_ticket['13号'] = num13
        elif selected == '14号':
            num14 += 1
            players_ticket['14号'] = num14
        else:
            num15 += 1
            players_ticket['15号'] = num15
        vote_num += 1
    else:
        tkMessageBox.showinfo(title='谁是卧底', message='请输入正确的投票号码')
        labelvar.set('请%s投票' % players_code[vote_num - 1])
        # 测试
        # print '被投玩家：' + selected
        # print players_code
        # print players_ticket

#分析票的结果函数
def analysis_votes():
    global result_status, vote_num, players_code, players_ticket, max_ticket, undercover_code, undercover, max_ticket_codes, other_ticket_codes
    global undercover_died, exception_code
    print players_ticket

    max_ticket = players_ticket[players_code[0]]
    for code, num in players_ticket.items():
        if num > max_ticket:
            max_ticket = num

    # 求最大票数有多少个
    max_ticket_codes = []
    other_ticket_codes = []
    for code, num in players_ticket.items():
        if num == max_ticket:
            max_ticket_codes.append(code)
        else:
            other_ticket_codes.append(code)
    max_ticket_codes.sort()
    other_ticket_codes.sort()

    # 测试
    print '票数最多玩家:',
    for i in max_ticket_codes:
        print i,
    print '票数：' + str(max_ticket)
    print '\n'

    # 平局和非平局状态
    if len(max_ticket_codes) == 1:
        # 非平局
        for player in players_ticket:
            if max_ticket == players_ticket[player] and (player in undercover_code):
                tkMessageBox.showinfo(title='谁是卧底', message='%s果然是卧底，大家都有一双火眼睛睛' % player)
                labelvar.set('卧底是%s' % player)
                undercover_died += 1

                if len(undercover_code) == undercover_died:
                    tkMessageBox.showinfo(title='谁是卧底', message='平民胜利')
                    text.delete(1.0, END)

                    # 显示卧底
                    a = ''
                    for i in undercover_code:
                        a += i + ''
                    text.insert(END, '卧底:%s' % a)

                    exception_code = 1

                    return '跳出循环'
                else:
                    players_code.remove(player)

                    if len(players_code) == 2:
                        tkMessageBox.showinfo(title='谁是卧底', message='卧底胜利了')
                        # 显示卧底
                        text.delete(1.0, END)
                        a = ''
                        for i in undercover_code:
                            a += i + ''
                        text.insert(END, '卧底:%s' % a)

                        exception_code = 1

                        return '跳出循环'
                    else:

                        # 初始化变量
                        init()
                        # 更新玩家数据
                        display_player()
                        choice_code.set('')

                        tkMessageBox.showinfo(title='谁是卧底', message='剩余玩家，继续描述,然后投票')
                        labelvar.set('请%s进行投票' % players_code[0])
                        return '跳出循环'

            elif max_ticket == players_ticket[player]:
                tkMessageBox.showinfo(title='谁是卧底', message='卧底太狡猾了，%s平民被冤死。' % player)
                # text.insert(END, '\n%s是平民'% player)
                labelvar.set('%s是平民' % player)
                players_code.remove(player)

                if len(players_code) == 2:

                    tkMessageBox.showinfo(title='谁是卧底', message='卧底胜利了')
                    # 显示卧底
                    text.delete(1.0, END)
                    a = ''
                    for i in undercover_code:
                        a += i + ''
                    text.insert(END, '卧底:%s' % a)


                    exception_code = 1
                    return '跳出循环'

                else:

                    # 初始化变量
                    init()
                    # 更新玩家数据
                    display_player()
                    choice_code.set('')

                    tkMessageBox.showinfo(title='谁是卧底', message='剩余玩家，继续描述,然后投票')
                    labelvar.set('请%s进行投票' % players_code[0])
                    return '跳出循环'

    else:
        # 平局
        a = ''
        for i in max_ticket_codes:
            a += i + ' '
        tkMessageBox.showinfo(title='谁是卧底', message='人数出现了相同，请%s描述，所有玩家重新进行投票' % a)
        labelvar.set('请%s进行投票' % players_code[0])
        init()
        display_player()
        text.insert(END, '\n相同票数玩家：' + a)
        return '跳出循环'


#初始化函数
def init():
    global word_num, vote_num, players_ticket, players, player_code, display_status, result_status, exception_code
    global num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15

    # 初始化
    players = {}
    word_num = 1
    vote_num = 1
    exception_code = 0
    display_status = 0
    result_status = 0
    players_ticket = {'1号': 0, '2号': 0, '3号': 0, '4号': 0, '5号': 0, '6号': 0, '7号': 0, '8号': 0, '9号': 0, '10号': 0,
                      '11号': 0, '12号': 0, '13号': 0, '14号': 0, '15号': 0}
    num1 = num2 = num3 = num4 = num5 = num6 = num7 = num8 = num9 = num10 = num11 = num12 = num13 = num14 = num15 = 0
    text.delete(1.0, END)


#显示当前玩家函数
def display_player():
    global players_code, undercover_code
    #显示当前玩家
    text.delete(1.0, END)
    text.insert(END, '玩家：')
    for player_code in players_code:
        text.insert(END, player_code + ' ')

    #显示卧底数
    text.insert(END, '\n'+'卧底：'+str(len(undercover_code))+'人')

    #更新下拉框
    choice_code['values'] = players_code


    #测试
    # print players_code


#异常处理
exception_code = 1
def exception_process():
    global exception_code



def start_game():
    global word_num, vote_num,  players_ticket, players, player_code, display_status, result_status, undercover_code
    global num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15,undercover_died, exception_code


    #初始化
    init()
    undercover_died = 0
    #判定是否用完了单词
    if len(words_list) != 0:
        #分配卧底和词语
        allot_undercover()
        allot_words()

        #更新玩家情况
        display_player()

        tkMessageBox.showinfo(title='谁是卧底', message='惊心动魄的游戏即将开始，你们准备好了吗！')
        labelvar.set('请1号查看词语')

    else:
        tkMessageBox.showinfo(title='谁是卧底', message='天啊，我用尽了毕生所学到的词了')



def check_word():
    global word_num, display_status


    #异常处理 防止未按开始按钮就点击查看单词
    if exception_code == 1:
        tkMessageBox.showwarning(title='谁是卧底', message='亲，你是不是忘记了啥啦。请开始游戏')
        return '异常处理'


    # 方案一

    # word_num = 1
    # for player_code in players_code:
    #     messagebox.showinfo(title='谁是卧底', message='请%s查看单词' % player_code)
    #     messagebox.showinfo(title='谁是卧底', message=players[str(word_num) + '号'])
    #     word_num += 1

    # 方案二
    #display_status 控制状态 0为查看单词，1为隐藏单词
    if word_num <= len(players):
        if display_status == 0:
            text.delete(1.0, END)
            text.insert(1.0, players[str(word_num) + '号'])
            word_num += 1
            display_status = 1
        else:
            text.delete(1.0, END)
            labelvar.set('请' + str(word_num) + '号查看词语')
            display_status = 0

    else:
        text.delete(1.0, END)
        tkMessageBox.showinfo(title='谁是卧底', message='单词查看完毕，请所有玩家进行描述')
        labelvar.set('请%s进行投票' % players_code[0])

        # 显示当前玩家
        display_player()




def vote():
    global result_status, vote_num, players_code, players_ticket, max_ticket, undercover_code, undercover, max_ticket_codes, other_ticket_codes
    global num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15,exception_code

    if exception_code == 1:
        tkMessageBox.showwarning(title='谁是卧底', message='亲，你是不是忘记了啥啦。请开始游戏')
        return '异常处理'

    #异常处理，防止未点击开始就点投票
    try:
        display_player()
        if vote_num < len(players_code):
            #获取票数
            get_votes()
            labelvar.set('请%s投票' % players_code[vote_num - 1])
        else:
            #分析票
            get_votes()
            analysis_votes()

    except Exception:
        pass


def end_game():
    print('游戏结束')

# 按钮
choice_player.pack(side=LEFT)

but1 = Button(frame, text="开始游戏", width=10, command=start_game)
but1.pack(side=LEFT)

but2 = Button(frame, text="查看单词", width=10, command=check_word)
but2.pack(side=LEFT)

choice_code.pack(side=LEFT)

but3 = Button(frame, text="结束游戏", width=10, command=root.quit)
but3.pack(side=RIGHT)

but4 = Button(frame, text="投票", width=10, command=vote)
but4.pack(side=RIGHT)


frame.pack()
root.mainloop()




