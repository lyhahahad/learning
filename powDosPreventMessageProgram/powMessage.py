import hashlib
import pickle
import threading
import socket
udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#메시지 클래스
class msg:
    def __init__(self) :
        self.name = ""
        self.text = ""
        self.pownonce = 0

#메시지 전송자 클래스
class sender:
    def __init__(self, diff) -> None:
        self.diff = diff
        self.nonce = 0

    #메시지 해시캐시 진행.
    def hashCash(self, msg):
        data = "%s %s "%(msg.text,self.nonce)
        data = data.encode()
        data_nonce = data+str(msg.pownonce).encode()
        hashstring = hashlib.sha1(data_nonce).hexdigest()        
        while(hashstring[:self.diff] != "0"*self.diff):
            msg.pownonce +=1
            data_nonce = data+str(msg.pownonce).encode()
            hashstring = hashlib.sha1(data_nonce).hexdigest()
            print(hashstring)
        return

    #메시지 전송
    def send(self, msg):
        msgs = pickle.dumps(msg)
        udp_client_socket.sendto(msgs, ("127.0.0.1", 3000))
        self.nonce +=1
        print("전송 성공")
        return


#메시지 수신자 클래스
class receiver:
    #같은 메시지를 반복적으로 보내는 것을 방지하기 위해 hashstring 저장.
    def __init__(self, diff) -> None:
        self.diff = diff
        # {임요한 : {hashString : , nonce : }}
        self.sender = {}

    #메시지 해시캐시 검중.
    def verify(self, msg):
        if(msg.name not in self.sender):
            self.sender[msg.name] = ["", 0]
        data = "%s %s %s"%(msg.text, self.sender[msg.name][1], msg.pownonce)
        msghash = hashlib.sha1(data.encode()).hexdigest()
        print(msghash)
        #메시지 반복 검사.
        if msghash == self.sender[msg.name][0]:
            print("반복 메시징.")
            return False

        #난이도 검사
        if msghash[:self.diff] != "0"*self.diff: 
            print("난이도가 올바르지 않음.")
            return False

        sender[msg.name][0] = msghash
        sender[msg.name][1] += 1
        return True
        

    def receiverServer():
            server_addr_port = ("127.0.0.1", 3000)
            buffersize = 100000000
            udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            udp_server_socket.bind(server_addr_port)
            udp_server_socket.setblocking(False)
            print("UDP server is up and listening")

sender = sender(2)
receiver = receiver(2)
msg0 = msg()    

def senderThread():
    msg0.name = input("이름을 입력하세요 : ")
    sender.diff = int(input("난이도를 입력하세요 : "))
    while(True):
        msg0.text = input("text : ")
        sender.hashCash(msg0)
        sender.send(msg0)

def receiverThread():
    server_addr_port = ("127.0.0.1", 3000)
    buffersize = 100000000
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind(server_addr_port)
    udp_server_socket.setblocking(False)
    print("UDP server is up and listening")
    receiver.diff = int(input("난이도는 선택하세요 : "))

    while(True):
        try:
            rec_data = udp_server_socket.recvfrom(buffersize)
        except BlockingIOError:
            continue
        msg = pickle.loads(rec_data[0])
        if(receiver.verify(msg) == True):
            receiver.receive(msg)
            
while(True):
    comm = input("sender or receiver : ")
    if comm == "sender":
        s_T = threading.Thread(target=senderThread)
        s_T.start()
        s_T.join()
    elif comm == "receiver":
        r_T = threading.Thread(target=receiverThread)
        r_T.start()
        r_T.join()