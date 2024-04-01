import tkinter
import tkinter.messagebox
import customtkinter
import socket
import threading
from security import *
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from tkinter import *
from tkinter import ttk


class app:
    def __init__(self, master):

        self.master = master
        self.master.geometry("1200x600")
        self.HOST = 'messagerie-python.ydns.eu'
        self.PORT = 9090

        self.login()
    
    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.home = customtkinter.CTkFrame(self.master, width=300, height=250)
        self.home.grid_columnconfigure(index=0, weight=5)
        self.home.grid_rowconfigure(index=0, weight=5)
        #self.home.configure()
        self.home.pack(pady=150)
        self.home.pack_propagate(0)
        self.login_ = customtkinter.CTkEntry(self.home, placeholder_text="Login")
        self.login_.pack(pady=10)

        self.password_ = customtkinter.CTkEntry(self.home, placeholder_text="Password", show="*")
        self.password_.pack()

        self.home_alerte = customtkinter.CTkEntry(self.home, width=250, border_width=0, state="disabled",fg_color="transparent")
        self.home_alerte.pack(pady= 5)

        self.connect_btn = customtkinter.CTkButton(self.home, text='Connect',font=('Bold', 12), width=250, command=self.connection)
        self.connect_btn.pack(pady=10)

        self.create_btn = customtkinter.CTkButton(self.home, text='Create account',font=('Bold', 12), fg_color='black',width=250, command=self.register)
        self.create_btn.pack(pady=5)

        self.master.bind('<Return>', self.connection_button) 

    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.home_account = customtkinter.CTkFrame(self.master, width=300, height=250)
        self.home_account .grid_columnconfigure(index=0, weight=5)
        self.home_account .grid_rowconfigure(index=0, weight=5)
        #self.home.configure()
        self.home_account .pack(pady=150)
        self.home_account .pack_propagate(0)
        self.login_user = customtkinter.CTkEntry(self.home_account, placeholder_text="Login")
        self.login_user.pack(pady=10)

        self.password_1 = customtkinter.CTkEntry(self.home_account, placeholder_text="Password", show="*")
        self.password_1.pack()

        self.password_2 = customtkinter.CTkEntry(self.home_account, placeholder_text="Password", show="*")
        self.password_2.pack(pady=2)

        self.acct_alerte = customtkinter.CTkEntry(self.home_account, width=250, border_width=0, state="disabled",fg_color="transparent")
        self.acct_alerte.pack(pady= 5)


        self.create_btn = customtkinter.CTkButton(self.home_account, text='Create account',font=('Bold', 12), fg_color='black',width=250, command=self.create_account)
        self.create_btn.pack(pady=5)

        self.connect_btn = customtkinter.CTkButton(self.home_account, text='Back to the login page',font=('Bold', 12), width=250, command=self.login)
        self.connect_btn.pack(pady=10)

        self.master.bind('<Return>', self.create_account)

    def create_account_button(self,event):
        self.create_account()

    def create_account(self):
        self.acct_alerte.configure(state=tkinter.NORMAL)
        self.acct_alerte.delete(0, END) 
        self.acct_alerte.configure(state=tkinter.DISABLED)
        self.loginuser = self.login_user.get().strip()
        self.password1 = self.password_1.get().strip()
    
        
        self.password2 = self.password_2.get().strip()
        
        print(self.loginuser, f"{self.password1}")
        if self.loginuser == "" or self.password1 == "" or self.password2 == "":
            self.acct_alerte.configure(state=tkinter.NORMAL)
            self.acct_alerte.insert(tkinter.INSERT,"Password or user empty !")
            self.acct_alerte.configure(state=tkinter.DISABLED)
            self.password_1.delete(0, END) 
            self.password_2.delete(0, END)
        elif self.password1 != self.password2:
            self.acct_alerte.configure(state=tkinter.NORMAL)
            self.acct_alerte.insert(tkinter.INSERT,"Passwords are different ! ")
            self.acct_alerte.configure(state=tkinter.DISABLED) 
            self.password_1.delete(0, END) 
            self.password_2.delete(0, END)

        else:
            self.password1 = hash_password(self.password1)
            self.password2 = hash_password(self.password2)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))

            self.sock.send(self.loginuser.encode('utf-8'))
            null = (self.sock.recv(1024)).decode('utf-8')
            self.sock.send(self.password1.encode('utf-8'))
            cnn = (self.sock.recv(1024)).decode('utf-8')
      
            if cnn == "nop":
                key = create_key(self.loginuser)
              
                self.sock.send(key.encode('utf-8'))
                self.account_success()
            else:
                self.acct_alerte.configure(state=tkinter.NORMAL)
                self.acct_alerte.insert(tkinter.INSERT,"The user name exists already")
                self.acct_alerte.configure(state=tkinter.DISABLED)
                self.sock.close()

    def account_success(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.home_success = customtkinter.CTkFrame(self.master, width=500, height=250)
        self.home_success.grid_columnconfigure(index=0, weight=5)
        self.home_success.grid_rowconfigure(index=0, weight=5)
        #self.home.configure()
        
        self.home_success.pack(pady=150)
        self.home_success.pack_propagate(0)
        self.success = customtkinter.CTkLabel(self.home_success, text=f"Welcome !\nYour account has been successfully created.\nClick below to login.",font=('Bold', 20))
        self.success.pack(pady=10)
        self.connect_btn = customtkinter.CTkButton(self.home_success, text='Back to the login page',font=('Bold', 12), width=250, command=self.login)
        self.connect_btn.pack(pady=10)

    def connection_button(self,event):
        self.connection()

    def connection(self):
        self.home_alerte.configure(state=tkinter.NORMAL)
        self.home_alerte.delete(0,tkinter.END)
        self.home_alerte.configure(state=tkinter.DISABLED)
        self.password = self.password_.get()
        self.user = self.login_.get()
        self.password = self.password.strip()
        self.password = hash_password(self.password)
        self.user = self.user.strip()
    
        if self.user == "" or self.password == "":
            self.home_alerte.configure(state=tkinter.NORMAL)
            self.home_alerte.insert(tkinter.INSERT,"Password or user empty !")
            self.home_alerte.configure(state=tkinter.DISABLED)
        
        else:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))

            self.sock.send(self.user.encode('utf-8'))
            null = (self.sock.recv(1024)).decode('utf-8')
            self.sock.send(self.password.encode('utf-8'))
            cnn = (self.sock.recv(1024)).decode('utf-8')
            
            if cnn == "Accepted":
                self.page_messages(self.user)
            else:
                self.home_alerte.configure(state=tkinter.NORMAL)
                self.home_alerte.insert(tkinter.INSERT,"Password or user incorrect !")
                self.home_alerte.configure(state=tkinter.DISABLED)
                self.sock.close()


    def page_messages(self, user):
        self.sock.send(" ".encode('utf-8'))
        self.contacts_recv= (self.sock.recv(1024)).decode('utf-8')
        self.contacts = self.contacts_recv.split()
        self.contacts.remove(self.user)
 

        for i in self.master.winfo_children():
            i.destroy()
        self.home_messages = customtkinter.CTkFrame(self.master,width=140)
        #self.home_messages.grid(row=0, column=3)
        self.home_messages.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.home_messages.grid_rowconfigure(4, weight=1)

        #self.home_messages.pack()
        #self.home_messages.pack_propagate(0)
        self.contact = customtkinter.CTkLabel(self.home_messages, text='Contact')
        self.contact.grid(row=0, column=0, padx = 10, sticky="nsew")
        #self.contact.pack()
        self.contact_lb = Listbox(self.home_messages, selectforeground='Black', activestyle='none', selectbackground= '#FFFFFF')
        self.listbox_scrollbar = tkinter.Scrollbar(self.home_messages, orient="vertical", command=self.contact_lb.yview)
        self.contact_lb.configure(yscrollcommand=self.listbox_scrollbar.set,  width= 30, bg = '#000081', fg = '#FFFFFF',font=('Bold', 13), bd = 0,  borderwidth=0, highlightthickness=0)
        #self.listbox_scrollbar.pack(fill='both')
        self.listbox_scrollbar.grid(row=1, column=1, sticky=customtkinter.NW+customtkinter.S)

        for i in self.contacts:
            self.contact_lb.insert(END, i)
        self.contact_lb.bind("<<ListboxSelect>>", self.onSelect)
        self.contact_lb.grid(row=1, column=0, padx =10)

        self.messages_display = customtkinter.CTkFrame(self.master,width=140)
        #self.home_messages.grid(row=0, column=3)
        self.messages_display.grid(row=2, column=5, rowspan=4, sticky="nsew")
        self.messages_display.grid_rowconfigure(4, weight=1)
        self.message_print =customtkinter.CTkTextbox(self.messages_display, width=800, height=400)
        self.message_print.grid(row=0, column=0, padx = 20, pady= 10)
        self.message_print.configure(state=tkinter.DISABLED)

        self.messages_entry= customtkinter.CTkFrame(self.master,width=140)
        self.messages_entry.grid(row=6, column=5, rowspan=4, sticky="nsew")
        self.messages_entry.grid_rowconfigure(0, weight=6)
     
        self.message_input =customtkinter.CTkTextbox(self.messages_entry, width=500, height=100)
        self.message_input.grid(row=2, column=0, padx = 20, pady= 15, sticky="nsew")
        self.message_input.insert("0.0","Ecrire un message...")
        self.message_input.configure(state=tkinter.DISABLED)
        self.message_input.bind("<Button-1>", self.on_click)
    
        self.button_1 = customtkinter.CTkButton(self.messages_entry, text="Envoyer", command=self.send)
        self.button_1.grid(row=2, column=5)

        self.gui_done = False
        self.running = True
        
        receive_thread = threading.Thread(target=self.receive, args=(self.user,))
        receive_thread.start()


    def onSelect(self, val):
        sender = val.widget
        idk = sender.curselection()
        self.value = sender.get(idk)
        conversation = f"new-conv-{self.user}_{self.value}"
        
        self.sock.send(conversation.encode('utf-8'))


    def send(self):
        self.message = self.message_input.get("0.0",'end-1c')
     
        if self.message != "" and self.message != "Ecrire un message...":
           
            message_to_send = encrypt(self.message,self.user,self.value)
            message_to_send[0] = str(message_to_send[0])
            messenge_to_send = " ".join(message_to_send)
          

            message_ = f"{self.user}: {self.message}"
            self.sock.send(messenge_to_send.encode('utf-8'))
            self.message_input.delete('1.0', 'end')



    def on_click(self,event):
        self.message_input.configure(state=tkinter.NORMAL)
        self.message_input.delete("0.0",tkinter.END)


    def receive(self, user):
        user = self.user
        while self.running:
            try:
                message_ = (self.sock.recv(1024)).decode('utf-8')
                if message_ == "new_conversation":                  
                    self.message_print.configure(state=tkinter.NORMAL)
                    self.message_print.delete('1.0', 'end')
                    self.message_print.configure(state=tkinter.DISABLED)
                else:
                    self.print_new_messages(message_,user)
            except ConnectionAbortedError:
                break
            
    
    
    def print_new_messages(self,message,user):
        message = self.mise_en_forme(message,user)
        for elem in message:
            self.message_print.configure(state=tkinter.NORMAL)
            self.message_print.insert(tkinter.INSERT,elem)
            self.message_print.configure(state=tkinter.DISABLED)


    def mise_en_forme(self,msg,user_):
        tab = []
        while msg != "":
            pos = msg.index(':')
            nb = int(msg[:pos])
            message_provisoire = msg[len(msg[:pos+1]):nb+4]
            date_heure = float(message_provisoire[:message_provisoire.index(':')])
            message_provisoire = message_provisoire[len(str(date_heure))+1:]
            user = message_provisoire[:message_provisoire.index(":")]
            message = message_provisoire[message_provisoire.index(":")+1:]
            message =  decrypt(message,user_)
            tab.append(f"{timestamp_to_readable(date_heure)}\n{user}: {message}\n\n")
            msg = msg[nb+4:]
        return tab




 
root = customtkinter.CTk()
app(root)
root.mainloop()