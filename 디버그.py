def remove_substring(string, start, end):
        return string[:start] + string[end+1:]

msg="SEND ETTTP/1.0 \r\nHost: 192.168.0.2 \r\nNew-Move: (1, 2) \r\n\r\n"
start_index = 1
end_index = 1
if len(msg) > 0:#메세지 비어있는 것 들어올 경우 예외처리
    if msg[0]=="A":#ACK
        start_index = msg.find("A")
        end_index = msg.find(" ")
    elif msg[0]=="S":#SEND
        start_index = msg.find("S")
        end_index = msg.find(" ")
#1. 메세지를 띄어쓰기 후까지만 활용
msg = remove_substring(msg, start_index, end_index)
Ttext_list=msg.split("\r\n")
print(Ttext_list)
print(msg)