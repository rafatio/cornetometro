from Tkinter import *

i = -1

def save(l, status):
    print l.cget("text") + "----------> " +  status

def previous(f, l):
    global i
    i -= 1
    getTweet(f, l)

def next(f, l):
    global i
    i += 1
    getTweet(f, l)

def getTweet(f, l):
    global i
    l.config(text="Tweet " + str(i) + ": " + f[i])

def main():
    file = open('data/macxche-dataset.txt','r')
    f = file.readlines()

    root = Tk()

    root.wm_title("CORNETOMETRO CLASSIFICATOR!!!")

    c = Canvas(root,width=800)
    c.pack(side = 'left',expand=1,fill=BOTH)

    c2 = Canvas(c,width=800)
    c2.pack(side = 'left',expand=1,fill=BOTH)

    c3 = Canvas(c,width=800)
    c3.pack(side = 'right',expand=1,fill=BOTH)

    l = Label(c2, text="", width=120)
    l.pack()

    b1 = Button(c3,text='Good',command=lambda:save(l, "good"))
    b1.pack(fill='x')

    b2 = Button(c3,text='Bad',command=lambda:save(l, "bad"))
    b2.pack(fill='x')

    b3 = Button(c3,text='Next',command=lambda:next(f,l))
    b3.pack(fill='x')

    b4 = Button(c3,text='Previous',command=lambda:previous(f,l))
    b4.pack(fill='x')

    root.mainloop()

if __name__ == '__main__':
    main()
