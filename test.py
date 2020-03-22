start_test = [1,1]
from tkinter import *
from tkinter.ttk import *


chosen_alg = 1
def setup():
    window = Tk()
    var=IntVar()
    window.title("Finder Setup")

    window.geometry('250x200')

    lbl = Label(window, text="Set start point coordinates in range 0-49:")
    lbl.place(x=0,y=15)

    lbl2 = Label(window, text="Start point:")
    lbl2.place(x=0,y=40)

    lbl2x = Label(window, text="x:")
    lbl2x.place(x=80,y=40)
    lbl2y = Label(window, text="y:")
    lbl2y.place(x=130,y=40)

    x_ = Entry(window,width=3)
    x_.place(x=91,y=40)

    y_ = Entry(window,width=3)
    y_.place(x=141,y=40)


    lbl = Label(window, text="Choose algorithm:")
    lbl.place(x=0,y=70)

    def get_alg():
        global chosen_alg
        chosen_alg = var.get()

    rad1 = Radiobutton(window,text='A* algorithm', variable = var,value=1,command = get_alg)
    rad1.place(x=0,y=90)
    rad2 = Radiobutton(window,text="Dijkstra's algorithm", variable = var,value=2,command = get_alg)
    rad2.place(x=0,y=110)

    global chosen_alg
    chosen_alg = get_alg()

    def clicked():
        global start_test
        start_test[0]= int(x_.get())
        start_test[1] = int(y_.get())
        window.destroy()

    btn = Button(window, text="START",command = clicked)
    btn.place(x=150,y=145)

    window.mainloop()

setup()
print(chosen_alg)
print(type(chosen_alg))