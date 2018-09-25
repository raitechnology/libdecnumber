
CC       ?= gcc
AR       ?= ar
CFLAGS   ?= -ggdb -O2 -Wall -fPIC
INCLUDES ?= -I. -Ibid -Idpd

all: libdecnumber.a

clean:
	rm -f *.o *.a

libdecnumber.a: decNumber.o decContext.o decimal32.o decimal64.o decimal128.o \
                bid2dpd_dpd2bid.o host-ieee32.o host-ieee64.o host-ieee128.o
	$(AR) rc $@ $^

%.o: %.c
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) -c $< -o $@

%.o: bid/%.c
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) -c $< -o $@

