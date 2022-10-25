#pyinstaller --onefile -w  wp.py
from tkinter import *
from socket import *
from threading import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import time

class Pencere(Tk): #Tkinter penceremizi oluştuyoruz

    def __init__(self):
        super().__init__()    
        self.title("TCP Chat") #Penceremize isim veriyoruz
        self.geometry("430x550") #pencerenin boyutunu ayarlıyoruz

        self.msg_list = scrolledtext.ScrolledText(self, width=44, undo=True , wrap=WORD)   #mesajları ekranda göstericek tkinter elamanını oluşturuyoruz
        self.msg_list['font'] = ('consolas', '12')
        self.msg_list.pack(expand=True, fill='both')
        self.msg_list.grid(row=0, column=0, padx=10, pady=10)

        self.msg=Entry(self, width=50) #mesaj girdilerini yazacağımız entry değişkenini oluşturuyoruz
        self.msg.insert(0,"Kullanıcı Adı: ")
        self.msg.grid(row=1, column=0)
        self.msg.focus()
        self.msg.selection_range(0, END)


        
window=Pencere()

class Application(Pencere):

    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.ip = '127.0.0.1'
        self.port = 56789
        self.baglanti=(self.ip,self.port)

    def t(self):
        return time.strftime('%X')+" "   

    #Enter tuşuna bastığımızda mesajı göndermemizi sağlayan fonksiyon.
    def mesaj_gonder(self,event):
        clientMessage = window.msg.get()
        window.msg_list.insert(END, '\n'+self.t() + 'Sen: ' + clientMessage)
        window.msg_list.insert(END, '\n'+"--------------------------------------------")
        window.msg_list.yview(END)
        self.client.send(clientMessage.encode('utf8'))
        window.msg.delete(0, END)
        
    #Button a bastığımızda mesajı göndermemizi sağlayan fonksiyon.    
    def mesaj_gonder_btn(self): 
        clientMessage = window.msg.get()
        window.msg_list.insert(END, '\n'+self.t() + 'Sen: ' + clientMessage)
        window.msg_list.insert(END, '\n'+"--------------------------------------------")
        window.msg_list.yview(END)
        self.client.send(clientMessage.encode('utf8'))
        window.msg.delete(0, END)
    
    #Sunucu üzerinden gelen mesajları aldığımzı fonksiyon
    def mesaj_al(self):

        while True:
            try:

                serverMessage =  self.client.recv(1024).decode('utf8')
            except:
                messagebox.showerror(title="Bağlantı hatası",message="Sunucu ile bağlantı kesildi")
                window.close()
                break
            window.msg_list.insert(END, '\n' + serverMessage)
            window.msg_list.insert(END, '\n'+"--------------------------------------------")
            window.msg_list.yview(END)

    #button ve enter tuşunu aktif hale getirdiğimiz fonksiyon
    def mesaj(self):
        window.msg.bind('<Return>', self.mesaj_gonder)
        window.btn=Button(window,text="Gönder", width=20, command=self.mesaj_gonder_btn)
        window.btn.grid(row=2, column=0, padx=10, pady=10)
    
    

app=Application() #uygulamamızı başlatıyoruz
app.mesaj()


#thread işlemini kullanarak uygulamamızı açıyoruz.
try: 
    app.client.connect(app.baglanti)

    recvThread = Thread(target=app.mesaj_al)
    recvThread.daemon = True
    recvThread.start()
except:

    messagebox.showerror(title="Bağlantı hatası",message="Sunucu ile bağlantı kurulamadı")



window.mainloop()