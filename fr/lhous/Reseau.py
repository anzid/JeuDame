# coding=utf-8
'''
Created on 21 mars 2015

@author: rachdi
'''
# coding: utf-8
from Tkinter import *
from ttk import *
from math import floor
import socket
import thread
import json
import time

class ChatClient(Frame):
  
    def __init__(self, fen1):   #constructeur 
        Frame.__init__(self, fen1)
        self.fen1 = fen1
        self.initUI(fen1)
        self.serverSoc = None
        self.serverStatus = 0
        self.clientStatus = 0
        self.buffsize = 1024
        self.allClients = {}
        self.counter = 0
        self.laMain = 0
        self.tic = 0
  
    def initUI(self,fen1):
        self.fen1.title("Jeu de dame en ligne")
        ScreenSizeX = self.fen1.winfo_screenwidth()
        ScreenSizeY = self.fen1.winfo_screenheight()
        self.FrameSizeX  = 900
        self.FrameSizeY  = 700
        FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
        FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
        self.fen1.geometry("%sx%s+%s+%s" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
        self.fen1.resizable(width=True, height=True)
    
        padX = 10
        padY = 10
        parentFrame = Frame(self.fen1)
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)
    
        ipGroup = Frame(parentFrame)
        serverLabel = Label(ipGroup, text="Set: ")
        self.nameVar = StringVar()
        self.nameVar.set("SDH")
        nameField = Entry(ipGroup, width=10, textvariable=self.nameVar)
        self.serverIPVar = StringVar()
        self.serverIPVar.set("127.0.0.1")
        serverIPField = Entry(ipGroup, width=15, textvariable=self.serverIPVar)
        self.serverPortVar = StringVar()
        self.serverPortVar.set("8090")
        serverPortField = Entry(ipGroup, width=5, textvariable=self.serverPortVar)
        serverSetButton = Button(ipGroup, text="Set", width=10, command=self.handleSetServer)
        addClientLabel = Label(ipGroup, text="Add friend: ")
        self.clientIPVar = StringVar()
        self.clientIPVar.set("127.0.0.1")
        clientIPField = Entry(ipGroup, width=15, textvariable=self.clientIPVar)
        self.clientPortVar = StringVar()
        self.clientPortVar.set("8091")
        clientPortField = Entry(ipGroup, width=5, textvariable=self.clientPortVar)
        clientSetButton = Button(ipGroup, text="Add", width=10, command=self.handleAddClient)
        Start = Button(ipGroup, text='Quitter', width=10, command = fen1.quit())
        serverLabel.grid(row=0, column=0)
        nameField.grid(row=0, column=1)
        serverIPField.grid(row=0, column=2)
        serverPortField.grid(row=0, column=3)
        serverSetButton.grid(row=0, column=4, padx=5)
        addClientLabel.grid(row=0, column=5)
        clientIPField.grid(row=0, column=6)
        clientPortField.grid(row=0, column=7)
        clientSetButton.grid(row=0, column=8, padx=5)
        Start.grid(row=0, column=9)
    
        readChatGroup = Frame(parentFrame)
        width =600
        height =600
        self.a =0
        self.b =0
        self.DETECTION_CLIC_SUR_OBJET=3
        self.pion  = [[0 for y in xrange(10)]   for x in xrange(10)]   # declaration de la liste des pions
        self.pion_adverse = [[0 for y in xrange(10)] for x in xrange(10)] # declaration de la liste des pions adverses
        self.liste = [] # la liste des cases ocupees
        self.liste_adverse = [] # la liste des caeses ocuppees par les pions adverses
        self.can = Canvas(readChatGroup, width =width, height =height, bg ='ivory')
        for x in xrange(0,10):
            for y in xrange(0,10):
                if (x+y)%2==1:
                    self.can.create_rectangle(x*width/10,y*width/10,(x+1)*width/10,(y+1)*width/10,fill='black')
                
                
        for y in xrange(0,4):
            for x in xrange(0,10):
                if (x+y)%2==1:
                    self.pion_adverse[x][y]=self.can.create_oval(5+x*60, 5+y*60, 55+x*60, 55+y*60, outline='black', fill='green')
                    self.liste_adverse.append([x,y])
                    print("la liste des cases adverses occupees est -> :",self.liste_adverse)
                
        for y in xrange(6,10):
            for x in xrange(0,10):
                if (x+y)%2==1:
                    self.pion[x][y]=self.can.create_oval(5+x*60, 5+y*60, 55+x*60, 55+y*60, outline='black', fill='maroon')
                    self.liste.append([x,y])
                    print("la liste des cases occupees est -> :",self.liste)
    
        self.can.bind('<Button-1>',self.Clic) # évévement clic gauche (press)
        self.can.focus_set()
        self.receivedChats = Text(readChatGroup, bg="white", width=20, height=30, state=DISABLED)
        #scrollbar = Scrollbar(self.receivedChats)
        #scrollbar.pack(side=RIGHT, fill=Y)
        #listbox = Listbox(self.receivedChats, yscrollcommand=scrollbar.set)
        #for i in range(1000):
            #listbox.insert(END, str(i))
        #listbox.pack(side=LEFT, fill=BOTH)
        #scrollbar.config(command=listbox.yview)

        self.friends = Listbox(readChatGroup, bg="white", width=20, height=30)
        self.receivedChats.grid(row=0, column=0, sticky=W+N+S, padx = (0,10))
        self.can.grid(row=0, column=1)
        self.friends.grid(row=0, column=2, sticky=E+N+S)

        writeChatGroup = Frame(parentFrame)
        self.chatVar = StringVar()
        self.chatField = Entry(writeChatGroup, width=20, textvariable=self.chatVar)
        sendChatButton = Button(writeChatGroup, text="Send", width=10, command=self.handleSendChat)
        self.chatField.grid(row=0, column=0, sticky=W)
        sendChatButton.grid(row=0, column=1, padx=5)

        self.statusLabel = Label(parentFrame)

        bottomLabel = Label(parentFrame, text="Created by Lhoussaine RACHDI")
    
        ipGroup.grid(row=0, column=0)
        readChatGroup.grid(row=1, column=0)
        writeChatGroup.grid(row=2, column=0, pady=10)
        self.statusLabel.grid(row=3, column=0)
        bottomLabel.grid(row=4, column=0, pady=10)
    
    def connexionSuccesed(self):
        if self.serverStatus == 1 and self.clientStatus == 1 :
            return TRUE
        else:
            return FALSE
    
    def handleSetServer(self):
        if self.serverSoc != None:
            self.serverSoc.close()
            self.serverSoc = None
            self.serverStatus = 0
        serveraddr = (self.serverIPVar.get().replace(' ',''), int(self.serverPortVar.get().replace(' ','')))
        try:
            self.serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSoc.bind(serveraddr)
            self.serverSoc.listen(5)
            self.setStatus("Server listening on %s:%s" % serveraddr)
            thread.start_new_thread(self.listenClients,())
            self.serverStatus = 1
            self.name = self.nameVar.get().replace(' ','')
            if self.name == '':
                self.name = "%s:%s" % serveraddr
        except:
            self.setStatus("Error setting up server")
    
    def listenClients(self):
        while 1:
            clientsoc, clientaddr = self.serverSoc.accept()
            self.setStatus("Client connected from %s:%s" % clientaddr)
            self.clientStatus = 1
            self.addClient(clientsoc, clientaddr)
            thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
        self.serverSoc.close()
  
    def handleAddClient(self):
        if self.serverStatus == 0:
            self.setStatus("Set server address first")
            return
        clientaddr = (self.clientIPVar.get().replace(' ',''), int(self.clientPortVar.get().replace(' ','')))
        try:
            clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsoc.connect(clientaddr)
            self.setStatus("Connected to client on %s:%s" % clientaddr)
            self.clientStatus = 1
            self.laMain = 1
            self.addClient(clientsoc, clientaddr)
            thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
        except:
            self.setStatus("Error connecting to client")

    def handleClientMessages(self, clientsoc, clientaddr):
        while 1:
            try:
                data = clientsoc.recv(self.buffsize)
                if not data:
                    break
                self.addChat("%s:%s" % clientaddr, data)
            except:
                break
        self.removeClient(clientsoc, clientaddr)
        clientsoc.close()
        self.setStatus("Client disconnected from %s:%s" % clientaddr)
  
    def handleSendChat(self):
        if self.serverStatus == 0:
            self.setStatus("Set server address first")
            return
        msg = self.chatVar.get().replace(' ','')
        if msg == '':
            return
        self.addChat("me", msg)
        for client in self.allClients.keys():
            client.send(msg)
  
    def addChat(self, client, msg):
        self.receivedChats.config(state=NORMAL)
        self.ReceiveCoup(msg)
        self.receivedChats.insert("end",client+": "+msg+"\n")
        self.receivedChats.config(state=DISABLED)
  
    def addClient(self, clientsoc, clientaddr):
        self.allClients[clientsoc]=self.counter
        self.counter += 1
        self.friends.insert(self.counter,"%s:%s" % clientaddr)
  
    def removeClient(self, clientsoc, clientaddr):
        print self.allClients
        self.friends.delete(self.allClients[clientsoc])
        del self.allClients[clientsoc]
        print "tata"and self.allClients
  
    def setStatus(self, msg):
        self.statusLabel.config(text=msg)
        print msg
    
    def Clic(self, event):
        """ Gestion de l'événement Clic gauche """
        # position du pointeur de la souris
        X = event.x
        Y = event.y
        changement = {}
        print("Position du clic -> ",X,Y)

        if self.DETECTION_CLIC_SUR_OBJET == True and self.laMain == 1:  # si on avait cliquer precedement sur un pion
            current_a = int (floor(X/60)) # la premiere coordonnee de la case a se deplacer
            current_b = int (floor(Y/60)) # la deuxieme coordinnee de la case a se deplacer

            if self.AutorisationCoup(self.a,self.b,current_a,current_b) == 0: # coup autoriser
                self.can.delete(self,self.pion[self.a][self.b])                   # on efface le pion 
                #creation d'un nouveau pion dans l'endroit souhaite
                self.pion[current_a][current_b] = self.can.create_oval(5+current_a*60, 5+current_b*60, 55+current_a*60, 55+current_b*60, outline='black', fill='maroon')
                self.liste.remove([self.a,self.b])                          # retirer la case precedente de la liste des cases occupees 
                self.liste.append([current_a,current_b])          # ajouter la nouvelle case dans la liste des cases occupees
                changement[json.dumps([self.a,self.b])] = 0
                changement[json.dumps([current_a,current_b])] = 1
                print "aaa"
                print changement
                self.EnvoyerCoup(changement)
            elif self.AutorisationCoup(self.a,self.b,current_a,current_b) == 1:
                self.setStatus("vous devez monger le pion adverse")
            elif self.AutorisationCoup(self.a,self.b,current_a,current_b) == 2:
                self.setStatus("ce carreau est deja rempli")
            elif self.AutorisationCoup(self.a,self.b,current_a,current_b) == 3:
                self.setStatus("il faut ce deplacer sur les carreaux fonces")
            elif self.AutorisationCoup(self.a,self.b,current_a,current_b) == 4:
                self.setStatus("deplacement non autosier")
            self.DETECTION_CLIC_SUR_OBJET = False  # pour l'attente d'une nouvelle clique sur un pion
                
        elif self.laMain == 1: # si on a pas cliquer precedemnt sur un pion
            # coordonnées de l'endroit du clique
            self.a=int (floor(X/60))
            self.b=int (floor(Y/60))
            print("CLIC SUR LA CARREAU -> ",self.a,self.b)
            for x in xrange(0,len(self.liste)):
                if [self.a,self.b]==self.liste[x]:
                    self.DETECTION_CLIC_SUR_OBJET = True
                    break
            print("DETECTION CLIC SUR OBJET -> ",self.DETECTION_CLIC_SUR_OBJET)   
        
        
    def AutorisationCoup(self, a,b,current_a,current_b):
        """getion de l'autorisation des coups"""
        resultat = 0 # coup autorisé
        for x in xrange(0,len(self.liste_adverse)):
            #if [current_a+1,current_b+1]==liste_adverse[x] or [current_a-1,current_b+1]==liste_adverse[x] or [current_a-1,current_b-1]==liste_adverse[x] or [current_a+1,current_b-1]==liste_adverse[x]:
                #resultat = 1 # manger obligatoirement
                #break
            for x in xrange(0,len(self.liste)):
                if [current_a,current_b]==self.liste[x] or [current_a,current_b]==self.liste_adverse[x]:
                    resultat = 2 # ce carreau est deja rempli
                    break

        if (current_a+current_b)%2==0:
            resultat = 3 # FAUT SE DEPLACER SUR LES CARREAUX FONCE
        if [a+1,b-1]!=[current_a,current_b] and [a-1,b-1] != [current_a,current_b]:
            resultat = 4 # deplacement non autoriser

        return resultat          
      
    def EnvoyerCoup(self, changement ):
        for client in self.allClients.keys():
            msg = json.dumps(changement) 
            print "ccc"
            print msg
            client.send(msg)
        self.laMain = 0
          
    def ReceiveCoup(self, msg):
        liste = json.loads(msg)
        print liste
        for cle in liste.keys():
            print cle
            if liste[cle] == 0:
                m = json.loads(cle)
                print type(m)
                self.can.delete(self, self.pion_adverse[9-m[0]][9-m[1]])
                self.liste_adverse.remove([9-m[0],9-m[1]])
            else:
                a = json.loads(cle)
                self.can.create_oval(5+(9-a[0])*60, 5+(9-a[1])*60, 55+(9-a[0])*60, 55+(9-a[1])*60, outline='black', fill='green')
                self.liste_adverse.append([9-a[0],9-a[1]])
        self.laMain = 1
            
        #for y in xrange(0,4):
            #for x in xrange(0,10):
                #if (x+y)%2==1:
                    #self.can.delete(self,self.pion_adverse[x][y])
        #del(self.liste_adverse[:])
        #for x in xrange(0,len(liste)):
            #a = liste[x]  
            #self.can.create_oval(5+(9-a[0])*60, 5+(9-a[1])*60, 55+(9-a[0])*60, 55+(9-a[1])*60, outline='black', fill='green')
            #self.liste_adverse.append(a)
            #self.laMain = 1
        
    #self.tic = time.time()
    #thread.start_new_thread(Timer, self.tic)
      
    #def Timer(tic):
        #while time.time() - tic < 10:
            #self.laMain = 1
        #self.EnvoyerCoup()