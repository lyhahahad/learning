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
        self.nonce = 0
        self.pownonce = 0

#메시지 전송자 클래스
class sender:
    def __init__(self, diff) -> None:
        self.diff = diff

    #메시지 해시캐시 진행
    def hashCash(self, msg):
        data = "%s %s "%(msg.text, msg.rand)
        data = data.encode()
        while(msg.hashString[:self.diff] != "0"*self.diff):
            print(msg.hashString[:self.diff])
            print("0"*self.diff)
            msg.pownonce +=1
            data_nonce = data+str(msg.pownonce).encode()
            msg.hashString = hashlib.sha1(data_nonce).hexdigest()
            print(msg.pownonce)
        return

    #메시지 전송
    def send(self, msg):
        msgs = pickle.dumps(msg)
        udp_client_socket.sendto(msgs, ("127.0.0.1", 3000))
        print("전송 성공")
        return


#메시지 수신자 클래스
class receiver:
    #같은 메시지를 반복적으로 보내는 것을 방지하기 위해 hashstring 저장.
    def __init__(self, diff) -> None:
        self.diff = diff
        # {임요한 : {hashString : , nonce : }}
        self.sender = []

    #메시지 해시캐시 검중.
    def verify(self, msg):
        data = "%s %s %s"%(msg.text, msg.nonce, msg.pownonce)
        msghash = data.encode()
        if(sender[msg.name])
        #메시지 반복 검사.
        if msghash == self.sender[msg.name]['hashString']:
            print("반복 메시징.")
            return False

        #난이도 검사
        if msghash[:self.diff] != "0"*self.diff: 
            print("난이도가 올바르지 않음.")
            return False

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
        msg0.hashString = ""
        msg0.nonce = 0
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