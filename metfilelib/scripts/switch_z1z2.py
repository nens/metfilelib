#!/usr/bin/env python
"""Helper script to switch Z1 and Z2 values in a directory of .met
files."""

import os


def directory():
    """Which directory to search in. Let's keep it simple: we use the
    directory that this script is located in."""
    return os.path.dirname(os.path.realpath(__file__))


def files():
    """Yield the files to process. We return all .txt and .met files
    in the directory."""
    d = directory()
    for filename in os.listdir(d):
        if (os.path.splitext(filename)[-1].lower() in
           ('.txt', '.met')):
            yield os.path.join(d, filename)


class LineReplacer(object):
    """Context manager and iterator. Loop over lines, call
    replacer.replace() on the lines that need replacing, saves the new
    file at the end."""
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.lines = open(self.path, 'rU').readlines()
        self.last_yielded_line = None
        self.changed = False

    def __next__(self):
        if self.last_yielded_line is None:
            line_to_yield = 0
        else:
            line_to_yield = self.last_yielded_line + 1

        if len(self.lines) <= line_to_yield:
            raise StopIteration()

        self.last_yielded_line = line_to_yield
        return self.lines[line_to_yield]

    def replace(self, l):
        print('line {num} becomes {l}'.format(num=self.last_yielded_line, l=l))
        if self.lines[self.last_yielded_line] != l:
            self.lines[self.last_yielded_line] = l
            self.changed = True

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and self.changed:
            f = open(self.path, 'w')
            for l in self.lines:
                f.write(l)
            f.close()
        elif exc_type:
            print(exc_type)


def switched(line):
    return "whee\n"


def switch_z1z2():
    for path in files():
        print("Processing '{path}'.".format(path=path))
        with LineReplacer(path) as replacer:
            for line in replacer:
                replacer.replace(switched(line))
