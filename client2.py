from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.constants import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") + "\n"
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def uploadImage(event=None):
    filename = filedialog.askopenfilename()
    img = Image.open(filename).resize((64, 64), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    msg_list.image_create(INSERT, padx=5, pady=5, image=photo)
    msg_list.images.append(photo)


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = ScrolledText(top, wrap=WORD, width=50, height=40)
msg_list.grid(row=2, column=4, padx=10, pady=10)
msg_list.images = []

# scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack(padx=10, pady=10)
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(padx=10, pady=10)
button = tkinter.Button(top, text='Open', command=uploadImage)
button.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.