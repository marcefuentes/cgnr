TARGET_NAME = cgnr

CC = gcc
CFLAGS_RELEASE = -DNDEBUG -O3 -finline-functions -Wall
CFLAGS_TEST = -g -Wall

LIBS = -lm -lgsl -lgslcblas

SRCDIR = src
DTNORMDIR = dtnorm/src
OBJDIR_RELEASE = obj/release
OBJDIR_TEST = obj/test
BINDIR = bin
TESTDIR = test

INCLUDES = -I$(SRCDIR) -I$(DTNORMDIR)

SOURCES = $(wildcard $(SRCDIR)/*.c) $(wildcard $(DTNORMDIR)/*.c)
OBJECTS_RELEASE = $(patsubst $(SRCDIR)/%.c, $(OBJDIR_RELEASE)/%.o, $(SOURCES))
OBJECTS_TEST = $(patsubst $(SRCDIR)/%.c, $(OBJDIR_TEST)/%.o, $(SOURCES))

RELEASE_TARGET = $(BINDIR)/$(TARGET_NAME)
TEST_TARGET = $(BINDIR)/$(TARGET_NAME)_test

.PHONY: clean release test all

all: release

release: $(RELEASE_TARGET)

test: $(TEST_TARGET)
	cp $(TESTDIR)/test.glo $(TESTDIR)/000.glo
	mv $(TESTDIR)/000.csv $(TESTDIR)/old_000.csv
	rm -f $(TESTDIR)/000.frq $(TESTDIR)/000.ics
	./$(TEST_TARGET) $(TESTDIR)/000
	-diff $(TESTDIR)/000.csv $(TESTDIR)/old_000.csv

$(RELEASE_TARGET): $(OBJECTS_RELEASE)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) $^ $(LIBS) -o $@

$(TEST_TARGET): $(OBJECTS_TEST)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) $^ $(LIBS) -o $@

$(OBJDIR_RELEASE)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	@mkdir -p $(OBJDIR_RELEASE)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) -c $< -o $@

$(OBJDIR_RELEASE)/%.o: $(DTNORMDIR)/%.c
	@mkdir -p $(OBJDIR_RELEASE)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) -c $< -o $@

$(OBJDIR_TEST)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	@mkdir -p $(OBJDIR_TEST)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

$(OBJDIR_TEST)/%.o: $(DTNORMDIR)/%.c
	@mkdir -p $(OBJDIR_TEST)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OBJDIR_RELEASE) $(OBJDIR_TEST) $(BINDIR)/$(TARGET_NAME) $(BINDIR)/$(TARGET_NAME)_test
