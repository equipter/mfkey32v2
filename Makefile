MYSRCPATHS = /include
MYSRCS = include/crypto1.c include/crypto01.c include/bucketsort.c 
MYINCLUDES = -Iinclude

BINS = mfkey32v2.c
INSTALLTOOLS = $(BINS)

LDFLAGS = -Wl,-z,max-page-size=16384

mfkey32v2:$(MYSRCS)
