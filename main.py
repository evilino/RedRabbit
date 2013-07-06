﻿# coding=UTF-8
import os
import time
import ffext

def GetNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

class player_mgr_t(object):
    def __init__(self):
        self.all_players = {}
    def get(self, session_id_):
        return self.all_players.get(session_id_)
    def remove(self, session_id_):
        del  self.all_players[session_id_]
    def add(self, session_id_, player):
        self.all_players[session_id_] = player
    def size(self):
        return len(self.all_players)
    def idlist(self):
        return self.all_players.keys()

class player_t(object):
    def __init__(self, session_id_):
        self.session_id = session_id_;
    def id():
        return self.session_id

#这个修饰器的意思是注册process_chat函数接收cmd=1的消息
@ffext.session_call(1)
def process_chat(session_id, msg):
    content = msg[0]
    if content == 'reload':
        os.system('./update_code.sh')
        ret = ffext.reload('main')#重载此脚本
        ffext.broadcast_msg_session(1, '<b><font color="#ff0000"> main.py已完成重载'\
                                       '%s</font></b>'%(str(ret)))
        return

    print("process_chat session_id=%s content=%s"%(session_id, content))

    ret = '<font color="#008000">[%s %s]:</font>%s'%(session_id, GetNowTime(), content)
    ffext.broadcast_msg_session(1, ret)
    


#这个修饰器的意思是注册下面函数处理验证client账号密码，
#session_key为账号密码组合体，client第一个包必为登陆包
@ffext.session_verify_callback
def my_session_verify(session_key, online_time, ip, gate_name):
    return [session_key]#需要返回数组，验证成功，第一个元素为分配的id，
						#第二个元素可以不设置，若设置gate会返回给client，login gate的时候
						#需要第二个元素返回分配的game gate

#此修饰器的作用是注册下面函数处理用户下线 
@ffext.session_offline_callback
def my_session_offline(session_id, online_time):
    content = '<font color="#ff0000">[%s %s] offline </font>'%(session_id, GetNowTime())
    ffext.broadcast_msg_session(1, content)
    ffext.singleton(player_mgr_t).remove(session_id)
    ffext.broadcast_msg_session(1, '<font color="#ff0000">当前在线:</font>')
    ffext.broadcast_msg_session(1, ffext.singleton(player_mgr_t).idlist())

#此修饰器的作用是注册下面函数处理client切换到此场景服务器
@ffext.session_enter_callback
def my_session_enter(session_id, from_scene, extra_data):
    #单播接口
    ffext.send_msg_session(session_id, 1, '<font color="#ff0000">测试单播接口！欢迎你！'\
                           				  '</font>')
    content = '<font color="#ff0000">[%s %s] online </font>'%(session_id, GetNowTime())
    ffext.broadcast_msg_session(1, content)
    player = player_t(session_id)
    ffext.singleton(player_mgr_t).add(session_id, player)
    ffext.broadcast_msg_session(1, '<font color="#ff0000">当前在线:</font>')
    ffext.broadcast_msg_session(1, ffext.singleton(player_mgr_t).idlist())

print("loading.......")

#数据库操作示例
def sqlite_test():
    db = ffext.ffdb_create('sqlite://./test.db')
    db.query('CREATE TABLE  IF NOT EXISTS dumy (A int, c float, b varchar(200), primary key (A))')
    db.query('insert into dumy values(1, 2.3, "ttttTTccc")')
    def cb(ret):
        print(ret.flag, ret.result, ret.column, ffext.DB_CALLBACK_DICT)
    db.query('select * from dumy', cb)#cb 为异步回调函数
    ffext.reload('main')#重载此脚本

def mysql_test():
    db = ffext.ffdb_create('mysql://localhost:3306/root/root/fftest')
    db.query('CREATE TABLE  IF NOT EXISTS dumy (A int, c float, b varchar(200), primary key (A))')
    db.query('insert into dumy values(1, 2.3, "ttttTTccc")')
    def cb(ret):
        print(ret.flag, ret.result, ret.column, ffext.DB_CALLBACK_DICT)
    db.query('select * from dumy', cb)#cb 为异步回调函数
    ffext.reload('main')#重载此脚本

