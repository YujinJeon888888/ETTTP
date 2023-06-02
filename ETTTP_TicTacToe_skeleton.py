'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread
from unicodedata import decimal

SIZE=1024

#추가한 함수.
def remove_substring(string, start, end):
        return string[:start] + string[end+1:]

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr#상대 ip
        self.recv_ip = src_addr#내 ip
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        rcv_msg =  self.socket.recv(SIZE).decode() # get message using socket
        #ETTTP 형식 맞는지 확인
        ETTTP_result=True if (check_msg(rcv_msg,self.recv_ip) == True) else  False
        #ETTTP_result 따라 quit여부 결정
        #if ETTTP_result is false - 프로그램 종료.
        if not ETTTP_result:
            self.quit()       
        # If message is valid - send ack, update board and change turn
        #send ack
        rcv_msg_list=rcv_msg.split("\r\n")
        self.socket.send(bytes("ACK ETTTP/1.0\r\n"+ "Host:"+self.send_ip+"\r\n"
        +rcv_msg_list[2],"utf-8"))
        #rcv_msg_list[2] : New-Move:(a,b) 형태의, 선택한 블록의 위치.
        #loc 정하는 코드
        start_index = rcv_msg.find("(")
        end_index = rcv_msg.find(")")
        location=rcv_msg[start_index + 1 : end_index]
        #행 인덱스 * 3
        row=int(location[0])*3
        #열 인덱스
        col=int(location[2])
        #둘이 더한 게 loc
        loc= row+col # received next-move (예시로 loc = 5로 설정)
        
        print("상대방이 선택한 칸은 ("+str(location[0])+", "+str(location[2])+") 입니다.")
        ######################################################   
        #update board and change turn
            
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.computer, loc, get=True)
        if self.state == self.active:  
            self.my_turn = 1
            self.l_status_bullet.config(fg='green')
            self.l_status ['text'] = ['Ready']
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")

        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        #1. message를 받는다. 
        #2. message를 분석해서 어느 칸을 선택했는지 본다. 
        #3. 이미 선택한 칸이면 send message 못하고 돌려보내진다.
        
        debugMsg=d_msg.replace("\r\n","\\r\\n")
        print("디버그 창에서",end=" ")
        print(debugMsg+"라는 메시지를 받았어요")

        
        start_index = d_msg.find("(")
        end_index = d_msg.find(")")
        location=d_msg[start_index + 1 : end_index]
        #행 인덱스 * 3
        row=int(location[0])*3
        #열 인덱스
        col=int(location[2])
        #둘이 더한 게 user_move
        user_move=row+col
        
        print("내가 선택한 칸은 ("+str(location[0])+", "+str(location[2])+") 입니다.")

        #유효한 자리인지 확인한다.
        if self.board[user_move] != 0 : # 0으로 초기화했는데 0이 아니라는 건 이미 차지된 자리라는 뜻
            print("유효하지 않은 칸")
            return
        #유효한 자리인지 확인 했으면 peer에게 message를 보낸다.
        '''
        Send message to peer
        '''
        self.socket.send(bytes(d_msg,"utf-8")) # 디버그 창에 입력한 ETTTP 형식의 message를 그대로 보낸다.
        print("소켓을 통해 peer에게 debug message를 보냈어요")
        '''
        Get ack
        '''
        rcv_msg=self.socket.recv(SIZE).decode()
        #ETTTP형식 맞는지 확인.
        ETTTP_result=True if (check_msg(rcv_msg,self.recv_ip) == True) else  False
        #result 따라 quit여부 결정한다.
        if not ETTTP_result:
            self.quit()
        else:
            #Mark on tic-tac-toe board
            print("peer로부터 ACK를 받았어요")
            #update_board에서 보드판 바뀌게 하기 위한 변수
            loc = user_move # peer's move, from 0 to 8
            #상대편에서는 get_move에서 업데이트
            
        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3) #row는 3으로 나눈 몫, col은 3으로 나눈 나머지
        ###################  Fill Out  #######################
        # send message and check ACK
        #블록을 선택하면 message를 보낸다. 이미 차지된 칸인지 아닌지는 my_move에서 확인. 
        print("내가 선택한 칸은 ("+str(row)+", "+str(col)+") 입니다.")
        self.socket.send(bytes("SEND ETTTP/1.0\r\n"+
        "Host:"+self.send_ip+"\r\n"
        +"New-Move:("+str(row)+","+str(col)+")\r\n\r\n","utf-8"))
        #ACK 받고
        rcv_msg=self.socket.recv(SIZE).decode()
        #ETTTP형식 맞는지 확인
        ETTTP_result=True if (check_msg(rcv_msg,self.recv_ip) == True) else  False
        #result 따라 quit여부 결정한다.
        if not ETTTP_result:
            self.quit()
        else:
            return True
        ######################################################  




    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
    
        result=False#초기값
        if get==False: # if get is false, it means this user is winner and need to report the result "first" #이긴 사람 시점
          #게임 결과를 먼저 전송.
            self.socket.send(bytes(
                "RESULT ETTTP/1.0\r\n"+
                "Host:"+self.send_ip+"\r\n"+
                "Winner:ME\r\n\r\n","utf-8"))
            #상대방이 게임 결과 보낸게 ETTTP 맞는형식인지 확인.
            rcv_msg=self.socket.recv(SIZE).decode()         
            rcv_msg_list=rcv_msg.split("\r\n")
            #ETTTP형식 맞는지 확인
            ETTTP_result=True if (check_msg(rcv_msg,self.recv_ip) == True) else  False
            #result 따라 quit여부 결정
            if not ETTTP_result:
                self.quit()
            else:
                # Winner:ME이면 false. 둘 다 WIN 일 수는 없으니까 false return.
                if(rcv_msg_list[2]=="Winner:ME"):
                    result=False        
                # Winner:YOU이면 true.
                if(rcv_msg_list[2]=="Winner:YOU"):
                    result=True        
        else: #진 사람 시점
            #상대방이 게임 결과 보낸게 ETTTP 맞는형식인지 확인.
            rcv_msg=self.socket.recv(SIZE).decode()
            rcv_msg_list=rcv_msg.split("\r\n")
            ETTTP_result=True if (check_msg(rcv_msg,self.recv_ip) == True) else  False
            #result 따라 quit여부 결정
            if not ETTTP_result:
                self.quit()
            else:
                # Winner:ME이면 True. 
                if(rcv_msg_list[2]=="Winner:ME"):
                    result=True        
                # Winner:YOU이면 False. 둘 다 LOSE 일 수는 없으니까 false return.
                if(rcv_msg_list[2]=="Winner:YOU"):
                    result=False  
                #이제 내 결과도 보내기       
                self.socket.send(bytes(
                "RESULT ETTTP/1.0\r\n"+
                "Host:"+self.send_ip+"\r\n"+ 
                "Winner:YOU\r\n\r\n","utf-8")) 
               
        return result  #맞는지 아닌지 결과 리턴
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class



def check_msg(msg, recv_ip): #recv_ip: My IP. 
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    #0. SEND,ACK,RESULT string 이후의 string만 추출하기 위해 index를 확인. 
    #변수초기화
    start_index = 1
    end_index = 1
    if len(msg) > 0: #len(msg)==0 일 때 예외처리.
        if msg[0]=="A":#ACK
            start_index = msg.find("A")
            end_index = msg.find(" ")
        elif msg[0]=="S":#SEND
            start_index = msg.find("S")
            end_index = msg.find(" ")
        elif msg[0]=="R":#RESULT
            start_index = msg.find("R")
            end_index = msg.find(" ")
    #1. SEND,ACK,RESULT string 이후의 string만 활용
    msg = remove_substring(msg, start_index, end_index)
    Ttext_list=msg.split("\r\n")
    if (Ttext_list[0]!=("ETTTP/1.0"))or(Ttext_list[1]!="Host:"+str(recv_ip)):
      #1) ETTTP 형식에 맞는지 확인 or 2) 내 IP주소와 받은 message에서의 IP주소가 같은지 확인.
            print("ETTTP 형식에 맞지 않는 메시지입니다.")          
            print("비정상 종료")
            return False
    ######################################################  
    return True
    ######################################################  

