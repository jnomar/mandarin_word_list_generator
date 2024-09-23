#!/usr/bin/python
import sys
from hanzipy.dictionary import HanziDictionary

dictionary = HanziDictionary()

if __name__ == "__main__":
    if len(sys.argv) > 1:
       f = open(sys.argv[1])
    else:
       f = sys.stdin 

    lines = f.readlines()

    hanzi_set = {}
    output_hanzi = []

    for line in lines:
        l = line.strip()
        if len(l) == 0:
           continue
        if len(l) == 1:
            if l not in hanzi_set:
                hanzi_set[l] = True
                output_hanzi.append(l)
        else:
            for hanzi in l:
                if hanzi not in hanzi_set:
                    hanzi_set[hanzi] = True
                    try:
                        traditional = False 
                        r = dictionary.definition_lookup(hanzi)
                        for h_def in r:
                            if hanzi == h_def["traditional"]:
                                traditional = True
                                break

                        if not traditional:
                            output_hanzi.append("{} make sure traditional".format(hanzi))
                        else:
                            output_hanzi.append("{}".format(hanzi))

                    except Exception as e:
                        output_hanzi.append("{}".format(hanzi))
                        
            output_hanzi.append(l)  
    
    for hanzi in output_hanzi:
        print(hanzi)


