#!/usr/bin/python
# -*- coding: UTF-8 -*-
#运行环境 python2.7

__authors__ = 'hexi'


from Tkinter import *
import tkMessageBox
import ttk
from PIL import ImageTk, Image
import random
from collections import Counter


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


#下拉框，玩家人数选定
players_num = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
num_list = StringVar()
choice_player = ttk.Combobox(frame, width=15, textvariable=num_list)
choice_player['values'] = players_num   # 设置下拉列表的值
choice_player.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


#下拉框，投票框
all_players = ['1号', '2号', '3号', '4号', '5号', '6号', '7号', '8号',
               '9号', '10号', '11号', '12号', '13号', '14号', '15号']
code_list = StringVar()
choice_code = ttk.Combobox(frame, width=15, textvariable=code_list)
choice_code['values'] = all_players    # 设置下拉列表的值
choice_code.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
# choice_code.insert(END, '选择玩家号码')




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

# 读取游戏规则和软件介绍
def get_game_rule():
    with open('README.md', 'r+')as f:
        content = f.read()
        text.insert(END, content)
get_game_rule()

# 分配卧底人数函数
def allot_undercover():
    global undercover_num, players_code, undercover_code, all_players, choice_num,all_undercover

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

# 分配词语函数
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

# 获得票数函数
def get_votes(voted_players,vote_players):
    global players_ticket, players_code, vote_num, voted_code_list

    selected = choice_code.get()
    selected = selected.encode('utf-8')

    if selected in voted_players:
        voted_code_list.append(selected)
        vote_num += 1
    else:
        tkMessageBox.showinfo(title='谁是卧底', message='请输入正确的投票号码')
        labelvar.set('请%s投票' % vote_players[vote_num - 1])

    # 测试
    print '被投玩家：' + selected
    # print players_code
    # print players_ticket

# 判定人数是否小于2人
def is_not_twoPlayer():
    global players_code, undercover_code, exception_code, result_status

    if len(players_code) == 2:
        tkMessageBox.showinfo(title='谁是卧底', message='卧底胜利了')

        #显示卧底
        display_undercover()
        # 更新label
        labelvar.set('谁是卧底')

    else:
        # 初始化变量
        init()
        # 更新玩家数据
        update(vote_players=players_code, voted_players=players_code)
        #投票状态
        result_status = 'normal'

        tkMessageBox.showinfo(title='谁是卧底', message='剩余玩家，继续描述,然后投票')
        labelvar.set('请%s进行投票' % players_code[0])

#显示卧底
def display_undercover():
    global exception_code

    text.delete(1.0, END)
    # 显示卧底
    a = ''
    for i in undercover_code:
        a += i + ''
    text.insert(END, '卧底:%s' % a)
    exception_code = 1

# 分析票的结果函数
def analysis_votes():
    global players_code, players_ticket, max_ticket, max_ticket_codes, undercover_code
    global undercover_died, exception_code, vote_num, result_status, other_ticket_codes

    #生成玩家票数字典
    players_ticket = Counter(voted_code_list)

    #获取最大票数
    max_ticket = max(players_ticket.values())

    # 最大票数玩家列表
    max_ticket_codes = []
    for code, num in players_ticket.items():
        if num == max_ticket:
            max_ticket_codes.append(code)
    max_ticket_codes.sort()

    #其他票数玩家列表
    other_ticket_codes = []
    for i in players_code:
        if i not in max_ticket_codes:
            other_ticket_codes.append(i)

    #处理所有玩家票数都相等的情况
    if len(other_ticket_codes) == 0:
        tkMessageBox.showinfo(title='谁是卧底', message='这么奇葩的情况都出现了，所有人的票数居然都相等，大家重新开始描述')
        # 初始化变量
        init()
        # 更新玩家数据
        update(vote_players=players_code, voted_players=players_code)
        return '跳出'


    # 测试
    print '投票情况',players_ticket

    print '票数最多玩家:',
    for i in max_ticket_codes:
        print i,
    print '票数：' + str(max_ticket)


    # 平局和非平局状态
    if len(max_ticket_codes) == 1:
        # 非平局
        player = max_ticket_codes[0]
        if player in undercover_code:
            undercover_died += 1
            #判断卧底是否已经全部找出
            if len(undercover_code) == undercover_died:
                tkMessageBox.showinfo(title='谁是卧底', message='平民胜利')
                #显示卧底
                display_undercover()
                #更新label
                labelvar.set('谁是卧底')
            else:
                print player, '是卧底'
                tkMessageBox.showinfo(title='谁是卧底', message='%s果然是卧底，大家都有一双火眼睛睛' % player)
                labelvar.set('卧底是%s' % player)
                players_code.remove(player)
                # 判定是否只剩两个玩家
                is_not_twoPlayer()

        else:
            print player, '是平民'
            tkMessageBox.showinfo(title='谁是卧底', message='卧底太狡猾了，%s平民被冤死。' % player)
            labelvar.set('%s是平民' % player)
            players_code.remove(player)
            # 判定是否只剩两个玩家
            is_not_twoPlayer()

    else:
        # 平局
        a = ''
        for i in max_ticket_codes:
            a += i + ' '
        tkMessageBox.showinfo(title='谁是卧底', message='人数出现了相同，请%s描述，投票玩家进行投票' % a)
        labelvar.set('请%s进行投票' % other_ticket_codes[0])
        init()
        update(voted_players=max_ticket_codes, vote_players=other_ticket_codes)
        result_status = 'unnormal'
        text.insert(END, '\n\n相同票数玩家：' + a)

