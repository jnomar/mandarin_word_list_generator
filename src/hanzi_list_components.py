import argparse, sys
from hanzipy.decomposer import HanziDecomposer
from hanzipy.dictionary import HanziDictionary

dictionary = HanziDictionary()
decomposer = HanziDecomposer()

def get_components(comp_list):
    text = ""
    for comp in comp_list:
        text += comp + " "

    return text.strip()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("inFile")
    parser.add_argument("outFile")
    args = parser.parse_args()

    f = open(args.inFile)

    lines = f.readlines()
    output_hanzi = []

    with open(args.outFile, "w") as file:
        for line in lines:
            l = line.strip()
            if len(l) == 0:
               continue
            if len(l) == 1:
                components = decomposer.decompose(l)
                print("{}\n1: {}\n2: {}".format(l, components["once"], components["radical"]), file=sys.stderr)
                s = input()
                if s == '1':
                    file.write("{}\t{}\n".format(l, get_components(components["once"])))
                elif s == '2':
                    file.write("{}\t{}\n".format(l, get_components(components["radical"])))
                else:
                    file.write("{}\t{}\n".format(l, components))

            else:
                file.write("{}\t{}\n".format(l, components))

            file.flush()
