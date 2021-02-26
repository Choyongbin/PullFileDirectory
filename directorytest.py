# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:59:29 2021

@author: 82102
"""

import os
from tkinter import filedialog
import shutil
import natsort
import tkinter as tk
import sqlite3
import hashlib

class abcd():
    def __init__(self, key= None):
       self.root = tk.Tk()
       self.root.title("File 정리")
       self.root.resizable(False,False)
       self.strvar = ""
       self.current =""
       self.new = ""
       self.textb = tk.Entry(self.root,width=20,textvariable=self.strvar,show="*")
       
       #self.textBox = tk.Text(self.root, height=10)
       self.button1 = tk.Button(self.root,
                               text="Insert",
                               command=self.inputPwd)
       self.currentPwd = tk.Entry(self.root,width=20,textvariable=self.current,show="*")
       self.newPwd = tk.Entry(self.root,width=20,textvariable=self.new,show="*")
       self.button2 = tk.Button(self.root,
                               text="ChangePassword",
                               command=self.ChangePassword)
       self.txt1 = tk.Label(self.root, text ="Password : ")
       self.txt2 = tk.Label(self.root, text ="현재비밀번호 : ")
       self.txt3 = tk.Label(self.root, text ="변경후비밀번호 : ")
       
       
       self.txt1.grid(row = 0, column = 0)
       self.textb.grid(row = 0, column = 1)
       self.textb.focus()
       self.button1.grid(row = 0, column = 2)
       self.txt2.grid(row = 1, column = 0)
       self.txt3.grid(row = 2, column = 0)
       self.currentPwd.grid(row = 1, column = 1)
       self.newPwd.grid(row = 2, column = 1)
       self.button2.grid(row = 3, column = 1)
       
       if self.textb.focus:
           self.textb.bind('<Return>', self.inputPwd)
       if self.newPwd.focus or self.currentPwd.focus:
           self.newPwd.bind('<Return>', self.ChangePassword)
           self.currentPwd.bind('<Return>',self.ChangePassword)
           
       self.conn = sqlite3.connect("test.db", isolation_level=None)

       self.c= self.conn.cursor()

       self.c.execute("CREATE TABLE IF NOT EXISTS table1 \
                       (id integer PRIMARY KEY, password text)")
     
       self.root.mainloop()
        
    def inputPwd(self,event):
       self.strvar =self.textb.get().strip()
       self.c.execute("SELECT * FROM table1 WHERE id=:Id",{"Id":1})
       a = list(self.c.fetchone())
       b = hashlib.sha256(self.strvar.encode()).hexdigest()
       if b == a[1]:
           self.conn.close()
           self.root.destroy()
           app=Test()
       else:
           self.textb.delete(0,100)
           tk.messagebox.showinfo("Error", "비밀번호 확인")
           print("Password Error")
       
    def ChangePassword(self,event):
        self.current = self.currentPwd.get().strip()
        self.new = self.newPwd.get().strip()
        self.c.execute("SELECT * FROM table1 WHERE id=:Id",{"Id":1})
        a = list(self.c.fetchone())
        b = hashlib.sha256(self.current.encode()).hexdigest()
        if b==a[1]:
            self.c.execute("UPDATE table1 SET password=? WHERE id=?", 
                      (hashlib.sha256(self.new.encode()).hexdigest(), 1))
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)
            tk.messagebox.showinfo("Complete", "비밀번호 변경완료")
        elif self.current == self.new:
            tk.messagebox.showinfo("Error","비밀번호 동일")
            print("Same Password Please insert different Password")
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)
        else :
            tk.messagebox.showinfo("Error","비밀번호 확인")
            print("Password Error")
            self.currentPwd.delete(0,100)
            self.newPwd.delete(0,100)
            

class Test():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File 정리")
        self.root.geometry("500x100+200+200")
        self.root.resizable(True,True)
        
        self.txt = tk.Label(self.root, text = " ")
        self.button1 = tk.Button(self.root,
                                text="폴더 선택",
                                command=self.opendirectory)
        
        self.button2 = tk.Button(self.root,
                                 text = "실행",
                                 command=self.makeup)
        self.dir_list =[]
        self.fil_list =[]
        self.CheckVariety = tk.IntVar() 
        self.r1 = tk.Checkbutton(self.root,text = "하위폴더명 추가",
                                 variable=self.CheckVariety)
        
        self.button1.pack()
        self.button2.pack()
        self.r1.pack()
        self.txt.pack()
        self.root.mainloop()
        
        #pdf 열기
    def opendirectory(self):  
        
        self.root.directory = filedialog.askdirectory(
            initialdir='dir',
            title='select directory')
            
        self.txt.configure(text=self.root.directory)
        
    def makeup(self):
        
        self.dir_list.clear()
        self.fil_list.clear()
        
        #하위폴더명 추가
        if self.CheckVariety.get() == 1:
            self.enum_file_only(self.root.directory)
            self.enum_folder_only(self.root.directory)
            fil_list_name =[]
            dir_list_name =[]
            
            for item in self.fil_list:
                fil_list_name.append(item.replace(self.root.directory,"").replace("\\","").replace("/",""))
            
            for item in self.dir_list:
                dir_list_name.append(item.replace(self.root.directory,"").replace("\\","").replace("/",""))
            
            self.newdir = self.root.directory + "[정리]"
            try:
                os.makedirs(self.newdir, exist_ok=False)
            except:
                shutil.rmtree(self.newdir)
                os.makedirs(self.newdir)
            
            
            numbering = int(1)
            numbering2 = int(0)
            
            sortedlist = natsort.natsorted(os.listdir(self.root.directory))
            for filename in sortedlist:
                
                file_path = os.path.join(self.root.directory,filename)
                
                if not os.path.isdir(file_path):
                    print("%s" % (file_path))
                    shutil.copy2("%s" % (file_path), self.newdir)
                    os.rename("%s/%s" % (self.newdir, filename), 
                              self.newdir+'/['+str(format(numbering2, self.format_num(self.fil_list)))+
                              "]_["+str(format(numbering, self.format_num(self.fil_list)))+']_'+filename)
                    numbering += 1
                          
            
            for i, item in enumerate(self.dir_list):
                numbering2 += 1
                numbering = 1
                numlen = int(0)
                for (path, dir, files) in os.walk(item):
                    numlen += len(files)
                    
                for (path, dir, files) in os.walk(item):                        
                    files = natsort.natsorted(files)
                    for filename in files:
                        print("%s/%s" % (path, filename))
                        shutil.copy2("%s/%s" % (path, filename), self.newdir)
                        os.rename("%s/%s" % (self.newdir, filename), 
                                  self.newdir+'/['+str(format(numbering2, self.format_num2(len(self.dir_list) + len(self.fil_list))))+   
                                  "]_"+str(dir_list_name[i])+
                                  " ["+str(format(numbering, self.format_num2(numlen)))+']_'+filename)
                        numbering += 1
            
            
        #모든 파일 복사
        else:
            self.newdir = self.root.directory + "[정리]"
            try:
                os.makedirs(self.newdir, exist_ok=False)
            except:
                shutil.rmtree(self.newdir)
                os.makedirs(self.newdir)
            
            self.copy_file(self.root.directory)
            
    def format_num(self, files):
        output = '06'
        if len(files) < 10:
            output = '02'
        elif len(files) < 100:
            output = '03'
        elif len(files) >= 100 and len(files) < 1000:
            output = '04'
        elif len(files) >= 1000 and len(files) < 10000:
            output = '05'
        return output
        
    def format_num2(self, num):
        output = '06'
        if num < 10:
            output = '02'
        elif num < 100:
            output = '03'
        elif num >= 100 and num < 1000:
            output = '04'
        elif num >= 1000 and num < 10000:
            output = '05'
        return output
        
        
    def enum_folder_only(self, dirname):
        for filename in os.listdir(dirname):
            file_path = os.path.join(dirname,filename)
            if os.path.isdir(file_path):
                self.dir_list.append(file_path)
                
    def enum_file_only(self, dirname):
        for filename in os.listdir(dirname):
            file_path = os.path.join(dirname,filename)
            
            if not os.path.isdir(file_path):
                self.fil_list.append(file_path)
                
        
    def copy_file(self, dirname):
        numbering = int(1)
        numlen = int(0)
        for (path, dir, files) in os.walk(dirname):
            numlen += len(files)
        
        for (path, dir, files) in os.walk(dirname):
                
            files = natsort.natsorted(files)
            
            for filename in files:
                print("%s/%s" % (path, filename))
                shutil.copy2("%s/%s" % (path, filename), self.newdir)
                os.rename("%s/%s" % (self.newdir, filename), 
                          self.newdir+'/['+
                          str(format(numbering, self.format_num2(numlen)))+']_'+filename)
                numbering += 1
    
app = abcd()