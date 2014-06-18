#!/usr/bin/env python3

import os, sys
import tkinter

pallet8 = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "magic", "default", # magic: enable 256 color
]

pallet16 = [
    "000000","800000","008000","808000","000080","800080","008080","c0c0c0",
    "808080","ff0000","00ff00","ffff00","0000ff","ff00ff","00ffff","ffffff",
]

xx = [ "00", "5f", "87", "af", "d7", "ff" ]

SGR = True
try:
    if os.environ['SGR'].lower() in [ "false", "0" ]:
        SGR = False
except Exception as NoEnvVariableSet:
    pass

class vt100tk():
    def __init__(self, text_wig, string=None):
        self.txtwig = text_wig
        _font = self.txtwig['font'].split()
        self.txtwig.tag_config(1, font=_font[:2] + ["bold"])
        self.txtwig.tag_config(3, font=_font[:2] + ["italic"])
        self.txtwig.tag_config(4, underline=1)
        self.txtwig.tag_config(9, overstrike=1)
        for i in range(8): # pallet8
            self.txtwig.tag_config(i+30, foreground=pallet8[i])
            self.txtwig.tag_config(i+40, background=pallet8[i])
        for i in range(16): # 0-15/256-colors
            self.txtwig.tag_config("fg"+str(i), foreground="#"+pallet16[i])
            self.txtwig.tag_config("bg"+str(i), background="#"+pallet16[i])
        for i in range(6): # 16-231/256-colors
            for j in range(6):
                for k in range(6):
                    rgb = "#"+xx[i]+xx[j]+xx[k]
                    suffix = str(i*36+j*6+k+16)
                    self.txtwig.tag_config("fg"+suffix, foreground=rgb)
                    self.txtwig.tag_config("bg"+suffix, background=rgb)
        for i in range(24): # 232-255/256-colors
            value = hex(i*10+8); rgb = "#"+value[2:]*3
            suffix = str(i+232)
            self.txtwig.tag_config("fg"+suffix, foreground=rgb)
            self.txtwig.tag_config("bg"+suffix, background=rgb)
        if string: self.parser(string)

    def tag_sgr(self, code):
        if not code: return None
        tag = int(code);
        if tag == 0: return None
        if   self.ext == 53: tag = "bg" + code; self.ext = 0; # 38+5+code
        elif self.ext == 43: tag = "fg" + code; self.ext = 0; # 48+5+code
        elif self.ext: self.ext += tag; return; #2nd skip
        elif tag in [ 38, 48 ]: self.ext = tag; return;
        self.txtwig.tag_add(tag, self.pre, self.cur)
        return tag

    def de_code(self, fp):
        self.ext = 0; fbreak = fp
        while self.string[fp] != 'm':
            if self.string[fp] == ";":
                self.tag_sgr(self.string[fbreak:fp])
                fbreak = fp + 1
            fp += 1
        return self.tag_sgr(self.string[fbreak:fp])

    def parser(self, string):
        self.cur = "";
        fp = cflag = code = 0
        length = len(string)
        self.string = string
        while fp < length:
            if string[fp]=='\x1b':
                self.pre = self.cur
                self.cur = self.txtwig.index(tkinter.CURRENT)
                pcode = code + 2; code = fp # +2 shift escape sequence
                while string[fp] !="m": fp += 1
                fp += 1; cflag += 1
                if cflag == 2 and SGR:
                    self.de_code(pcode); cflag-=1;
                continue
            self.txtwig.insert("end", string[fp])
            fp += 1;

if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print("Argument(s) Missing", file=sys.stderr); exit(1);

    from subprocess import check_output
    text = tkinter.Text(font=[ "DejaVuSansMono", 11, "normal" ])
    text.pack(expand=1, fill="both")
    vt100tk(text, check_output(sys.argv[1:], universal_newlines=True))
    text.master.bind("<Key-Escape>", lambda event: quit())
    tkinter.mainloop()
