import itchat
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from math import *
from shutil import *
import numpy as np
import os
import datetime
from copy import deepcopy
import random

import threading
import time


class LoginDlg(QMainWindow):
    add_record = pyqtSignal(str, str)
    def __init__(self, name_list, group_list):
        super(LoginDlg, self).__init__()
        
        
        self.setWindowTitle('TheyChat')  
        screenRect = QApplication.desktop().screenGeometry()
        self.sh = screenRect.height()
        self.sw = screenRect.width()
        win_w = 500
        win_h = 600
        base_height = 25
        base_weight = 60
        
        self.name_lise = name_list
        self.group_list = group_list
        self.current_name = ''
        
        self.setGeometry((self.sw - win_w) // 2, (self.sh - win_h) // 2, win_w, win_h)
        
        self.lbl_name = QLabel(self)
        self.lbl_name.setText('好友：')
        self.lbl_name.setGeometry(35, 25, 60, 25)
        self.fnd_list = QListWidget(self)
        self.fnd_list.itemClicked.connect(self.set_friend)
        self.fnd_list.setGeometry(25, 50, 120, 275)
        
        for i, fname in enumerate(name_list):
            if i > 0:
                self.fnd_list.addItem(fname)
        
        self.lbl_name = QLabel(self)
        self.lbl_name.setText('群组：')
        self.lbl_name.setGeometry(35, 335, 60, 25)
        self.grp_list = QListWidget(self)
        self.grp_list.itemClicked.connect(self.set_group)
        self.grp_list.setGeometry(25, 370, 120, 205)
        
        for gname in group_list:
            self.grp_list.addItem(gname)
        
        self.msgs = QTextEdit(self)
        self.msgs.setGeometry(155, 25, 320, 300)
        
        self.lbl_name = QLabel(self)
        self.lbl_name.setText('发送给：')
        self.lbl_name.setGeometry(170, 335, 60, 25)
        self.p_name = QLabel(self)
        self.p_name.setGeometry(230, 335, 120, 25)

        self.btn_cal = QPushButton("发送")
        self.btn_cal.clicked.connect(self.send)
        self.btn_cal.setShortcut(Qt.Key_Enter)
        self.btn_cal.setGeometry(370, 335, 90, 25) 
        self.layout().addWidget(self.btn_cal)
        
        self.send_msg = QTextEdit(self)
        self.send_msg.setGeometry(155, 370, 320, 205)
        
        
        self.add_record.connect(self.add_rec)
        #self.p_pw.setEchoMode(QLineEdit.Password)
        
    def set_friend(self, sel_fnd):
        #if len(item) > 0:
        #sel_fnd = item 
        self.p_name.setText(sel_fnd.text())
        self.current_name = self.name_lise[sel_fnd.text()]
        
    def set_group(self, sel_fnd):
        #if len(item) > 0:
        #sel_fnd = item 
        self.p_name.setText(sel_fnd.text())
        self.current_name = self.group_list[sel_fnd.text()]
        
    def send(self):
        # lqw: '@dd64ab9e8a80e94102b05158e5b0069a1588472b31c4adf2f4806bbec05a4eda'
        # filehelper: 'filehelper'
        reply = self.send_msg.toPlainText()
        itchat.send(reply, toUserName=self.current_name)
        print("You send: " + reply)
        self.add_record.emit(self.current_name, reply)
        self.send_msg.setText('')
    
    def add_rec(self, name, msg):
        #print(name, msg)
        if name.startswith('@'):
            fnd = itchat.search_friends(userName=name)
            if fnd is None:
                self.msgs.append('You send: {}'.format(msg))
            else:
                if fnd.RemarkName != '':
                    tname = fnd.RemarkName
                else:
                    tname = fnd.NickName
                self.msgs.append('{} send: {}'.format(tname, msg))
        else:
            self.msgs.append('{} send: {}'.format(name, msg))
        
        
        
#只对群消息有效
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def text_reply(msg):
    #print(msg)

    if msg["FromUserName"] == uid:
        print("You send: " + msg["Text"])
        ex1.add_record.emit(msg.ActualUserName, msg.text)
    else:
        #print(msg)
        print("@"+msg.actualNickName+" send:"+msg.text)
        
        fnd = itchat.search_friends(userName=msg.ActualUserName)
        if fnd is None:
            # not friends
            ex1.add_record.emit(msg.ActualNickName, msg.text)
        else:
            ex1.add_record.emit(msg.ActualUserName, msg.text)
        #return "@"+msg.actualNickName+" 发了一条信息："+msg.text    #if(msg["Text"]=="11")
    #return "自动回复数据xx:"+msg["Text"]
    
#只对个人用户有效
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    #print(msg)
    if msg["FromUserName"] == uid:
        ex1.add_record.emit(msg["FromUserName"], msg["Text"])
        print("You send: " + msg["Text"])
    else:
        ex1.add_record.emit(msg["FromUserName"], msg.text)
        inuserx = itchat.search_friends(userName=msg["FromUserName"])["NickName"]
        print("@"+inuserx+" send:"+msg.text)
        #return "@"+msg.actualNickName+" 发了一条信息："+msg.text    #if(msg["Text"]=="11")
    #print(msg["Text"])
    #return "自动回复数据:"+msg["Text"]


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        #print ("开始线程：" + self.name)
        itchat.run()
        #print ("退出线程：" + self.name)

#def run_wechat():
#    itchat.run()

if __name__ == '__main__':
    
    itchat.auto_login(hotReload=True)
    #itchat.auto_login(enableCmdQR=True)
    
    #uid=itchat.search_friends()
    friends = itchat.get_friends(update=True)
    uid = friends[0].UserName
    print(friends[0])
    
    name_list = {}
    for fnd in friends:
        if fnd.RemarkName != '':
            name_list[fnd.RemarkName] = fnd.UserName
        else:
            name_list[fnd.NickName] = fnd.UserName
            
        #name_list.append(fnd.NickName)
        #self.listview.addItem(fnd.NickName)
    
    group_list = {}
    groups = itchat.get_chatrooms(update=True)
    for grp in groups:
        if grp.RemarkName != '':
            group_list[grp.RemarkName] = grp.UserName
        else:
            group_list[grp.NickName] = grp.UserName
        #print(grp)
    
    #thread1.join()
    
    
    #name_list = {}
    #group_list = {}
    
    
    
    app = QApplication(sys.argv)
    app.setStyle('WindowsXP')
    ex1 = LoginDlg(name_list, group_list)
    thread1 = myThread(1, "Thread-1", 1)
    thread1.start()
    ex1.show()
    #ex1 = Example()
    sys.exit(app.exec_())
    
