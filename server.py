import socket
from threading import Thread
import sys
from collections import defaultdict as df
import time

TARGET_HOST = "127.0.0.3"
TARGET_PORT = 33000

class Server:
    def __init__(self):
        self.rooms = df(list)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((TARGET_HOST, int(TARGET_PORT)))
        self.server.listen(100)
        ACCEPT_THREAD = Thread(target=self.acceptIncomingConnections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()

    def acceptIncomingConnections(self):
        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ":" + str(address[1]) + " Terhubung")
            Thread(target=self.handleClients, args=(connection,)).start()
            # start_new_thread(self.handleClients(connection))

    def handleClients(self, connection):
        user_id = connection.recv(1024).decode().replace("User ", "")
        room_id = connection.recv(1024).decode().replace("Join ", "")

        if room_id not in self.rooms:
            connection.send("Grup Baru Terbentuk".encode())
        else:
            connection.send("Selamat Datang di Grup".encode())

        self.rooms[room_id].append(connection)

        while True:
            try:
                message = connection.recv(1024)
                print(str(message.decode()))

                if message:
                    if str(message.decode()) == "FILE":
                        self.broadcastFile(connection, room_id, user_id)

                    else:
                        message_to_send = str(user_id) + " | " + message.decode()
                        self.broadcastMessage(connection, room_id, message_to_send)

                else:
                    self.remove(connection, room_id)

            except Exception as e:
                print(repr(e))
                print("Client disconnected")
                break

    def broadcastFile(self, connection, room_id, user_id):
        fileName = connection.recv(1024).decode()
        fileLength = connection.recv(1024).decode()
        for client in self.rooms[room_id]:
            if client !=connection:
                try:
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(fileName.encode())
                    time.sleep(0.1)
                    client.send(fileLength.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(fileName, fileLength)
        while str(total) != fileLength:
            data = connection.recv(1024)
            total = total +len(data)
            for client in self.rooms[room_id]:
                if client !=  connection:
                    try:
                        client.send(data)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("Terkirim")

    # Send text messages
    def broadcastMessage(self, connection, room_id, message):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)

if __name__ == "__main__":
    server = Server()