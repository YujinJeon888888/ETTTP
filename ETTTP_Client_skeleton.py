'''
  ETTTP_Client_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

from http import client
import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        def remove_substring(string, start, end):
            return string[:start] + string[end+1:]
        client_socket.connect(SERVER_ADDR)  
        print("연결되었습니다.")
        ###################################################################
        # Receive who will start first from the server
        ######################### Fill Out ################################
        ctext=client_socket.recv(SIZE).decode()#server가 보낸 메세지 까본다.
        #0. 메세지를 첫 띄어쓰기 나올 때 이후만 떼어씀
        start_index = ctext.find("S")
        end_index = ctext.find(" ")
        #1. 메세지를 띄어쓰기 후까지만 활용
        ctext = remove_substring(ctext, start_index, end_index)
        ctext_list=ctext.split("\r\n")
        if (ctext_list[0]!=("ETTTP/1.0"))or(ctext_list[1]!="Host:"+MY_IP):#1)ETTTP형식에 맞지 않으면. 2)나한테 온 건지 까봐야 함.
            print("비정상 종료")
            client_socket.close()
            exit()
        if ctext_list[2]=="First-Move: ME":
            start=0
            print("start is server")
            # Send ACK 
            client_socket.send(bytes("ACK ETTTP/1.0\r\n"
            +"Host:"+SERVER_IP+"\r\n"
            +"First-Move: ME\r\n\r\n" ,"utf-8"))
        else :
            start=1
            print("start is client")
            # Send ACK 
            client_socket.send(bytes("ACK ETTTP/1.0\r\n"
            +"Host:"+SERVER_IP+"\r\n"
            +"First-Move: YOU\r\n\r\n" ,"utf-8"))
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
