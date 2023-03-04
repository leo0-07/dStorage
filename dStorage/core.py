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
    
    def __init__(self,pindex,pdata):
        self.version="1.0rc1"
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

    def version(self):
        return self.version
    
    def show(self):
        print("informações:")
        self.dbinfo()
        for i in range(len(self.pdata)):
            print(self.pindex[i],": ", self.pdata[i])
    ''' displays the data contents and indexes, graph mode '''

    def set_database(self, value):
        if len(self.dpath) > 1:
            self.database = self.dpath  + value + ".db"

        else:
            print("file path not specified!")
    
    def display(self):
            window =Tk()
            window.configure(background='blue')
            window.title("Data wire visualization!")
            output = Text(window, background=self.dcolor)
            output.grid()
            window.okb = Button(window,text="Exit",command=window.destroy)
            window.okb.grid()
            stdout = output
            output.insert(END, str(" : "+ self.table + "/"),"\n")
            for i in range(len(self.pdata)):
                output.insert(END, str(self.pindex[i])+" : "+ str(self.pdata[i]))
                output.insert(END, "\n")

            window.mainloop()
            
    def cdBase(self):
        database = os.getenv("HOME") +"/"+  self.database + ".db"
        '''print (("db name: " + database),"\n")'''
        con = sqlite3.connect(self.database)
        c = con.cursor()        
        cstring="CREATE TABLE " + self.table
        tfields =""
        for i in range(len(self.pindex)):
            print(self.pindex[i])
            if i == 0:
                tfields +=  str(self.pindex[i]) + " integer "
                
            else:
                    tfields +=  str(self.pindex[i]) + " text "
                    
            if i < (len(self.pindex) -1):
                tfields +=", "
                
        cstring +="( "+tfields + " )"
        print("db creation string:"+ cstring + "\n")
        c.execute(cstring)
        '''print ("database created!")'''

    ''' reads the indexes from the data corner '''
    
    def l_pdindex(self):
        if self.debug == 1:
            self.dbinfo()
            
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
        if self.debug ==1 :
            print("savedata")
            self.dbinfo()

        dfields = ""
        print("arquivo",self.database)
        con = sqlite3.connect(self.database)
        c = con.cursor()
        cstring = "INSERT INTO "+ self.table + " VALUES("
        for i in range(len(self.pdata)):
            
            if i > 0:
                dfields += "'" + self.pdata[i] + "'"

            else:
                dfields += str(self.pdata[i])

            if i  < (len(self.pdata) -1):
                dfields +=", "
                
        cstring += dfields + " )"
        if self.debug == 1:
            print(cstring)
            
        c.execute(cstring)
        con.commit()
        con.close()
        self.updted = 1
 
    def loaddata(self,  reg):
        if self.debug ==1 :
            print("loaddata")
            self.dbinfo()
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
            self.set_database = os.getenv("HOME") +  dbname
            self.table = tbname

        else:
            self.database= self.dpath + "/" + dbname
            self.table = tbname
            
            self.set_database(dbname)
        if self.debug== 1:
            print (("database name: " + self.database),"\n")
        
    ''' list so members data filtered by id '''
    def litems(self):
        self.dbinfo()
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


    def dbinfo(self):
        if self.debug == 1:
            print("informações da base de dados")
            print("file path ",self.dpath)
            print("database ",self.database)
        print("data table ",self.table)
        



        
