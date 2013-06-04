#!/usr/bin/python3

from tkinter import *
from subprocess import check_output

def_font=[ "DejaVuSansMono", 11 ]

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
        self.text.tag_config(1, font=[ def_font[0], def_font[1], "bold"])
        self.text.tag_config(3, font=[ def_font[0], def_font[1], "italic"])
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
            if code=="" : code="1" # no code condition ^[[m
            tag=c=int(code)
            if   self.extend==53: tag="bg"+code; self.extend=0;
            elif self.extend==43: tag="fg"+code; self.extend=0;
            elif self.extend: self.extend+=c; return; #2nd skip
            elif c in [ 38, 48 ]: self.extend=c; return;
            self.text.tag_add(tag, pre, cur)

        temp=fbreak=fp
        while 1:
            if self.string[fp]=="m": tag_me(self.string[fbreak:fp]); break;
            if self.string[fp]==";": tag_me(self.string[fbreak:fp]); fbreak=fp+1
            fp+=1
        return self.string[temp:fp];

    def parser(self, string):
        cur=pre=pcode=code=""
        j=1; i=fp=cflag=0
        length=len(string) # what abut C style
        self.string=string
        while fp<length:
            if string[fp] in '\x1b':
                pre=cur; cur=str(j)+'.'+str(i)
                pcode=code; code=fp+2 # +2 shift escape sequence
                while string[fp]!="m": fp+=1
                #print(end="|")
                fp+=1; cflag+=1
                continue
            if cflag==2:
                if string[pcode:pcode+2] is [ "0m", "m" ] : pass
                else: out=self.de_code(pcode, pre, cur)
                cflag-=1
            if string[fp]=='\n': j+=1; i=-1;
            self.text.insert(END, string[fp])
            #print(string[fp], end="")
            fp+=1; i+=1

if __name__ == "__main__" :
    if len(sys.argv)<2:
        print("Argument(s) Missing", file=sys.stderr); exit(1);
    string=check_output(sys.argv[1:], universal_newlines=True)
    root=Tk()
    text=Text(root, font=def_font)
    vtk=vt100tk(text)
    vtk.parser(string)
    text.pack(expand=YES, fill=BOTH)
    root.bind('<Key-Escape>', quit)
    root.mainloop()
