import socket
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import time
import os

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 33000


class GUI:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((TARGET_HOST, TARGET_PORT))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login ChatProgjar")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=400, bg="#45818e")

        self.pls = tk.Label(self.login, text="Silakan Login ke Chatroom", justify=tk.CENTER, font="Helvetica 12 bold", bg="#45818e")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username ", font="Helvetica 11", bg="#45818e")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 11")
        self.userEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.3)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Chatroom ID ", font="Helvetica 11", bg="#45818e")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.4)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)

        self.go = tk.Button(self.login, text="LOGIN", font="Helvetica 12 bold", bg="#1c3439", fg="#fff",
                            command=lambda: self.authenticate(self.userEntryName.get(), self.roomEntryName.get()))
        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def authenticate(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))

        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title("Chatroom")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=400, height=600, bg="#45818e")
        self.chatBoxHead = tk.Label(self.Window,
                                    bg="#45818e",
                                    fg="#EAECEE",
                                    text=self.name,
                                    font="Helvetica 11 bold",
                                    pady=5)

        self.chatBoxHead.place(relwidth=1)

        self.textCons = tk.Text(self.Window, width=20, height=2, bg="#dae6e8", fg="#000", padx=5, pady=5,
                                font="Helvetica 11")
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        self.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)

        self.labelBottom = tk.Label(self.Window, bg="#45818e", height=80)
        self.labelBottom.place(relwidth=1, rely=0.8)

        self.messageBox = tk.Entry(self.labelBottom, bg="#dae6e8", fg="#000", font="Helvetica 11")
        self.messageBox.place(relwidth=0.74, relheight=0.03, rely=0.008, relx=0.011)
        self.messageBox.focus()

        self.textSendButton = tk.Button(self.labelBottom, text="Kirim", width=10, bg="#1c3439",
                                        font="Helvetica 10 bold", fg="#fff",
                                        command=lambda: self.sendTextButton(self.messageBox.get()))
        self.textSendButton.place(relx=0.77, rely=0.008, relheight=0.03, relwidth=0.22)

        self.labelFile = tk.Label(self.Window, bg="#45818e", height=70)
        self.labelFile.place(relwidth=1, rely=0.9)

        self.fileLocation = tk.Label(self.labelFile, text="Upload file", bg="#2C3E50", fg="#EAECEE",
                                     font="Helvetica 11")
        self.fileLocation.place(relwidth=0.65, relheight=0.03, rely=0.008, relx=0.011)

        self.fileBrowseButton = tk.Button(self.labelFile, text="Cari", width=10, bg="#1c3439", font="Helvetica 10", fg="#fff",
                                          command=self.browseFile)
        self.fileBrowseButton.place(relx=0.67, rely=0.008, relheight=0.03, relwidth=0.15)

        self.fileSendButton = tk.Button(self.labelFile, text="Kirim File", width=10,font="Helvetica 10", bg="#1c3439",fg="#fff",
                                        command=self.sendFile)
        self.fileSendButton.place(relx=0.84, rely=0.008, relheight=0.03, relwidth=0.15)

        self.fileName = ""

    def browseFile(self):
        self.fileName = filedialog.askopenfilename(initialdir="/",
                                                   title="Pilih File",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
        self.fileLocation.configure(text="File Terbuka: " + self.fileName)

    def sendFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(str("client_" + os.path.basename(self.fileName)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.fileName)).encode())
        time.sleep(0.1)

        file = open(self.fileName, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state=tk.NORMAL)
        self.textCons.insert(tk.END, "You | " + str(os.path.basename(self.fileName)) + " Terkirim\n\n")
        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def sendTextButton(self, message):
        self.textCons.config(state=tk.DISABLED)
        self.message = message
        self.messageBox.delete(0, tk.END)
        thread = threading.Thread(target=self.sendText)
        thread.start()

    def sendText(self):
        self.textCons.config(state=tk.DISABLED)

        while True:
            self.server.send(self.message.encode())
            self.textCons.config(state=tk.NORMAL)
            self.textCons.insert(tk.END, "You | " + self.message + "\n\n")
            self.textCons.config(state=tk.DISABLED)
            self.textCons.see(tk.END)
            break

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    fileName = self.server.recv(1024).decode()
                    fileLength = self.server.recv(1024).decode()
                    sender = self.server.recv(1024).decode()

                    if os.path.exists(fileName):
                        os.remove(fileName)

                    total = 0
                    with open(fileName, 'wb') as file:
                        while str(total) != fileLength:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, str(sender) + " | File " + fileName + " diterima\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)
                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, message + "\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)
            except:
                self.server.close()
                break


if __name__ == "__main__":
    gui = GUI()

