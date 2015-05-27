'''
Created on 22 mai 2015

@author: rachdi
'''
from Tkinter import *
from ttk import *
from Reseau  import *
from Timer import *




def main():  
    fen1 = Tk()
    app = ChatClient(fen1)  
    fen1.mainloop()
 
  
      
  
  
      

if __name__ == '__main__':
    main()   