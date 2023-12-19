import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

nickname = input("Enter your nickname here : ")

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address,port))

print("Connected with the server... This may take some time")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = Label(self.login,text="Login to access our app" , justify=CENTER , font="Georgia 18 bold")
        self.pls.place(relheight=0.15,relx=0.2,rely=0.07)

        self.labelName = Label(self.login , text = "Name : " , font="Georgia 14" )
        self.labelName.place(relheight=0.2 , relx=0.1 , rely=0.2 )

        self.entryName = Entry(self.login, font="Georgia 14")
        self.entryName.place(relwidth=0.4 , relheight=0.12 , relx=0.35 , rely=0.2 )

        self.go = Button(self.login,text="Continue",font="Helvetica 14 bold",
        command = lambda : self.goAhead(self.entryName.get()))

        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.name = name
        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self,name):
         self.layout(name)
         self.Window.deiconify()
         self.Window.title("CHATROOM")
         self.Window.resizable(width=False,height=False)
         self.Window.configure(width=470,height=550,bg="#17202A")

    def receive(self):
           while True:
                try:
                    message = client.recv(2048).decode('utf-8')
                    if message == 'NICKNAME':
                        client.send(self.name.encode('utf-8'))
                    else:
                        self.show_message(message)
                except:
                    print("An error occured!")
                    client.close()
                    break

    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= Thread(target = self.write)
        snd.start()

    def show_message(self, message):
             self.textCons.config(state = NORMAL)
             self.textCons.insert(END, message+"\n\n")
             self.textCons.config(state = DISABLED)
             self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)	
            break

g = GUI()
