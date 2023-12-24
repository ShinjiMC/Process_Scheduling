CC = gcc
CFLAGS = -Wall -Wextra -std=c11
SRC_DIR = src
INC_DIR = Components
OUT_DIR = bin
EXEC = main

SRCS = $(wildcard $(SRC_DIR)/*.c)
INCS = $(wildcard $(INC_DIR)/*.h)
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(OUT_DIR)/%.o)

.PHONY: all clean

all: $(OUT_DIR)/$(EXEC)

$(OUT_DIR)/$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

$(OUT_DIR)/%.o: $(SRC_DIR)/%.c $(INCS) | $(OUT_DIR)
	$(CC) $(CFLAGS) -I$(INC_DIR) -c $< -o $@

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean:
	rm -rf $(OUT_DIR)
