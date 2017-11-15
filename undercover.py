#!/usr/bin/python
# -*- coding: UTF-8 -*-
#运行环境 python2.7
#author：hx

from Tkinter import *
from PIL import ImageTk, Image
from random import *
from time import *
import tkMessageBox


root = Tk()
root.title('who is undercover')
# root.geometry('300x300')
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

# messagevar=StringVar()
# message = Message(frame, textvariable=messagevar, width=300)
# message.pack()
# messagevar.set('hellodddddd')


# 文本，显示信息
textvar = StringVar
text = Text(frame, height=10)
text.pack()

# 投票框
entryvar = StringVar
entry = Entry(frame, width=35, textvariable=entryvar)




words_list = [['钢笔', '铅笔'], ['月亮', '太阳'], ['鸭脖', '鸡爪'], ['苹果', '安卓'], ['风衣','毛衣'],['唇膏','口红'],['最炫民族风','江南style']]
players_code = ['1号', '2号', '3号', '4号', '5号']

#check-word变量
word_num = 1
flag = 0

#vote投票变量
vote_num = 1
num1 = num2 = num3 = num4 = num5 = 0
players_ticket = dict()

def get_word():
    global undercover, players,words_list
    words = choice(words_list)
    words_list.remove(words)
    u_word = choice(words)
    words.remove(u_word)
    c_word = choice(words)

    player_code = choice(players_code)
    undercover = player_code
    print('卧底是%s' % undercover)

    players = dict()
    for player_code in players_code:
        if player_code == undercover:
            players[player_code] = u_word
        else:
            players[player_code] = c_word
    print(players)
    return players


def start_game():
    global game_num, word_num, vote_num, flag, num1, num2, num3, num4, num5, players_ticket

    text.delete(1.0, END)
    if len(words_list) != 0:
        text.insert(END, '当前玩家：')
        for player_code in players_code:
            text.insert(END, player_code+' ')

        tkMessageBox.showinfo(title='谁是卧底', message='惊心动魄的游戏即将开始，你们准备好了吗！')
        get_word()
        labelvar.set('请1号查看词语')

        # 初始化变量
        word_num = 1
        vote_num = 1
        flag = 0
        num1 = num2 = num3 = num4 = num5 = 0
        players_ticket = dict()

    else:
        tkMessageBox.showinfo(title='谁是卧底', message='很抱歉啦，我用尽了毕生所有的词了')



def check_word():
    global word_num, flag
    if flag == 0:
        if word_num < 6:
            text.delete(1.0, END)
            text.insert(1.0, players[str(word_num)+'号'])
            word_num += 1
            flag = 1
        else:
            text.delete(1.0, END)
            text.insert(1.0, '所有玩家已查看完词语')
            labelvar.set('接下啦，请所有玩家投票，选取出你认为最有可能是卧底的人')
            flag = 0
    else:
        if word_num < 6:
            text.delete(1.0, END)
            labelvar.set('请' + str(word_num) + '号查看词语')
            flag = 0
        else:
            text.delete(1.0, END)
            tkMessageBox.showinfo(title='谁是卧底', message='所有玩家单词查看完毕，接下啦所有玩家进行依次描述')
            labelvar.set('请%s进行投票' % players_code[0])

            text.insert(END, '当前玩家：')
            for player_code in players_code:
                text.insert(END, player_code + ' ')





def vote():
    global players_ticket, vote_num, players_code, num1, num2, num3, num4, num5, max_ticket
    selected = entry.get()
    selected = selected.encode('utf-8')

    if vote_num < len(players_code)+1:
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
            else:
                num5 += 1
                players_ticket['5号'] = num5

            vote_num += 1
            entry.delete(0, END)
            if vote_num < len(players_code)+1:
                labelvar.set('请%s投票' % players_code[vote_num-1])
            else:

                entry.delete(0, END)
                a = [num1, num2, num3, num4, num5]
                max_ticket = max(num1, num2, num3, num4, num5)

                num = 0
                for i in a:
                    if i == max_ticket:
                        num += 1
                if num == 1:
                    print(players_ticket)
                    for player in players_ticket:
                        if (max_ticket == players_ticket[player]) and (undercover == player):
                            tkMessageBox.showinfo(title='谁是卧底', message='游戏结束，平民胜利，大家都有一双火眼睛睛')
                            labelvar.set('卧底是%s' % player)
                            text.delete(1.0, END)

                            return '跳出循环'
                        elif max_ticket == players_ticket[player]:
                            tkMessageBox.showinfo(title='谁是卧底', message='卧底太狡猾了，%s平民被冤死。' % player)
                            labelvar.set('%s是平民' % player)
                            players_code.remove(player)

                            text.delete(1.0, END)
                            text.insert(END, '当前玩家：')
                            for player_code in players_code:
                                text.insert(END, player_code + ' ')

                            if len(players_code) == 2:
                                tkMessageBox.showinfo(title='谁是卧底', message='没想到吧，%s才是卧底，哥们你隐藏得太深了' % undercover)
                            else:
                                tkMessageBox.showinfo(title='谁是卧底', message='接下啦，大家进行描述')
                                labelvar.set('请%s进行投票' % players_code[0])

                                vote_num = 1
                                players_ticket = {}
                                num1 = num2 = num3 = num4 = num5 = 0
                                return '跳出循环'
                        else:
                            pass
                else:
                    tkMessageBox.showinfo(title='谁是卧底', message='人数出现了相同，请大家重新描述，并进行投票')
                    labelvar.set('请%s进行投票' % players_code[0])
                    vote_num = 1
                    players_ticket = {}
                    num1 = num2 = num3 = num4 = num5 = 0
                    return '跳出循环'

        else:
            tkMessageBox.showinfo(title='谁是卧底', message='请输入正确的投票号码')
            labelvar.set('请%s投票' % players_code[vote_num-1])

    else:
        pass

def end_game():
    print('游戏结束')

# 按钮
but1 = Button(frame, text="开始游戏", width=10, command=start_game)
but1.pack(side=LEFT)

but2 = Button(frame, text="查看单词", width=10, command=check_word)
but2.pack(side=LEFT)


entry.pack(side=LEFT)

but3 = Button(frame, text="结束游戏", width=10, command=root.quit)
but3.pack(side=RIGHT)

but4 = Button(frame, text="投票", width=10, command=vote)
but4.pack(side=RIGHT)

frame.pack()
root.mainloop()




