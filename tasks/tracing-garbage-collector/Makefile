all: libtgc.so

libtgc.so: tgc.c tgc.h
	$(CC) -shared -fPIC -o libtgc.so tgc.c

clean:
	rm -f libtgc.so