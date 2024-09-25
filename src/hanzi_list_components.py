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

def get_last_character(outFile):
    # if the script has already been run get the last character that was processed
    # in order to find the next one
    try:
        with open(outFile, "r") as file:
            lines = file.readlines()
            if len(lines) != 0:
                return lines[-1].split("\t")[0]
    except:
        pass

    return None

def valid_hanzi(hanzi_list):
    for h in hanzi_list:
        if h == "No glyph available":
            return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inFile")
    parser.add_argument("outFile")
    parser.add_argument("--truncate", default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.truncate:
        outFileMode = "w"
    else:
        outFileMode = "a"

    with open(args.inFile, "r") as file:
        lines = file.readlines()

    if not args.truncate:
        last_character = get_last_character(args.outFile)
        if last_character is not None:
            count = 1 

            for line in lines:
                if line.strip() == last_character:
                    break
                count += 1

            if count < len(lines):
                lines = lines[count:]
            else:
                quit()

    with open(args.outFile, outFileMode) as file:
        for line in lines:
            l = line.strip().split("\t")
        
            if len(l) == 0:
               continue
            elif len(l) == 1 and len(l[0]) == 1:
                components = decomposer.decompose(l[0])
                
                if valid_hanzi(components["radical"]):
                        file.write("{}\t{}\n".format(l[0], get_components(components["radical"])))
                elif valid_hanzi(components["once"]):
                        file.write("{}\t{}\n".format(l[0], get_components(components["once"])))
                else:
                        file.write("{}\t{}\n".format(l[0], components))

            else:
                file.write("{}\n".format(line.strip()))

            file.flush()