# 初始化函数
def init():
    global word_num,voted_code_list, vote_num, players_ticket, players
    global player_code, display_status, exception_code

    # 初始化
    players = {} #存放每个玩家对应的单词
    word_num = 1 #用于查看单词按键计数
    vote_num = 0 #用于投票按键计数
    exception_code = 0 #防未开始时，按键操作。
    display_status = 0 #设置查看单词和隐藏单词判断，0查看单词，1隐藏单词
    players_ticket = {} #存放玩家投票情况
    voted_code_list = [] #存放被投玩家，用于生成players_ticket
    text.delete(1.0, END)

# 更新GUI页面信息
def update(voted_players,vote_players):
    global players_code, undercover_code

    #更新当前玩家
    text.delete(1.0, END)
    text.insert(END, '玩家：')
    for player_code in players_code:
        text.insert(END, player_code + ' ')

    #更新卧底数
    text.insert(END, '\n\n'+'卧底：'+str(len(undercover_code)-undercover_died)+'人')

    #更新投票玩家和被投玩家
    text.insert(END, '\n\n投票玩家：')
    for player in vote_players:
        text.insert(END, player + '')

    text.insert(END, '\n\n可投玩家：')
    for player in voted_players:
        text.insert(END, player + '')

    #更新label显示
    labelvar.set('请'+str(vote_players[0])+'投票')

    #更新下拉框
    choice_code.set('选择可投玩家')
    choice_code['values'] = voted_players


    #测试
    # print players_code


# 异常处理
exception_code = 1
def start_game():
    global undercover_died, result_status, players_code, exception_code

    try:
        #初始化
        init()
        undercover_died = 0
        result_status = 'normal'

        #判定是否用完了单词
        if len(words_list) != 0:

            #分配卧底和词语
            allot_undercover()
            allot_words()

            #更新玩家情况
            update(voted_players=players_code, vote_players=players_code)

            tkMessageBox.showinfo(title='谁是卧底', message='惊心动魄的游戏即将开始，你们准备好了吗！')
            labelvar.set('请1号查看词语')

        else:
            tkMessageBox.showinfo(title='谁是卧底', message='天啊，我用尽了毕生所学到的词语了')
    except Exception:
        tkMessageBox.showinfo(title='谁是卧底', message='游戏崩溃，尝试着重新打开游戏')


def check_word():
    global word_num, display_status, players_code, players

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
            checkvar.set('隐藏单词')
        else:
            text.delete(1.0, END)
            labelvar.set('请' + str(word_num) + '号查看词语')
            display_status = 0
            checkvar.set('查看单词')
    else:
        text.delete(1.0, END)
        checkvar.set('查看单词')
        labelvar.set('请%s进行投票' % players_code[0])
        tkMessageBox.showinfo(title='谁是卧底', message='亲们，单词查看完毕，请大家进行描述')
        # 显示当前玩家
        update(voted_players=players_code, vote_players=players_code)

def vote():
    global players_code, players_ticket, max_ticket, max_ticket_codes, undercover_code, other_ticket_codes
    global exception_code, vote_num, result_status


    # 异常处理，防止未点击开始就点投票
    if exception_code == 1:
        tkMessageBox.showwarning(title='谁是卧底', message='亲，你是不是忘记了啥啦。请开始游戏')
        return '异常处理'

    # 获取票数
    if result_status == 'normal':
        #非平局的投票逻辑
        get_votes(voted_players=players_code, vote_players=players_code)
        if vote_num < len(players_code):
            labelvar.set('请%s投票' % players_code[vote_num ])
        else:
            #分析结果
            analysis_votes()
    else:
        #平局后的投票逻辑
        get_votes(voted_players=max_ticket_codes, vote_players=other_ticket_codes)
        if vote_num < len(other_ticket_codes):
            labelvar.set('请%s投票' % other_ticket_codes[vote_num])
        else:
            # 分析结果
            analysis_votes()




# 按钮
choice_player.pack(side=LEFT)

but1 = Button(frame, text="开始游戏", width=10, command=start_game)
but1.pack(side=LEFT)

checkvar = StringVar()
but2 = Button(frame, textvariable=checkvar, width=10, command=check_word)
checkvar.set('查看单词')
but2.pack(side=LEFT)

choice_code.pack(side=LEFT)

but3 = Button(frame, text="结束游戏", width=10, command=root.quit)
but3.pack(side=RIGHT)

but4 = Button(frame, text="投票", width=10, command=vote)
but4.pack(side=RIGHT)


frame.pack()
root.mainloop()




