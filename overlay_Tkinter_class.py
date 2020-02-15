from tkinter import *
import random
import time
from pynput.keyboard import Key, Controller
class GUI:
    def ShowWindow(self,PressLabel):
        #global keyboard 
        #keyboard.press('q')
        #keyboard.release('q')
        #Show Window display
        self.root.update()
        self.root.deiconify() #root.wm_attributes('-alpha',1)
        #Renew label content
        global Random_Label
        self.Random_Label=random.choice(Button_Array)
        self.PressLabel.configure(text=self.Random_Label)
        self.preTime=time.time()

    def StartNewTask(self):
        #Renew Label Content after a random time
            self.task_delay = random.randrange(10000,20000)
            self.PressLabel.after(self.task_delay, lambda: self.ShowWindow(self.PressLabel))
           
    def HideWindow(self):
        #Hide window
        self.root.withdraw() #root.wm_attributes('-alpha',0.1)
        #Clear Label Text Content
        self.PressLabel.configure(text="")
        

    def acheckPress(self,Random_Label):
        print("Random_Label")
        if self.Random_Label==">":
            self.useTime=time.time()-self.preTime
            print("A "+str(self.useTime))
            self.HideWindow()
            self.StartNewTask()
           
    def bcheckPress(self,Random_Label):
        print("Random_Label")
        if self.Random_Label=="v":
            self.useTime=time.time()-self.preTime
            print("B "+str(self.useTime))
            self.HideWindow() 
            self.StartNewTask()

    def xcheckPress(self,Random_Label):
        print("Random_Label")
        if self.Random_Label=="^":
            self.useTime=time.time()-self.preTime
            print("X "+str(self.useTime))
            self.HideWindow()
            self.StartNewTask()

    def ycheckPress(self,Random_Label):
        print("Random_Label")
        if self.Random_Label=="<":
            self.useTime=time.time()-self.preTime
            print("Y "+str(self.useTime))
            self.HideWindow()
            self.StartNewTask()

    def __init__(self, root): 
        self.root=root
        #constants
        global keyboard
        keyboard = Controller()

        global Button_Array
        Button_Array=[">","v","^","<"]
        

        #Initialise window setting
        self.root.title("Cognitive Cycling")
        #self.root.geometry("150x150+900+300") #"window width x window height + position right + position down"
        self.root.geometry("1000x300+0+0")
        self.root.configure(background='#BBB444')
        self.root.resizable(False, False) 

        #Initialise Frame in window
        self.frame = Frame(self.root, width=150, height=150, background='#BBB444')
        self.frame.pack(side="top")

        #Initialise Display Label in Frame
        global Random_Label
        self.Random_Label=random.choice(Button_Array)
        self.PressLabel=Label(self.frame,text=self.Random_Label,font=("Helvetica 40"),background='#BBB444')
        self.PressLabel.pack(side="top",padx=50,pady=50)

        #Initialize/bind Keypress
        self.root.bind("<a>", lambda event: self.acheckPress(self.Random_Label))
        self.root.bind("<b>", lambda event: self.bcheckPress(self.Random_Label))
        self.root.bind("<x>", lambda event: self.xcheckPress(self.Random_Label))
        self.root.bind("<y>", lambda event: self.ycheckPress(self.Random_Label))
        
        #Initialize for time cal
        self.useTtime=0
        self.preTime=time.time()

if __name__ == "__main__":
    #Start Main Window
    root = Tk()
    congnitive_gui=GUI(root)
    root.mainloop()