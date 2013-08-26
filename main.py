#!/usr/bin/python3

import os
from tkinter import *

def_font=[ "DejaVuSansMono", 11, "normal" ]

pallet8 = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "magic", "default", # magic: enable 256 color
]

pallet16 = [
    "000000","800000","008000","808000","000080","800080","008080","c0c0c0",
    "808080","ff0000","00ff00","ffff00","0000ff","ff00ff","00ffff","ffffff",
]

xx = [ "00", "5f", "87", "af", "d7", "ff" ]

try:
    if os.environ['SGR'].lower() in [ "false", "0" ]: SGR=False
    else: SGR=True
except Exception as NoEnvVariableSet:
    SGR=True

class vt100tk():
    def __init__(self, txt_wig, string=None):
        self.txtwig=txt_wig
        self.txtwig.tag_config(1, font=def_font[:2] + ["bold"])
        self.txtwig.tag_config(3, font=def_font[:2] + ["italic"])
        self.txtwig.tag_config(4, underline=TRUE)
        self.txtwig.tag_config(9, overstrike=TRUE)
        for i in range(8): # pallet8
            self.txtwig.tag_config(i+30, foreground=pallet8[i])
            self.txtwig.tag_config(i+40, background=pallet8[i])
        # 256-colors
        for i in range(16):
            self.txtwig.tag_config("fg"+str(i), foreground="#"+pallet16[i])
            self.txtwig.tag_config("bg"+str(i), background="#"+pallet16[i])
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    rgb="#"+xx[i]+xx[j]+xx[k]
                    suffix=str(i*36+j*6+k+16)
                    self.txtwig.tag_config("fg"+suffix, foreground=rgb)
                    self.txtwig.tag_config("bg"+suffix, background=rgb)
        for i in range(24):
            value=hex(i*10+8); rgb="#"+value[2:]*3
            suffix=str(i+232)
            self.txtwig.tag_config("fg"+suffix, foreground=rgb)
            self.txtwig.tag_config("bg"+suffix, background=rgb)
        if string: self.parser(string)

    def tag_sgr(self, code, pre, cur):
        if not code: return
        tag=int(code)
        if tag == 0: return
        if   self.extend==53: tag="bg"+code; self.extend=0;
        elif self.extend==43: tag="fg"+code; self.extend=0;
        elif self.extend: self.extend+=tag; return; #2nd skip
        elif tag in [ 38, 48 ]: self.extend=tag; return;
        self.txtwig.tag_add(tag, pre, cur)

    def de_code(self, fp, pre, cur):
        self.extend=0; fbreak=fp
        while self.string[fp] != 'm':
            if self.string[fp]==";":
                self.tag_sgr(self.string[fbreak:fp], pre, cur);
                fbreak=fp+1
            fp+=1
        self.tag_sgr(self.string[fbreak:fp], pre, cur)

    def parser(self, string):
        self.txtwig.delete('1.0', END)
        cur=""; j=1; i=fp=cflag=code=0
        length=len(string)
        self.string=string
        while fp<length:
            if string[fp]=='\x1b':
                pre=cur; cur=str(j)+'.'+str(i)
                pcode=code; code=fp+2 # +2 shift escape sequence
                while string[fp]!="m": fp+=1
                fp+=1; cflag+=1
                if cflag==2 and SGR:
                    self.de_code(pcode, pre, cur)
                    cflag-=1;
            if string[fp]=='\n': j+=1; i=-1; #print()
            self.txtwig.insert(END, string[fp])
            fp+=1; i+=1

if __name__ == "__main__" :
    if len(sys.argv)<2:
        print("Argument(s) Missing", file=sys.stderr); exit(1);
    root=Tk()
    text=Text(root, font=def_font)
    from subprocess import check_output
    vtk=vt100tk(text, check_output(sys.argv[1:], universal_newlines=True))
    text.pack(expand=YES, fill=BOTH)
    root.bind('<Key-Escape>', quit)
    root.mainloop()
