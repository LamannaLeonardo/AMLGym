DEBUGFLAG = -DDEBUG

CC = gcc

# MATHLIB = /opt/SUNWspro/SC2.0.1/libm.a
# MATHLIB = /usr/lib/libm.a
MATHLIB = -lm

CFLAGS = -O3
# CFLAGS = -W -g # -pg # $(DEBUGFLAG)

OPTOBS = optimal.o gn1lib.o utils.o mshs.o

PROGOBS = bbwstates.o us.o gn1.o gn2.o $(OPTOBS)

all: bbwstates

bbwstates: $(PROGOBS)
	$(CC) $(CFLAGS) $(PROGOBS) -o bbwstates $(MATHLIB)

us: us.o
	$(CC) $(CFLAGS) us.o

gn1: gn1.o
	$(CC) $(CFLAGS) gn1.o

gn2: gn2.o
	$(CC) $(CFLAGS) gn2.o

optimal: $(OPTOBS)
	$(CC) $(CFLAGS) $(OPTOBS)

install: all
ifneq ($(BIN),)
	mv bbwstates $(BIN)
else
	@echo Sub-makefile: No BIN dir defined here, see directory above.
endif

clean:
	/bin/rm -f *.o core bbwstates


bbwstates.o: bbwstates.h us.h gn1.h
us.o: us.h definitions.h
gn1.o: gn1.h definitions.h
gn2.o: gn2.h definitions.h
