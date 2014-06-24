#!/usr/bin/env python3

import os, sys
import tkinter as tk

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
    if os.environ['SGR'].lower() in [ "false", "0" ]: SGR = False
    else: SGR = True
except Exception as NoEnvVariableSet:
    SGR = True

class vt100tk():
    def __init__(self, text_wig, string=None):
        self.txtwig = text_wig
        self.i = 0; self.j = 1
        if string:
            self.load_tags()
            self.parser(string)

    def load_tags(self):
        _font = self.txtwig['font'].split()
        self.txtwig.tag_config('1', font=_font[:2] + ["bold"])
        self.txtwig.tag_config('3', font=_font[:2] + ["italic"])
        self.txtwig.tag_config('4', underline=1)
        self.txtwig.tag_config('9', overstrike=1)
        for i in range(8): # pallet8
            self.txtwig.tag_config(str(i+30), foreground=pallet8[i])
            self.txtwig.tag_config(str(i+40), background=pallet8[i])
        for i in range(16): # 0-15/256-colors
            self.txtwig.tag_config(str(i)+"fg", foreground="#"+pallet16[i])
            self.txtwig.tag_config(str(i)+"bg", background="#"+pallet16[i])
        for i in range(6): # 16-231/256-colors
            for j in range(6):
                for k in range(6):
                    suffix = str(i*36+j*6+k+16); rgb = "#"+xx[i]+xx[j]+xx[k]
                    self.txtwig.tag_config(suffix+"fg", foreground=rgb)
                    self.txtwig.tag_config(suffix+"bg", background=rgb)
        for i in range(24): # 232-255/256-colors
            suffix = str(i+232); rgb = "#"+hex(i*10+8)[2:]*3
            self.txtwig.tag_config(suffix+"fg", foreground=rgb)
            self.txtwig.tag_config(suffix+"bg", background=rgb)

    def tag_sgr(self, code):
        if code in [ "", "0" ]: return None
        if   self.ext == "485": code += "bg"; self.ext = ""
        elif self.ext == "385": code += "fg"; self.ext = ""
        elif self.ext: self.ext += code; return; #2nd skip
        elif code in [ "38", "48" ]: self.ext = code; return;
        self.txtwig.tag_add(code, self.pre, self.cur)
        return code

    def de_code(self, fp):
        self.ext = ""; fbreak = fp
        while self.string[fp] != 'm':
            if self.string[fp] == ";":
                self.tag_sgr(self.string[fbreak:fp])
                fbreak = fp + 1
            fp += 1
        self.tag_sgr(self.string[fbreak:fp])

    def parser(self, string):
        self.cur = ""
        fp = cflag = code = 0
        length = len(string)
        self.string = string
        while fp < length:
            if string[fp]=='\x1b':
                self.pre = self.cur
                self.cur = str(self.j) + '.' +str(self.i) #self.txtwig.index(tk.CURRENT)
                pcode = code + 2; code = fp # +2 shift escape sequence
                while string[fp] != "m": fp += 1
                fp += 1; cflag += 1
                if cflag == 2 and SGR:
                    self.de_code(pcode); cflag -= 1;
                continue
            if string[fp] == '\n': self.j += 1; self.i = -1
            self.txtwig.insert("end", string[fp])
            fp += 1; self.i += 1

if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print("Argument(s) Missing", file=sys.stderr); exit(1);
    from subprocess import check_output
    text = tk.Text(font=[ "DejaVuSansMono", 11, "normal" ])
    text.pack(expand=1, fill="both")
    vt100tk(text, check_output(sys.argv[1:], universal_newlines=True))
    text.master.bind("<Key-Escape>", lambda event: quit())
    tk.mainloop()
