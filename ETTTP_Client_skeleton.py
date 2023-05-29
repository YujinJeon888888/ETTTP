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
        client_socket.connect(SERVER_ADDR)  
        print("연결되었습니다.")
        ###################################################################
        # Receive who will start first from the server
        ######################### Fill Out ################################
        ctext=client_socket.recv(SIZE).decode()
        ctext_list=ctext.split("\r\n")
        if (ctext_list[0]!=("SEND ETTTP/1.0 "))or(ctext_list[1]!="Host: "+str(SERVER_IP)):#ETTTP형식에 맞지 않으면
            print("비정상 종료")
            client_socket.close()
            exit()
        if ctext_list[2]=="start is server":
            start=0
            print("start is server")
            # Send ACK 
            client_socket.send(bytes("ACK ETTTP/1.0 \r\n"
            +"Host: "+MY_IP+"\r\n"
            +"start is server","utf-8"))
        else :
            start=1
            print("start is client")
            # Send ACK 
            client_socket.send(bytes("ACK ETTTP/1.0 \r\n"
            +"Host: "+MY_IP+"\r\n"
            +"start is client","utf-8"))
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        