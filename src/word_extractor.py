import argparse
from hanzipy.decomposer import HanziDecomposer
from hanzipy.dictionary import HanziDictionary
import logging.config

dictionary = HanziDictionary()
decomposer = HanziDecomposer()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    args = parser.parse_args()

    with open(args.in_file, "r") as file:
        lines = file.readlines()

    output = []
    hanziSet = {}

    for line in lines:
        line = line.strip()
        if line[0] == "#" or len(line) == 0:
            continue
        else:
            s = line.split("\t")
            print("{}".format(s[3]))
