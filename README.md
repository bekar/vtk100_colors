# vtk100-colors

Dealing with the color output in terminal which is classy, but what about when you try to get those in the tkinter, yes this what `vtk100-colors` is intends to do.

![screenshot][screenshot]
above test file in screenshot can be donwload from [here][extreme].

#### HOW-TO-RUN

```bash
$ ./main.py <any command with color output>
```

#### *tip: use the tee command to grab output

To display plain text only set SGR to { 0, false }

```bash
$ SGR=0 ./main.py <any command with color output>
```

Some example simple examples can be found in `make`:

```bash
$ make
make [hello|ls]
```

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
