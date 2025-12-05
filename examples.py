import os
from zoomrlib.seq import Sequence

DATADIR = os.path.abspath("./data")


def multiply_pattern():
    seq = Sequence()
    seq.multiply_notes()
    seq.write_file()


if __name__ == "__main__":
    os.chdir(DATADIR)
    multiply_pattern()
