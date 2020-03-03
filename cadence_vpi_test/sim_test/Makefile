PROG=simbench

OBJS=simbench.o interprocess.o

CFLAGS=-Wall -std=c11 -D_XOPEN_SOURCE=500 -O0 -g -m32
LFLAGS=-L. -lrt -lpthread -m32

.PHONY: clean

all:$(PROG) interprocess.so
	@echo $(OBJS)

interprocess.so:interprocess.c
	$(CC) $< -O0 -g -std=c11 -D_XOPEN_SOURCE=500 -m32 -fPIC -shared -lpthread -o $@

$(PROG):$(OBJS)
	$(CC) $^ $(LFLAGS) -o $@

%.o:%.c
	$(CC) -c $< $(CFLAGS) -o $@

clean:
	rm -f *.o $(PROG) interprocess.so
