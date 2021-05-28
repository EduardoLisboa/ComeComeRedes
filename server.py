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

cubePosIndex = 0
cubePosList = [
    "290,485", "349,221", "473,441", "47,451",
    "646,243", "526,595", "324,438", "88,418",
    "245,128", "349,452", "61,139", "443,711",
    "732,537", "684,266", "140,626", "148,401",
    "353,462", "445,662", "504,779", "736,238",
    "322,343", "239,361", "769,516", "25,351",
    "164,724", "735,330", "415,7", "317,186",
    "26,275", "201,647", "291,411", "532,32",
    "196,409", "532,25", "529,335", "95,683",
    "132,106", "672,588", "521,637", "170,180",
    "413,256", "233,83", "445,271", "35,319",
    "67,358", "123,429", "351,372", "277,510",
    "511,12", "773,51", "765,458", "706,451",
    "372,209", "140,58", "24,322", "509,390",
    "165,418", "160,321", "178,449", "308,605",
    "13,703", "216,603", "629,475", "538,750"
]

currentId = "0"
pos = ["0:50,50", "1:100,100"]
cubePos = '2:600,600'
def threaded_client(conn):
    global currentId, pos, cubePosIndex
    conn.send(str.encode(currentId))
    lastId = '0'
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
                if(reply == 'WINNER'):
                    print('We have a winner!')
                    conn.close()
                    quit()

                playerPosReply = reply.split('/')[0]
                cubePosReply = reply.split('/')[1]
                
                playerInfo = playerPosReply.split(':')
                id = int(playerInfo[0])
                pos[id] = playerPosReply


                cubeEaten = int(cubePosReply.split(':')[0])
                if cubeEaten == 3:
                    if(cubePosIndex > 63):
                        cubePosIndex = 0
                    cubeX = cubePosList[cubePosIndex]
                    cubeY = cubePosList[cubePosIndex]
                    cubePos = '2:' + str(cubeX) + ',' + str(cubeY)
                    cubePosIndex += 1
                else:
                    cubePos = cubePosReply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = str(pos[nid][:]) + '/' + cubePos
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
