'''
#    Copyright (C) 2018, 2020–2021  Leonardo de Araújo Lima <leonardo@asl-sl.com.br>
#    Copyright (C) 1983, 1994–1995, 1997, 2005, 2007, 2015  Leonardo de Araújo Lima
#                                             <mailto:leonardo@asl-sl.com.br>
#                                               <xmpp:linux77@suchat.org>
#                               <https://linux77.asl-sl.com.br>
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  
    This program comes with ABSOLUTELY NO WARRANTY
    This is free software, and you are welcome to redistribute it '''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, sqlite3
from tkinter import *
from random import *
import array

class dStorage:
    
    def __init__(self,pdata, pindex):
        self.pdata = pdata
        self.pindex = pindex
        self.lbl = []
        self.ent = []
        self.dcolor="white"
        self.icolor="blue"
        self.dpath= ""
        self.database =""
        self.table=""
        self.regdata = []
        self.updted = 0
        self.debug = 1
    ''' displays the contents of data and indexes, text mode '''
    
    def show(self):
        print("informações:")
        for i in range(len(self.pdata)):
            print(self.pindex[i],": ", self.pdata[i])
    ''' displays the data contents and indexes, graph mode '''
    
    def display(self):
            window =Tk()
            window.configure(background='blue')
            window.title("Data wire visualization!")
            output = Text(window, background="white")
            output.grid()
            window.okb = Button(window,text="Exit",command=window.destroy)
            window.okb.grid()
            stdout = output
            output.insert(END, str(" : "+ self.table + "/"),"\n")
            for i in range(len(self.pdata)):
                output.insert(END, str(self.pindex[i])+" : "+ str(self.pdata[i]))
                output.insert(END, "\n")

            window.mainloop()
            
    ''' cria base de dados '''
    def cdBase(self):

            if len(self.dpath) > 1:
                self.database = os.getenv("HOME") +  self.database
                
            else:
                self.database = self.dpath  + "/" + self.database

            print("verificar ", self.database[-3:])

            if self.database[-3:] != ".db":
                self.database += ".db"

            if self.debug ==1:
                print("database creation: " + self.database)

            con = sqlite3.connect(self.database)
            if self.debug == 1:
                print ("database filepath: ", self.dpath)
                print("\ndatabase name", self.database ,"\n")

            print("database created!")
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

            cstring +="("+tfields + ")"
            if self.debug == 1:
                print("db table creation string: "+ cstring + "\n")
                print(cstring)

            if cstring == "CREATE TABLE ()":
                print("no data struct defined!")
                print("no tables defined!")
                return

            print(cstring)
            c.execute(cstring)

            if self.debug == 1:
                print ("database created!")

            ''' reads the indexes from the data corner '''
    def l_pdindex(self):
        if self.debug == 1:
            print("loading indexes...")
            print("banco de dados :" + self.database)
            print("\ntabela :" + self.table)
            
        con = sqlite3.connect(self.database)
        c = con.cursor()
        sql = "PRAGMA table_info("+ self.table +")"
        if self.debug == 1:
            print(sql)
            
        c.execute(sql)
        con.commit()
        tarr = []
        rstf = c.fetchall()
        for i in rstf:
            tarr.append(i[1])

        for item in tarr:
            self.pindex=tuple(tarr)
            
        con.close()

    ''' stores data '''
    def savecad(self):
        i=0
        self.regdata= []
        for item in self.ent:
            print(item.get())
            i+= 1
            self.regdata.append(item.get())
        self.pdata = self.regdata
        self.savedata()

    ''' saves the data from the current record to your table '''
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
        if self.debug == 1:
            print(cstring)
            
        c.execute(cstring)
        con.commit()
        self.updted = 1
        con.close()
    
    ''' performs the reading of the data members of the instance '''
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

    '''delete records'''
    def deletedata(self,  reg):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        cstring= str("DELETE FROM " + self.table + " WHERE id=:ireg")
        rst= c.execute(cstring, {"ireg":reg})
        con.commit()
        con.close()
    '''### ###'''
    ''' loads the data members of the instance '''
    def getid(self, name, value):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        searchstring= str("SELECT id FROM " + self.table + " WHERE "+ name + "='" +  value +"'")
        if self.debug == 1:
            print(searchstring)
        
        rst = c.execute(searchstring)
        return rst.fetchone()
        c.commit()
        con.close()

    ''' selects the database '''
    def setdb(self, dbname, tbname):
        if len(self.dpath) > 1:
            self.database = os.getenv("HOME") +"/"+  dbname
            self.table = tbname

        else:
            self.database= self.dpath + "/" + dbname
            self.table = tbname
            
        if self.database[-3:] != ".db":
            self.database += ".db"

        if self.debug== 1:
            print (("database name: " + self.database),"\n")
        
    ''' list so members data filtered by id '''
    def litems(self):
        
        con = sqlite3.connect(self.database)
        c = con.cursor()
        c.execute(("SELECT id FROM " + self.table))
        con.commit()
        result = c.fetchall()
        return result
        
    ''' reads the data indexes of the instance '''
    def lnames(self, i):
        con = sqlite3.connect(self.database)
        c = con.cursor()
        sqlstring = "SELECT "+ self.pindex[i] +" FROM " + self.table
        c.execute((sqlstring))
        con.commit()
        result = c.fetchall()
        return result
        con.close()
        
    ''' registers using graphical interface '''
    def cad(self):
        wnd = Tk()
        wnd.configure(background=self.icolor)
        self.lbl= []
        self.ent= []
        self.l_pdindex()
        i = 0
        if self.debug == 1:
            print(self.pindex)
        
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

    ''' registers in text mode '''
    def registrar(self):
        print ("cadastro de informações")
        listd = []
        for item in self.pindex:
            listd.append(input("entre com o valor para "+ item + ":"))

        self.pdata = tuple(listd)



        
