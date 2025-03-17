# Variables
TARGET_NAME = executable
CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -Wshadow -Wformat=2 -Wfloat-equal -Wconversion -Wlogical-op -Wcast-align -Wstrict-aliasing=2 -Wpointer-arith -Wundef -Wcast-qual -Wstrict-overflow=5 -Wwrite-strings -Winline -Wredundant-decls -Wno-unused-parameter
CFLAGS_DEBUG = $(CFLAGS) -g
CFLAGS_RELEASE = $(CFLAGS) -DNDEBUG -O3 -finline-functions
CFLAGS_TEST = $(CFLAGS) -DNDEBUG -O3 -finline-functions

LIBS = -lm -lgsl -lgslcblas

SRCDIR = src
INCDIR = $(SRCDIR)/include
MODULEDIR = $(SRCDIR)/modules
DTNORMDIR = dtnorm/src
OBJDIR = obj
BINDIR = bin
TESTDIR = test

INCLUDES = -I$(DTNORMDIR) -I$(INCDIR)

SOURCES = $(wildcard $(MODULEDIR)/*.c) $(SRCDIR)/main.c $(wildcard $(DTNORMDIR)/*.c)

OBJDIR_DEBUG = $(OBJDIR)/debug
OBJDIR_RELEASE = $(OBJDIR)/release
OBJDIR_TEST = $(OBJDIR)/test

# Object files using base filenames (requires unique .c filenames)
OBJECTS_DEBUG = $(addprefix $(OBJDIR_DEBUG)/, $(notdir $(SOURCES:.c=.o)))
OBJECTS_RELEASE = $(addprefix $(OBJDIR_RELEASE)/, $(notdir $(SOURCES:.c=.o)))
OBJECTS_TEST = $(addprefix $(OBJDIR_TEST)/, $(notdir $(SOURCES:.c=.o)))

DEBUG_TARGET = $(BINDIR)/$(TARGET_NAME)_debug
RELEASE_TARGET = $(BINDIR)/$(TARGET_NAME)
TEST_TARGET = $(BINDIR)/$(TARGET_NAME)_test

# Tell make where to look for source files
vpath %.c $(MODULEDIR) $(SRCDIR) $(DTNORMDIR)

.PHONY: all debug release test clean

all: release

# Build targets
debug: $(DEBUG_TARGET)
	@echo "Running gdb..."
	@cp $(TESTDIR)/test.glo $(TESTDIR)/000.glo
	gdb --args $(DEBUG_TARGET)

release: $(RELEASE_TARGET)
	@echo "Built release target"

test: $(TEST_TARGET)
	@echo "Running test..."
	@rm -f $(TESTDIR)/0000*
	@cp $(TESTDIR)/test.glo $(TESTDIR)/0000.glo
	./$(TEST_TARGET) $(TESTDIR)/0000

	@if diff $(TESTDIR)/0000.csv $(TESTDIR)/test.csv > /dev/null 2>&1; then \
		echo -e "csv output is the same. \033[1;32mGood refactoring!\033[0m"; \
	else \
		echo -e "csv output \033[1;31mDIFFERENCES FOUND\033[0m"; \
		diff $(TESTDIR)/0000.csv $(TESTDIR)/test.csv || true; \
	fi

	@if diff $(TESTDIR)/0000.frq $(TESTDIR)/test.frq > /dev/null 2>&1; then \
		echo -e "frq output is the same. \033[1;32mGood refactoring!\033[0m"; \
	else \
		echo -e "frq output \033[1;31mDIFFERENCES FOUND\033[0m"; \
		diff $(TESTDIR)/0000.frq $(TESTDIR)/test.frq || true; \
	fi

# Linking rules
$(DEBUG_TARGET): $(OBJECTS_DEBUG)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_DEBUG) $^ $(LIBS) -o $@

$(RELEASE_TARGET): $(OBJECTS_RELEASE)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_RELEASE) $^ $(LIBS) -o $@

$(TEST_TARGET): $(OBJECTS_TEST)
	@mkdir -p $(BINDIR)
	$(CC) $(CFLAGS_TEST) $^ $(LIBS) -o $@

# Static pattern rules for compilation
$(OBJECTS_DEBUG): $(OBJDIR_DEBUG)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_DEBUG) $(INCLUDES) -c $< -o $@

$(OBJECTS_RELEASE): $(OBJDIR_RELEASE)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) -c $< -o $@

$(OBJECTS_TEST): $(OBJDIR_TEST)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

# Clean rule
clean:
	rm -rf $(OBJDIR) $(BINDIR) $(TESTDIR)/0000*
