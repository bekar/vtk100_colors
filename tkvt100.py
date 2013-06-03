#!/usr/bin/python3

from tkinter import *
from subprocess import check_output

default_font=[ "DejaVuSansMono", 11 ]

pallet16 = [
    "000000","800000","008000","808000","000080","800080","008080","c0c0c0",
    "808080","ff0000","00ff00","ffff00","0000ff","ff00ff","00ffff","ffffff",
]
pallet8 = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "magic",  # 8 enable 256 color
    "def",    # 9 default foreground color
]

xx = [ "00", "5f", "87", "af", "d7", "ff" ]

class vt100tk():
    def __init__(self, text):
        self.text=text
        self.text.tag_config(1, font=[ default_font[0], default_font[1], "bold"])
        self.text.tag_config(3, font=[ default_font[0], default_font[1], "italic"])
        self.text.tag_config(4, underline=TRUE)
        self.text.tag_config(9, overstrike=TRUE)
        # pallet8
        for i in range(8):
            self.text.tag_config(i+30, foreground=pallet8[i])
            self.text.tag_config(i+40, background=pallet8[i])
        # 256-colors
        for i in range(16):
            self.text.tag_config("fg"+str(i), foreground="#"+pallet16[i])
            self.text.tag_config("bg"+str(i), background="#"+pallet16[i])
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    rgb="#"+xx[i]+xx[j]+xx[k]
                    suffix=str(i*36+j*6+k+16)
                    self.text.tag_config("fg"+suffix, foreground=rgb)
                    self.text.tag_config("bg"+suffix, background=rgb)
        for i in range(24):
            value=hex(i*10+8)
            rgb="#"+value[2:]*3
            suffix=str(i+232)
            self.text.tag_config("fg"+suffix, foreground=rgb)
            self.text.tag_config("bg"+suffix, background=rgb)

    def de_code(self, fp, pre, cur):
        self.extend=0
        def tag_me(code):
            tag=c=int(code)
            if   self.extend==53: tag="bg"+code; self.extend=0;
            elif self.extend==43: tag="fg"+code; self.extend=0;
            elif self.extend: self.extend+=c; return; #2nd skip
            elif c in [ 38, 48 ]: self.extend=c; return;
            self.text.tag_add(tag, pre, cur)

        temp=fbreak=fp
        while 1:
            if string[fp]=="m": tag_me(string[fbreak:fp]); break;
            if string[fp]==";": tag_me(string[fbreak:fp]); fbreak=fp+1
            fp+=1
        return string[temp:fp];

    def parser(self, string):
        j=1
        cur=pre=pcode=code=""
        fp=i=cflag=0
        length=len(string) # what abut C style

        while fp<length:
            if string[fp]=='\x1b':
                pre=cur; cur=str(j)+'.'+str(i)
                pcode=code; code=fp+2 # +2 shift escape sequence
                while string[fp-1]!="m": fp+=1
                #print(end="|")
                cflag+=1
            if cflag==2:
                if string[pcode]!="0":
                     out=self.de_code(pcode, pre, cur)
                     #print(out, end="^")
                cflag-=1

            if string[fp]=='\n': j+=1; i=-1;
            self.text.insert(END, string[fp])
            #print(string[self.fp], end="")
            fp+=1; i+=1

if __name__ == "__main__" :
    if len(sys.argv)<2: print("Argument(s) Missing", file=sys.stderr); exit()
    string=check_output(sys.argv[1:], universal_newlines=True)
    root=Tk()
    text=Text(root, font=default_font)
    vtk=vt100tk(text)
    vtk.parser(string)
    text.pack(expand=YES, fill=BOTH)
    root.bind('<Key-Escape>', quit)
    root.mainloop()
