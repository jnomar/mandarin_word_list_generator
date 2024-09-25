#!/usr/bin/python
import sys, collections
from hanzipy.dictionary import HanziDictionary

dictionary = HanziDictionary()

if __name__ == "__main__":
    if len(sys.argv) > 1:
       f = open(sys.argv[1])
    else:
       f = sys.stdin 

    lines = f.readlines()
    
    count = 0

    while True: 
        hanzi_set = {}
        found = {}

        output = []

        for line in lines:
            l = line.strip().split("\t")
            
            if len(l) == 1 and len(l[0]) == 1:
                hanzi_set[l[0]] = True

            elif len(l) == 2 and len(l[0]) == 1:
                # make sure we arne't processing something that has already been processed
                found[l[0]] = line.strip()
                if l[0] not in hanzi_set:
                    hanzi_set[l[0]] = True
                else:
                    continue

                for hz in l[1].split():
                    if hz not in hanzi_set:
                        hanzi_set[hz] = True
                        output.append(hz)
                        #print(hz)
            
            #print(line.strip())
            output.append(line.strip())


        for i in range(len(output)):
            if len(output[i]) == 1:
                if output[i] in found:
                    output[i] = found[output[i]]

        if set(output) == set(lines):
            break

        lines = output

    found = {}

    for o in output:
        s = o.split("\t")
        if s[0] not in found:
            found[s[0]] = True
        else:
            continue

        print(o)
