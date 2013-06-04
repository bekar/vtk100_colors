default:
	@echo "make [hello|ls|extreme(download required)]"

current: ls

hello:
	./tkvt100.py echo -e "\x1b[31;1;4mHello tkinter\x1b[0m\nThis is the output of \"\x1b[34;3mecho -e\x1b[0m\""

ls:
	./tkvt100.py ls --color=always

extreme:
	./tkvt100.py cat colorextreme
