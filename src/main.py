import argparse
from hanzipy.decomposer import HanziDecomposer
from hanzipy.dictionary import HanziDictionary

dictionary = HanziDictionary()
decomposer = HanziDecomposer()

def load_hanzi_from_file(filename):
    hanzi = []
    with open(filename, "r") as file:
        lines = file.readlines()

    count = 0
    for line in lines:
        char = line.strip()
        hanzi.append(char)

    return hanzi

def get_frequent_hanzi(n):
    hanzi = []
    hanzi_dict = {}

    # get a list of hanzi
    for i in range(1, n):
        try:
            c = dictionary.get_character_in_frequency_list_by_position(i)
            r = dictionary.definition_lookup(c["character"], "traditional")
            d = decomposer.decompose(r[0]["traditional"], 1)
            
            hanzi.append({"index" : c["number"], 
                          "character" : r[0]["traditional"], 
                          "components" : d["components"], 
                          "pinyin" : c["pinyin"], 
                          "definition": c["meaning"]})

            hanzi_dict[r[0]["traditional"]] = {"index" : c["number"], 
                                               "components" : d["components"], 
                                               "pinyin" : c["pinyin"], 
                                               "definition": c["meaning"]} 
        except Exception as e:
            print(e)

    return hanzi, hanzi_dict

def component_number_histogram(hanzi): 
    histo = {}
    # process list
    for h in hanzi:
        index = len(h["components"])
        if index in histo:
            histo[index].append(h) 
        else:
            histo[index] = [h]

    return histo


# breaks each word(one or multiple characters) into its constituent parts
def add_component_deps(hanzi):
    hanzi.reverse()
    output_characters = []
    included = {}
    characters = []

    # should be a depth first search over the dependencies of the characters in 
    # hanzi array, given that there are no dependencies missing from the list 
    # already then the character will be added in the same order as its in the 
    # hanzi array
    while(True):
        # make sure there is at least one character in the characters array
        if len(characters) == 0:
            try:
                characters.append(hanzi.pop())
            except:
                break
    
        h = characters.pop() 
        unknown = get_unsatisfied_deps(included, 
                                       decomposer.decompose(h, 1)["components"], h)

        if len(unknown) == 0:
            output_characters.append(h)
            included[h] = True
        else:
            characters.append(h)
            characters.extend(unknown)

    return output_characters 

def create_output(hanzi):
    output = []
    just_hanzi = []
    for char in hanzi:
        if len(char) == 1:
            try:
                # original position, character, pinyin, description
                definition = dictionary.definition_lookup(char)
                if definition[0]["pinyin"][0].isupper() and len(definition) > 1:
                    pinyin = definition[1]["pinyin"]
                    meaning = definition[1]["definition"]
                else:
                    pinyin = definition[0]["pinyin"]
                    meaning = definition[0]["definition"]

                output.append("{} ({}) - {}\n".format(char, pinyin, meaning))
            except Exception as e:
                meaning = decomposer.get_radical_meaning(char)
                if meaning == None:
                    meaning = ""

                output.append("{} {}\n".format(char, meaning))
        else:
            output.append("{}\n".format(char))

    return output

def get_unsatisfied_deps(included, components, character):
    unknown = []
    for component in components:
        if component == character or component == "No glyph available":
            continue

        if component not in included:
            unknown.append(component)

    return unknown 

def get_refold_dict(file_name):

    with open(file_name, "r") as file:
        lines = file.readlines()
    
    refold_d = {}

    for line in lines:
        if(line[0] == "#"):
            continue
        s = line.split("\t")
        refold_d[s[3]] = line
    
    return refold_d

def get_output_line_word(line):
    s = line.split(" ")
    return s[0].strip()

def add_back_refold_words(output, file_name):
    refold_d = get_refold_dict(file_name)
    
    count = 0
    for count in range(len(output)):
        word = get_output_line_word(output[count])
        if word in refold_d:
            output[count] = refold_d[word] 
    
    return output 

def write_output(output, file_name):
    count = 0
    known = 0
    # write output to a file
    with open(file_name, "w") as file: 
        for line in output:
            s = line.split("\t")
            if(count < 501):
                count += 1
                if line[0].isnumeric():
                    known += 1

            file.write(line)

    print("total:{}  known:{}  unknown:{}  known%:{}".format(
        count, known, count-known, known/count))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("refold_list")
    parser.add_argument("out_file")
    args = parser.parse_args()
    
    #hanzi, hanzi_dict = get_frequent_hanzi(3000) 
    hanzi = load_hanzi_from_file(args.in_file) 
    hanzi = add_component_deps(hanzi)
    output = create_output(hanzi)
    output = add_back_refold_words(output, args.refold_list)
    write_output(output, args.out_file) 
