from tkinter import *
 
class MainWindow:
    def __init__(self, master):
        mainframe = Frame(master, width = 300, height = 200)
        button = Button(mainframe, text="Open Window",
                        command=self.openWindow)
        button.place(x = 100, y = 80)
        mainframe.pack()
     
    def openWindow(self):
        win = ExtraWindow()
 
class ExtraWindow:
    def __init__(self):
        top = Toplevel()
 
        subframe = Frame(top, width = 200, height = 150)
        button = Button(top, text="Destroy Window", command=top.destroy)
        button.place(x = 50, y = 50)
        subframe.pack()
 
root = Tk()
window = MainWindow(root)
root.mainloop()