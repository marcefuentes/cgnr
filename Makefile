CC = gcc
CFLAGS_RELEASE = -DNDEBUG -O3 -finline-functions -Wall -lm -lgsl -lgslcblas
CFLAGS_TEST = -g -Wall -lm -lgsl -lgslcblas

SRCDIR = src
DTNORMDIR = dtnorm/src
OBJDIR = obj
BINDIR = bin
TESTDIR = test

INCLUDES = -I$(SRCDIR) -I$(DTNORMDIR)

SOURCES = $(wildcard $(SRCDIR)/*.c) $(wildcard $(DTNORMDIR)/*.c)
OBJECTS = $(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SOURCES))

RELEASE_TARGET = $(BINDIR)/gnr2
TEST_TARGET = $(BINDIR)/gnr2_test

.PHONY: clean release test

release: $(RELEASE_TARGET)
test: $(TEST_TARGET)
	mv $(TESTDIR)/t.csv $(TESTDIR)/old_t.csv
	rm -f $(TESTDIR)/t.gl2 $(TESTDIR)/t.frq $(TESTDIR)/t.ics
	./$(TEST_TARGET) $(TESTDIR)/t
	-diff $(TESTDIR)/t.csv $(TESTDIR)/old_t.csv

$(RELEASE_TARGET): $(OBJECTS)
	$(CC) $(CFLAGS_RELEASE) $(INCLUDES) $^ -o $@

$(TEST_TARGET): $(OBJECTS)
	$(CC) $(CFLAGS_TEST) $(INCLUDES) $^ -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c $(SRCDIR)/sim.h
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

$(OBJDIR)/%.o: $(DTNORMDIR)/%.c
	$(CC) $(CFLAGS_TEST) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OBJDIR)/*.o $(RELEASE_TARGET) $(TEST_TARGET)

