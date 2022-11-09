import socket
from _thread import *
from game import Game
import pickle

server = "192.168.10.23"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server initialised. Waiting for connection... \n")
connected = set()
games = {}
idCount = 0

def t_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(8192).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Connection Lost... \n")
    try:
        del games[gameId]
        print("Closing Game ", gameId, ". Thank you for playing. \n")
    except:
        pass

    idCount -= 1
    conn.close()


    
while True:
    conn, addr = s.accept()
    print("New connection : ", addr, "\n")
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game... \n")
    else:
        games[gameId].ready = True
        p = 1

    
    start_new_thread(t_client, (conn, p, gameId))
