MYSRCPATHS = /include
MYSRCS = include/crypto1.c include/crypto01.c include/bucketsort.c 
MYINCLUDES = -Iinclude

BINS = mfkey32v2.c
INSTALLTOOLS = $(BINS)

mfkey32v2:$(MYSRCS)

.PHONY: flipper-crack
flipper-crack: mfkey32v2
	python3 -c 'import serial' 2>/dev/null || python3 -m pip install pyserial
	python3 mfkey_extract.py --cli

