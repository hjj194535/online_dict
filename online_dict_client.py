# -*- coding: utf-8 -*-
from socket import *
import sys
import getpass
import hashlib

ADDR = ('127.0.0.1',8888)

def encrypt(pwd):
    salt = '^&%_5g*A'
    hash = hashlib.md5(salt.encode())
    hash.update(pwd.encode())
    new_pwd = hash.hexdigest()
    return new_pwd


class Client:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def second_menu(self,name):
        print('===============Command===============')
        print('==============1.查单词 ================')
        print('==============2.查历史记录 =============')
        print('==============3.退出 ==================')
        print('欢迎%s登录'%name)

    def firt_menu(self):
        print('===============Command===============')
        print('===============  1.登录 ===============')
        print('===============  2.注册 ===============')
        print('===============  3.注销 ===============')
        print('=====================================')

    def do_query(self,name):
        while True:
            word = input('请输入要查询的单词:')
            msg = 'Q %s %s'%(word,name)
            self.sockfd.send(msg.encode())
            data = self.sockfd.recv(4086).decode()
            return data

    def do_history(self,name):
        msg = "H " + name
        self.sockfd.send(msg.encode())
        while True:
            data = self.sockfd.recv(1024).decode()
            if data == '##':
                break
            print(data)

    def send_user_info(self,name,pwd,operation):
        new_pwd = encrypt(pwd)
        msg = '%s %s %s' % (operation,name, new_pwd)
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        return data

    def do_register(self):
        while True:
            name = input('请输入用户名:')
            pwd = getpass.getpass('请输入密码:')
            if ' ' in name or ' ' in pwd :
                print('用户名或密码中不能包含空格')
                continue
            else:
                data = self.send_user_info(name,pwd,'R')
                return (data,name)

    def do_login(self):
        while True:
            name = input('请输入用户名:')
            pwd = getpass.getpass('请输入密码:')
            data = self.send_user_info(name,pwd,'L')
            return (data,name)



    def handle_second_menu(self,name):
        while True:
            self.second_menu(name)
            cmd = input('选项(1,2,3):')
            if cmd == '1':
                data = self.do_query(name)
                data_list = data.split(' ',1)
                if data_list[0] == 'Succ':
                    print(data_list[1])
                else:
                    print('您查找的单词不存在')
                    continue
            elif cmd == '2':
                self.do_history(name)
            elif cmd == '3':
                return cmd
            else:
                print('输入有误!请重新输入')


def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    client = Client(sockfd)
    while True:
        client.firt_menu()
        cmd = input('选项(1,2,3):')
        if cmd == '1':
            res = client.do_login()
            msg = res[0]
            name = res[1]
            if msg == 'Succ':
                client.handle_second_menu(name)
            else:
                print('登录失败,请重新登录')
                continue
        if cmd == '2':
            res = client.do_login()
            msg = res[0]
            name = res[1]
            if msg == 'Succ':
                client.handle_second_menu(name)
            else:
                print('注册失败,请重新注册!!!')
                continue
        if cmd == '3':
            sockfd.send(b'C')
            sockfd.close()
            sys.exit('客户端退出')


if __name__ == '__main__':
    main()