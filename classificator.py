from Tkinter import *
from tkFileDialog import askopenfilename
import os
import shutil
import re


class Classificator(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.tweet_counter = 0

        c = Canvas(self.parent,width=800)
        c.pack(side = 'left',expand=1,fill=BOTH)

        c2 = Canvas(c,width=800)
        c2.pack(side = 'left',expand=1,fill=BOTH)

        c3 = Canvas(c,width=800)
        c3.pack(side = 'right',expand=1,fill=BOTH)

        c4 = Canvas(c,width=800)
        c4.pack(side = 'right',expand=1,fill=BOTH)

        c5 = Canvas(c,width=800)
        c5.pack(side = 'right',expand=1,fill=BOTH)

        self.tweet_label = Label(c2, text="Nenhum tweet")
        self.tweet_label.pack()
        self.tweet_widget = Label(c2, text="Carregue algum arquivo", width=120, font=('Helvetica', 10, 'bold'))
        self.tweet_widget.pack()

        b3 = Button(c5,text='Next',command=lambda:self.next())
        b3.pack(fill='x')

        b5 = Button(c5,text='Previous',command=lambda:self.previous())
        b5.pack(fill='x')

        b1 = Button(c4,text='Good',command=lambda:self.classify("good"))
        b1.pack(fill='x')

        b2 = Button(c4,text='Bad',command=lambda:self.classify("bad"))
        b2.pack(fill='x')

        b6 = Button(c3,text='Load',command=lambda:self.openfile(c2))
        b6.pack(fill='x')

        b7 = Button(c3,text='Save',command=lambda:self.save_file())
        b7.pack(fill='x')

        b4 = Button(c3,text='Delete',command=lambda:self.delete(c2))
        b4.pack(fill='x')

        # Keyboard shortcuts
        parent.bind('g', lambda e: self.classify("good"))
        parent.bind('b', lambda e: self.classify("bad"))
        parent.bind('s', lambda e: self.save_file())
        parent.bind('<Left>', lambda e: self.previous())
        parent.bind('<Right>', lambda e: self.next())
        parent.bind('d', lambda e: self.delete(c2))

    def openfile(self,c2):

       file_path = askopenfilename(parent=self.parent)

       file_name = file_path.split("/")[-1:][0]

       self.classified_file_path = os.path.dirname(os.path.realpath(__file__)) + "/data_classified/" + file_name[:-4] + "-classified.txt"

       if not os.path.exists( self.classified_file_path):
           shutil.copy(file_path,  self.classified_file_path)

       file = open(self.classified_file_path,'r')

       self.f = []
       tweet = ''
       for line in file:
           tweet += line
           if line[:4] == '####':
               self.f.append(tweet)
               tweet = ''

       file.close()

       # Start in first unclassified tweet
       self.tweet_counter = 0
       while self.f[self.tweet_counter][:4] == '###!':
           self.tweet_counter += 1

       self.tweet_label.config(text ="Tweet " + str(self.tweet_counter) + ":")
       self.tweet_label.pack()
       self.tweet_widget.config(text=self.f[self.tweet_counter])
       self.tweet_widget.pack()

    def classify(self, status):
        if self.f[self.tweet_counter][:4] == '###!':
            self.f[self.tweet_counter] = re.sub(r'###![^#]*###', '###!' + status + '###' , self.f[self.tweet_counter])
        else:
            self.f[self.tweet_counter] = "###!" + status + "### "  + self.f[self.tweet_counter]
        self.next()

    def delete(self,c2):
        del self.f[self.tweet_counter]

        self.tweet_label.config(text ="Tweet " + str(self.tweet_counter) + ":")
        self.tweet_label.pack()
        self.tweet_widget.config(text=self.f[self.tweet_counter])
        self.tweet_widget.pack()

    def save_file(self):
        with open(self.classified_file_path, "w") as file:
            for line in self.f:
                file.write(line)

    def previous(self):
        if (self.tweet_counter > 0):
            self.tweet_counter -= 1
            self.getTweet("-")

    def next(self):
        if (self.tweet_counter < len(self.f)-1):
            self.tweet_counter += 1
            self.getTweet("+")

    def getTweet(self, direction):
        self.tweet_label.config(text ="Tweet " + str(self.tweet_counter) + ":")
        self.tweet_label.pack()
        self.tweet_widget.config(text=self.f[self.tweet_counter])
        self.tweet_widget.pack()

        ''' TO_DECIDE: MOSTRAR OU NAO OS TWEETS JA CLASSIFICADOS
        if not self.f[self.tweet_counter].startswith("###!###"):
            self.tweet_widget.config(text="Tweet " + str(self.tweet_counter) + ": " + self.f[self.tweet_counter])
        else:
            if direction == "+":
                self.next()
            else:
                self.previous()
        '''

def main():

    root = Tk()

    classi = Classificator(root)

    root.mainloop()

if __name__ == '__main__':
    main()
