CC = gcc
CFLAGS = -Wall -O2
TARGET = target_binary
OBJS = main.o utils.o database.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

main.o: main.c utils.h database.h
	$(CC) $(CFLAGS) -c main.c

utils.o: utils.c utils.h
	$(CC) $(CFLAGS) -c utils.c

database.o: database.c database.h
	$(CC) $(CFLAGS) -c database.c

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
