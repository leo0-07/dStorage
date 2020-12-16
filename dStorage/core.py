#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, sqlite3
from tkinter import *
from random import *
import array
# classe abstrata poliórfica para abstração de dados usando SQLite.

class dStorage:
    
    
    def __init__(self,pdata, pindex):
        self.pdata = pdata
        self.pindex = pindex
        self.lbl = []
        self.ent = []
        self.database = ""
        self.table = ""
        self.regdata = []
        self.updted = 0
# função de exibição dos dados texto...

    def show(self):
        print("informações:")
        for i in range(len(self.pdata)):
            print(self.pindex[i],": ", self.pdata[i])
#função de exibição dos dados gui....

    def display(self):
            window =Tk()
            window.configure(background='blue')
            window.title("Visualização de aramazenamento de dados!")
            output = Text(window, background="white")
            output.grid()
            window.okb = Button(window,text="Sair",command=window.destroy)
            window.okb.grid()
            stdout = output
            output.insert(END, str(" : "+ self.table + "/"),"\n")
            for i in range(len(self.pdata)):
                output.insert(END, str(self.pindex[i])+" : "+ str(self.pdata[i]))
                output.insert(END, "\n")

            window.mainloop()
# função de criação da base de sados SQLite...

    def cdBase(self):
        database = os.getenv("HOME") +"/"+  self.database + ".db"
        '''print (("db name: " + database),"\n")'''
        con = sqlite3.connect(self.database)
        c = con.cursor()        
        cstring="CREATE TABLE " + self.table
        tfields =""
        for i in range(len(self.pindex)):
            if i == 0:
                tfields +=  self.pindex[i] + " integer "
                
            else:
                    tfields +=  self.pindex[i] + " text "
                    
            if i < (len(self.pindex) -1):
                tfields +=", "
                
        cstring +="( "+tfields + " )"
        print("db creation string:"+ cstring + "\n")
        c.execute(cstring)
        '''print ("database created!")'''

    def l_pdindex(self):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        sql = "PRAGMA table_info("+ self.table +")"
        c.execute(sql)
        con.commit()
        tarr = []
        rstf = c.fetchall()
        for i in rstf:
            tarr.append(i[1])

        for item in tarr:
            self.pindex=tuple(tarr)
            
        con.close()

# função para armazenar os dados membros na base dados...

    def savecad(self):
        i=0
        self.regdata= []
        for item in self.ent:
            print(item.get())
            i+= 1
            self.regdata.append(item.get())
        self.pdata = self.regdata
        self.savedata()

# funao de inserção de dados em base de dados SQLite...

    def savedata(self):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        dfields = ""
        cstring = "INSERT INTO "+ self.table + " VALUES("
        for i in range(len(self.pdata)):
            
            if i > 0:
                dfields += "'" + self.pdata[i] + "'"

            else:
                dfields += str(self.pdata[i])

            if i  < (len(self.pdata) -1):
                dfields +=", " 
        cstring += dfields + ")"
        print(cstring)                        
        c.execute(cstring)
        con.commit()
        self.updted = 1
        con.close()
    

# funao de carga de dados da base SQLite em objeto membro....
    def loaddata(self,  reg):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        cstring= str("SELECT * FROM " + self.table + " WHERE id=:ireg")
        rst= c.execute(cstring, {"ireg":reg})
        con.commit()
        i=0
        tarr = []
        for row in c.fetchone():
            tarr.append(row)
            self.pdata=tuple(tarr)
            i += 1
        con.close()

#função de recarga de id de ddos membro....
        
    def getid(self, name):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        searchstring= str("SELECT * FROM " + self.table + " WHERE nome=:iname")
        rst= c.execute(searchstring, {"iname":name})
        con.commit()
        return rst.fetchone()
        con.close()

# função de seleção de base de dados...

    def setdb(self, dbname, tbname):
        self.database = os.getenv("HOME") +"/"+  dbname + ".db"
        self.table = tbname
        '''print ("db name: " + database)'''
        
# função de listagem de dados membro por id...

    def litems(self):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        c.execute(("SELECT id FROM " + self.table))
        con.commit()
        result = c.fetchall()
        return result
        
        
# função de listagem de nomes/chaves dos dados membro....
    def lnames(self, i):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        sqlstring = "SELECT "+ self.pindex[i] +" FROM " + self.table
        c.execute((sqlstring))
        con.commit()
        result = c.fetchall()
        return result
        con.close()
# função de cadastro de dados membro gui....

    def cad(self):
        wnd = Tk()
        wnd.configure(background="blue")
        self.lbl= []
        self.ent= []
        i = 0
        for item in self.pindex:
            self.lbl.append(Label(wnd,text=item))
            self.lbl[i].grid(row=i,column=0)
            self.ent.append(Entry(wnd,background="white"))
            self.ent[i].grid(row=i,column=1)
            i += 1
            
        btnupd = Button(wnd,text="salvar", command = self.savecad)
        btnupd.grid(row=(i+1),column=0)
        btnexit = Button(wnd, text="Sair", command=wnd.destroy)
        btnexit.grid(row=(i+2),column=1)
        wnd.mainloop()
        return self.updted

# função de entrada de dados membro texto....

    def registrar(self):
        print ("cadastro de informações")
        listd = []
        for item in self.pindex:
            listd.append(input("entre com o valor para "+ item + ":"))

        self.pdata = tuple(listd)



        
