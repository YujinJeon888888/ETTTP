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
        def remove_substring(string, start, end):
            return string[:start] + string[end+1:]
        #ETTTP형식의 메시지인지 확인하기 위해 substring을 추출하는 함수를 새로 생성
        client_socket, client_addr = server_socket.accept()
        print("클라이언트의 주소는 "+str(client_addr)+"입니다. ")
        start = random.randrange(0,2)
        # select random to start
        
        ###################################################################
        # Send start move information to peer
        ######################### Fill Out ################################
        
        if start==0:
          #서버 먼저 시작.
          #server가 client에게 시작한다는 message를 전송.
            client_socket.send(bytes("SEND ETTTP/1.0\r\n"
            +"Host:"+client_addr[0]+"\r\n"
            +"First-Move: ME\r\n\r\n" ,"utf-8"))
            print("start is server")
            # Receive ack - if ack is correct, start game
            stext=client_socket.recv(SIZE).decode()
            #client가 보낸 ACK message를 받아서 stext에 넣음.
            #0. ETTTP message에서, ACK string 이후의 string만 추출하기 위해 index를 확인. 
            start_index = stext.find("A")
            end_index = stext.find(" ")
            #1. ACK string 이후의 string만 활용
            stext = remove_substring(stext, start_index, end_index)
            stext_list=stext.split("\r\n")
            if (stext_list[0]!=("ETTTP/1.0"))or(stext_list[1]!="Host:"+MY_IP):
              #1) ETTTP 형식에 맞는지 확인 or 2) 내 IP주소와 받은 message에서의 IP주소가 같은지 확인.
                print("비정상 종료")
                client_socket.close()
                break          
            else: 
                print("ACK 정상 수신")
            
        else: 
          #클라이언트 먼저 시작.
          #server가 client에게 시작한다는 message를 전송.
            client_socket.send(bytes("SEND ETTTP/1.0\r\n"
            +"Host:"+client_addr[0]+"\r\n"
            +"First-Move: YOU\r\n\r\n" ,"utf-8"))
            print("start is client")
            # Receive ack - if ack is correct, start game
            stext=client_socket.recv(SIZE).decode()
            #client가 보낸 ACK message를 받아서 stext에 넣음.
            #0. ETTTP message에서, ACK string 이후의 string만 추출하기 위해 index를 확인. 
            start_index = stext.find("A")
            end_index = stext.find(" ")
            #1. ACK string 이후의 string만 활용
            stext = remove_substring(stext, start_index, end_index)
            stext_list=stext.split("\r\n")
            if (stext_list[0]!=("ETTTP/1.0"))or(stext_list[1]!="Host:"+MY_IP):
              #1) ETTTP 형식에 맞는지 확인 or 2) 내 IP주소와 받은 message에서의 IP주소가 같은지 확인.
                print("비정상 종료")
                client_socket.close()
                break
            else:
                print("ACK 정상 수신")
        ###################################################################

        # Start game        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        break
    server_socket.close()

              
        ###################################################################
 
