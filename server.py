from socket import *
from threading import *
from tkinter import *
import tkinter.scrolledtext as scrolledtext


class Pencere(Tk): #Tkinter penceremizi oluştuyoruz

    def __init__(self):
        super().__init__()    
        self.title("TCP Server") #Penceremize isim veriyoruz
        self.geometry("400x500") #pencerenin boyutunu ayarlıyoruz 

        self.yazilar = scrolledtext.ScrolledText(self, width=44, undo=True , wrap=WORD)          #Mesajlarımızın ekranda gözükmesi ve yeni mesaj 
        self.yazilar['font'] = ('consolas', '12')                                                   #geldikçe aşağı kayması için tkinter kütüphanesinin
        self.yazilar.pack(expand=True, fill='both')  # ScrolledText elamanını kullanıyorum

app = Pencere()

class Server(Pencere):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 56789
        self.baglanti=(self.ip, self.port)  #bağlanti için gerekli ip ve portu atıyoruz
        self.serversocket = socket(AF_INET, SOCK_STREAM)  # AF_INET IPv4 adresine karşılık geliyor, SOCK_STREAM TCP socket e karşılık geliyor

        self.kullanicilar = []
        self.isimler = []        #Client ve isim bilgilerini tutacak listelerimizi oluşturuyoruz
    
    def t(self):
        return __import__("time").strftime('%X')+" "   #Saat bilgisini almak için Time kütüphanesini kullanıyorum

        
    
    def clientThread(self,client):
        bayrak = True
        while True:
            try:
                message = client.recv(1024).decode('utf8')      #Gelen mesajı türkçe harflerinde bulunduğu string bilgisine çeviriyoruz 

                if bayrak:
                    if message[0:15]=="Kullanıcı Adı: ":
                        message=message[15:]

                    if message[0:14]=="Kullanıcı Adı:":
                        message=message[14:]

                    index = self.kullanicilar.index(client)
                    degis=self.isimler[index]
                    self.isimler[index]=message #ilk mesaj ile kullanıcı adı bilgisini almamızı sağlıyor.

                    app.yazilar.insert(END,'\n'+self.t()+degis+" ismini "+message+' olarak değiştirdi.') # İsim bilgisini ekrana yazdırıyoruz               
                    bayrak = False #bayrak değerini false yaparak sadece ilk seferde kullanıcı adı almasını sağlıyoruz

        #Kullanıcıların mesajlarını diğer kullanıcılara ileten döngü     
                for kullanici in self.kullanicilar: 
                    if kullanici != client: 
                        index = self.kullanicilar.index(client)   
                        name = self.isimler[index]
                        kullanici.send((self.t()+name + ':' + message).encode('utf8'))         

        
        #Kullanıcı programı kapattığında çıktığını sunucu üzerinden gösteren fonksiyon          
            except:
                index = self.kullanicilar.index(client)
                self.kullanicilar.remove(client)
                name=self.isimler[index]
                self.isimler.remove(name)
                app.yazilar.insert(END,'\n'+self.t()+name+' çıkış yaptı.')            
                break
    


    def baslat(self): 
        self.serversocket.bind(self.baglanti)  #socket bağlantısını açıyoruz.
        self.serversocket.listen()    #socket bağlantısını dinliyoruz.
        app.yazilar.insert(END,self.t()+"Server Ip Adresi: {}".format(self.ip))          #Sunucunun Ip adresini ekrana yazdırıyoruz
        app.yazilar.insert(END,"\n"+self.t()+"Server dinlemede")          #Sunucunun dinlediğini ekrana yazdırıyoruz

        while True:       
            self.clientsocket, self.address = self.serversocket.accept()
            self.kullanicilar.append(self.clientsocket)
            name=__import__("os").getlogin()        
            self.isimler.append(name)        
            app.yazilar.insert(END,'\n'+self.t()+name+' Bağlandı.', self.address[0] + ':' + str(self.address[1]))
            thread = Thread(target=self.clientThread, args=(self.clientsocket, ))         #Thread kütüphanesini kullanarak fonksiyonun tek çekirdek yerine çoklu çekirdek kullanarak işlem yapmasını sağlıyoruz.
            thread.start()          #Thread işlemini başlatıyoruz

sunucu=Server() #sunucumuzu bağlıyoruz

thread=Thread(target=sunucu.baslat)          #Tkinter ile oluşturduğum                                
thread.daemon = True                         #arayüzün donmasını engellemek
thread.start()                               # için thread işlemini kullanıyorum

app.mainloop()  #Pencerenin açık kalmasını sağlıyoruz. 