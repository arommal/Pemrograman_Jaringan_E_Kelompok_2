import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os

class GUI:

    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350, bg="#30475E")

        self.pls = tk.Label(self.login, text="SILAHKAN LOGIN", justify=tk.CENTER, font="Montserrat 15 bold", fg="#dddddd", bg="#30475E")
        self.pls.place(relheight=0.15, relx=0.29, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username : ", font="Montserrat 12 bold", fg="#dddddd", bg="#30475E")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Montserrat 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Room Id : ", font="Montserrat 12 bold", fg="#dddddd", bg="#30475E")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Montserrat 11", show="*")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)

        self.go = tk.Button(self.login, text="Lanjutkan", font="Montserrat 12 bold", fg = "#dddddd", bg = "#F05454",
                            command = lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))

        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))

        self.login.destroy()
        self.tampilan()

        rcv = threading.Thread(target=self.terima)
        rcv.start()

    def tampilan(self):
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#222831")
        self.chatBoxHead = tk.Label(self.Window, bg = "#222831", fg = "#dddddd", text = self.name, font = "Montserrat 11 bold", pady = 5)

        self.chatBoxHead.place(relwidth = 1)

        self.line = tk.Label(self.Window, width = 450, bg = "#222831")

        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        self.textCons = tk.Text(self.Window, width=20, height=2, bg="#30475E", fg="#dddddd", font="Montserrat 11", padx=5, pady=5)

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(self.Window, bg="#dddddd", height=80)

        self.labelBottom.place(relwidth = 1, rely = 0.8)

        self.entryMsg = tk.Entry(self.labelBottom, bg = "#30475E", fg = "#dddddd", font = "Montserrat 11")
        self.entryMsg.place(relwidth = 0.65, relheight = 0.03, rely = 0.008, relx = 0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, text = "Kirim", font = "Montserrat 10 bold", width = 20, bg = "#F05454",
								command = lambda : self.tombolSend(self.entryMsg.get()))
        self.buttonMsg.place(relx = 0.67,
							rely = 0.008,
							relheight = 0.03,
							relwidth = 0.32)

        self.labelFile = tk.Label(self.Window, bg="#dddddd", height=70)

        self.labelFile.place(relwidth = 1,
							    rely = 0.9)

        self.fileLocation = tk.Label(self.labelFile, text = "Pilih File yang Akan Dikirim", bg = "#30475E", fg = "#EAECEE", font = "Montserrat 11")
        self.fileLocation.place(relwidth = 0.65, relheight = 0.03, rely = 0.008, relx = 0.011)

        self.browse = tk.Button(self.labelFile, text = "Browse", font = "Montserrat 10 bold", width = 13, bg = "#F05454", command = self.browse)

        self.browse.place(relx = 0.67, rely = 0.008, relheight = 0.03, relwidth = 0.15)

        self.sengFileBtn = tk.Button(self.labelFile, text = "Kirim File", font = "Montserrat 10 bold", width = 13, bg = "#F05454", command = self.kirimFile)
        self.sengFileBtn.place(relx = 0.84, rely = 0.008, relheight = 0.03, relwidth = 0.15)

        self.textCons.config(cursor = "arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight = 1,
						relx = 0.974)

        scrollbar.config(command = self.textCons.yview)
        self.textCons.config(state = tk.DISABLED)

    def browse(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                    title="Silahkan Pilih File",
                                    filetypes = (("Text files",
                                                "*.txt*"),
                                                ("all files",
                                                "*.*")))
        self.fileLocation.configure(text="File yang Akan Dikirim: "+ self.filename)

    def kirimFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(str("~~Menerima~~ " + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state = tk.NORMAL)
        self.textCons.insert(tk.END, "<Anda> "
                                     + str(os.path.basename(self.filename))
                                     + " ~~Terkirim~~\n\n")
        self.textCons.config(state = tk.DISABLED)
        self.textCons.see(tk.END)

    def tombolSend(self, msg):
        self.textCons.config(state = tk.DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, tk.END)
        snd= threading.Thread(target = self.kirimPesan)
        snd.start()

    def terima(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, "<" + str(send_user) + "> " + file_name + " D\n\n")
                    self.textCons.config(state = tk.DISABLED)
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END,
                                    message+"\n\n")

                    self.textCons.config(state = tk.DISABLED)
                    self.textCons.see(tk.END)

            except:
                print("Kesalahan Terjadi!")
                self.server.close()
                break

    def kirimPesan(self):
        self.textCons.config(state=tk.DISABLED)
        while True:
            self.server.send(self.msg.encode())
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END,
                            "<Anda> " + self.msg + "\n\n")

            self.textCons.config(state = tk.DISABLED)
            self.textCons.see(tk.END)
            break

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)