from socket import *
from multiprocessing import Process
import signal,sys
from time import sleep

from online_dict.dict_db import *
ADDR = ('127.0.0.1',8888)
class Server:
    def __init__(self,sockfd):
        self.sockfd = sockfd
        self.user = User()

    def do_listen(self):
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(ADDR)
        self.sockfd.listen(5)
    def res_msg(self,res,c):
        if res:
            c.send(b'Succ')
        else:
            c.send(b'fail')

    def request(self,c):
        while True:
            data = c.recv(4086).decode()
            print(data)
            data_list = data.split(' ')
            if not data or data_list[0] == 'C':
                c.close()
                sys.exit()
                break
            elif data_list[0] == 'R':
                res = self.user.do_register(data_list[1],data_list[2])
                self.res_msg(res,c)
            elif data_list[0] == 'L':
                res = self.user.do_login(data_list[1],data_list[2])
                self.res_msg(res,c)
            elif data_list[0] == 'Q':
                res = self.user.do_query(data_list[1],data_list[2])
                if res:
                    msg = 'Succ %s'%res
                    c.send(msg.encode())
                else:
                    c.send(b'fail')
            elif data_list[0] == 'H':
                print(data_list)
                name = data_list[1]
                res = self.user.get_history(name)
                for i in res:
                    msg = "%s   %-16s %s"%i
                    c.send(msg.encode())
                    sleep(1)
                c.send(b'##')







#大家网络
def main():
    s = socket()
    server = Server(s)
    server.do_listen()
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    #循环等待客户端连接
    print("Listen the port 8888")
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            server.user.db_close()
            sys.exit('服务端退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程
        p = Process(target=server.request,args=(c,))
        p.start()
if __name__ == '__main__':
    main()
