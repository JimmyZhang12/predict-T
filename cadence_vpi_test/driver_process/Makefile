PROG=driver_process

OBJS=main.o interprocess.o

CFLAGS=-Wall -std=c11 -D_XOPEN_SOURCE=500 -O0 -g -m32
LFLAGS=-lrt -lpthread -m32

.PHONY: clean

all:$(PROG)
	@echo $(OBJS)

$(PROG):$(OBJS)
	$(CC) $^ $(LFLAGS) -o $@

%.o:%.c
	$(CC) -c $< $(CFLAGS) -o $@

clean:
	rm -f *.o $(PROG)
