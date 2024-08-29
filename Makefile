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

RELEASE_TARGET = $(BINDIR)/cgnr
TEST_TARGET = $(BINDIR)/cgnr_test

.PHONY: clean release test all

all: release

release: $(RELEASE_TARGET)

test: $(TEST_TARGET)
	cp $(TESTDIR)/test.glo $(TESTDIR)/t.glo
	mv $(TESTDIR)/t.csv $(TESTDIR)/old_t.csv
	rm -f $(TESTDIR)/t.frq $(TESTDIR)/t.ics
	./$(TEST_TARGET) $(TESTDIR)/t
	-diff $(TESTDIR)/t.csv $(TESTDIR)/old_t.csv

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
	rm -rf $(OBJDIR_RELEASE) $(OBJDIR_TEST) $(BINDIR)/cgnr $(BINDIR)/cgnr_test
