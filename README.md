# vtk100-colors

Dealing with the color output in terminal which is classy, but what about when you try to get those in the tkinter, yes this what `vtk100-colors` is intends to do.

![screenshot][screenshot]

#### HOW-TO-RUN

```bash
$ ./vtk100.py <any command with color output>
```

To display plain text only set SGR to { 0, false }

```bash
$ SGR=0 ./vtk100.py <any command with color output>
```


If you have no idea what's suppose to be done run `make`:

```bash
$ make
make [hello|ls|extreme(download required)]
```

there are 3 samples you can play with. extreme has to be [downloaded][extreme] which has been shown in the screenshot:

#### Read more

 - [ANSI color][ansi]
 - [256 color chart][chart]
 - [Ecma-048][ecma]
 - [VT100][vt100]

[vt100]: http://en.wikipedia.org/wiki/VT100
[ecma]: http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-048.pdf
[screenshot]: https://raw.github.com/bekar/vtk100-colors/dump/images/screenshot.png
[extreme]: https://raw.github.com/bekar/vtk100-colors/dump/samples/colorextreme
[chart]: http://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
[ansi]: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
