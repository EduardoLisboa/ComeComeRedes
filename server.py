import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
cubePos = '2:600,600'
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(4096)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                playerPosReply = reply.split('/')[0]
                cubePosReply = reply.split('/')[1]
                
                playerInfo = playerPosReply.split(':')
                id = int(playerInfo[0])
                pos[id] = playerPosReply

                print(f'Player pos: {playerPosReply} | Cube pos: {cubePosReply}')

                cubePos = cubePosReply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = str(pos[nid][:]) + '/' + cubePos
                # reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except Exception as err:
            print('Error on server side!', err)
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))