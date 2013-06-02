#!/usr/bin/python3

from tkinter import *
from subprocess import check_output

sys.path.append('../vt100-colors')
from colors import pallet, fstyle

default_font=[ "DejaVuSansMono", 11 ]

class vt100tk():
    def __init__(self, text):
        self.text=text
        self.text.tag_config(1, font=[ default_font[0], default_font[1], "bold"])
        self.text.tag_config(3, font=[ default_font[0], default_font[1], "italic"])
        self.text.tag_config(4, underline=TRUE)
        self.text.tag_config(9, overstrike=TRUE)
        for i in range(30,38): self.text.tag_config(i, foreground=pallet[i-30])
        for i in range(40,48): self.text.tag_config(i, background=pallet[i-40])

    def tag_me(self, code, pre, cur):
        c=int(code)
        #if c is [ 5,38,48 ]: return
        # if c>10 and c<30: return c
        # if c>48: return c
        self.text.tag_add(c, pre, cur)

    def de_code(self, fp, pre, cur):
        temp=fbreak=fp
        while 1: #for letter in string[fp:]:
            if string[fp]=="m": self.tag_me(string[fbreak:fp], pre, cur); break;
            if string[fp]==";": self.tag_me(string[fbreak:fp], pre, cur); fbreak=fp+1
            fp+=1
        return string[temp:fp];

    def parser(self, string):
        j=1
        cur=pre=pcode=code=""
        self.fp=0
        i=cflag=0
        length=len(string) # what abut C style

        while self.fp<length:
            if string[self.fp]=='\x1b':
                pre=cur; cur=str(j)+'.'+str(i)
                pcode=code; code=self.fp+2
                while string[self.fp-1]!="m": self.fp+=1
                print(end="|")
                cflag+=1

            if cflag==2:
                #print(string[pcode], end="")
                if string[pcode]!="0":
                     out=self.de_code(pcode, pre, cur)
                     print(out, end="^")
                cflag-=1

            if string[self.fp]=='\n': j+=1; i=-1;
            self.text.insert(END, string[self.fp])
            print(string[self.fp], end="")
            self.fp+=1; i+=1

if __name__ == "__main__" :
    root=Tk()
    text=Text(root, font=default_font)

    exec_path="../vt100-colors/colors.py"
    #string=check_output([tokenizer_path, ed_path], universal_newlines=True)
    string=check_output(exec_path, universal_newlines=True)
    vtk=vt100tk(text)
    vtk.parser(string)
    text.pack(expand=YES, fill=BOTH)
    root.bind('<Key-Escape>', quit)
    root.mainloop()
