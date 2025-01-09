# Variables
TARGET_NAME = $(shell basename $(shell pwd))
CC = gcc
CFLAGS = -Wall
CFLAGS_DEBUG = $(CFLAGS) -g
CFLAGS_RELEASE = $(CFLAGS) -DNDEBUG -O3 -finline-functions
CFLAGS_TEST = $(CFLAGS) -DNDEBUG -O3 -finline-functions

LIBS = -lm -lgsl -lgslcblas

SRCDIR = src
DTNORMDIR = dtnorm/src
OBJDIR = obj
BINDIR = bin
TESTDIR = test

INCLUDES = -I$(SRCDIR) -I$(DTNORMDIR)

SOURCES = $(wildcard $(SRCDIR)/*.c) $(wildcard $(DTNORMDIR)/*.c)

OBJDIR_DEBUG = $(OBJDIR)/debug
OBJDIR_RELEASE = $(OBJDIR)/release
OBJDIR_TEST = $(OBJDIR)/test

OBJECTS_DEBUG = $(patsubst $(SRCDIR)/%.c, $(OBJDIR_DEBUG)/%.o, $(SOURCES))
OBJECTS_RELEASE = $(patsubst $(SRCDIR)/%.c, $(OBJDIR_RELEASE)/%.o, $(SOURCES))
OBJECTS_TEST = $(patsubst $(SRCDIR)/%.c, $(OBJDIR_TEST)/%.o, $(SOURCES))

DEBUG_TARGET = $(BINDIR)/$(TARGET_NAME)_debug
RELEASE_TARGET = $(BINDIR)/$(TARGET_NAME)
TEST_TARGET = $(BINDIR)/$(TARGET_NAME)_test

.PHONY: all debug release test clean

all: release

# Build rules
debug: $(DEBUG_TARGET)
	@echo "Running gdb..."
	gdb --args $(DEBUG_TARGET)

release: $(RELEASE_TARGET)
	@echo "Built release target"

test: $(TEST_TARGET)
	@echo "Running test..."
	@cp $(TESTDIR)/test.glo $(TESTDIR)/000.glo
	@mv $(TESTDIR)/000.csv $(TESTDIR)/old_000.csv
	@rm -f $(TESTDIR)/000.frq $(TESTDIR)/000*.ics
	./$(TEST_TARGET) $(TESTDIR)/000
	@if diff $(TESTDIR)/000.csv $(TESTDIR)/old_000.csv > /dev/null; then \
                echo "Output remains the same. Good refactoring!"; \
        else \
                echo "Differences found in CSV files:"; \
                diff $(TESTDIR)/000.csv $(TESTDIR)/old_000.csv || true; \
        fi

# Link rules
$(DEBUG_TARGET): $(OBJECTS_DEBUG)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_DEBUG) $(INCLUDES) $^ $(LIBS) -o $@

$(RELEASE_TARGET): $(OBJECTS_RELEASE)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) $^ $(LIBS) -o $@

$(TEST_TARGET): $(OBJECTS_TEST)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) $^ $(LIBS) -o $@

# Compilation rules
$(OBJDIR_DEBUG)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_DEBUG) $(INCLUDES) -c $< -o $@

$(OBJDIR_RELEASE)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) -c $< -o $@

$(OBJDIR_TEST)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

$(OBJDIR_DEBUG)/%.o: $(DTNORMDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_DEBUG) $(INCLUDES) -c $< -o $@

$(OBJDIR_RELEASE)/%.o: $(DTNORMDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) -c $< -o $@

$(OBJDIR_TEST)/%.o: $(DTNORMDIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

# Clean rule
clean:
	rm -rf $(OBJDIR) $(BINDIR)
