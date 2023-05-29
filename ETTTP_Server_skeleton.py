'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)#���� ������.
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    print("서버 대기중")
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        ######################### Fill Out ################################

        if start==0:#서버 먼저 시작.
            client_socket.send(bytes("SEND ETTTP/1.0 \r\n"
            +"Host: "+MY_IP+"\r\n"
            +"start is server" ,"utf-8"))
            print("start is server")
            # Receive ack - if ack is correct, start game
            stext=client_socket.recv(SIZE).decode()
            stext_list=stext.split("\r\n")
            if (stext_list[0]!=("ACK ETTTP/1.0 "))or(stext_list[1]!="Host: "+str(client_addr[0])):#ETTTP형식에 맞지 않으면
                print("비정상 종료")
                client_socket.close()
                break
            else: 
                print("ACK 정상 수신")
            
        else: #클라이언트 먼저 시작.
            client_socket.send(bytes("SEND ETTTP/1.0 \r\n"
            +"Host: "+MY_IP+"\r\n"
            +"start is client","utf-8"))
            print("start is client")
            # Receive ack - if ack is correct, start game
            stext=client_socket.recv(SIZE).decode()
            stext_list=stext.split("\r\n")
            if (stext_list[0]!=("ACK ETTTP/1.0 "))or(stext_list[1]!="Host: "+str(client_addr[0])):#ETTTP형식에 맞지 않으면
                print("비정상 종료")
                client_socket.close()
                break
            else:
               print("ACK 정상 수신")
                
            AckCheckText = client_socket.recv(SIZE).decode()
            if AckCheckText != ("ACK"):
                print("ACK를 수신하지 못함")
            else:
                root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
                root.play(start_user=start)
                root.mainloop()
        
                client_socket.close()
        
                break
                server_socket.close()

                
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        break
        server_socket.close()

              
        ###################################################################
 
