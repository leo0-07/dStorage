#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, sqlite3
from tkinter import *
from random import *
import array
'''classe abstrata poliórfica para abstração de dados usando SQLite.'''
''' construtora da classe '''
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
    ''' exibe os conteúdos de dados e índices, modo texto '''
    
    def show(self):
        print("informações:")
        for i in range(len(self.pdata)):
            print(self.pindex[i],": ", self.pdata[i])
    ''' exibe os conteúdos de dados e índices, modo gráfico '''
    
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
            
    ''' cria base de dados '''
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
        
    ''' lê os índices a partir do canco de dados '''
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

    ''' armazena dados de registro '''
    def savecad(self):
        i=0
        self.regdata= []
        for item in self.ent:
            print(item.get())
            i+= 1
            self.regdata.append(item.get())
        self.pdata = self.regdata
        self.savedata()

    ''' salva os dados do registro atual em sua tabela '''
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
    
    ''' realiza a leitura dos dados membros da instância '''
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

    ''' carrega os os dados membros da instância '''
    def getid(self, name):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        searchstring= str("SELECT * FROM " + self.table + " WHERE nome=:iname")
        rst= c.execute(searchstring, {"iname":name})
        con.commit()
        return rst.fetchone()
        con.close()

    ''' seleciona a base de dados '''
    def setdb(self, dbname, tbname):
        self.database = os.getenv("HOME") +"/"+  dbname + ".db"
        self.table = tbname
        '''print ("db name: " + database)'''
        
    ''' lista so dados membros filtrados por id '''
    def litems(self):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        c.execute(("SELECT id FROM " + self.table))
        con.commit()
        result = c.fetchall()
        return result
        
    ''' faz a leitura dos índices de dados da instância '''
    def lnames(self, i):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        sqlstring = "SELECT "+ self.pindex[i] +" FROM " + self.table
        c.execute((sqlstring))
        con.commit()
        result = c.fetchall()
        return result
        con.close()
        
    ''' realiza o cadastro usando interface gráfica '''
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

    ''' realiza o cadastro em modo texto '''
    def registrar(self):
        print ("cadastro de informações")
        listd = []
        for item in self.pindex:
            listd.append(input("entre com o valor para "+ item + ":"))

        self.pdata = tuple(listd)



        
