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
                                       decomposer.decompose(h, 1)["components"],
                                       h)

        if len(unknown) == 0:
            output_characters.append(h)
            included[h] = True
        else:
            characters.append(h)
            # get rid of any duplicates like in (xiu4xie) which will be added 
            h = {}
            for c in unknown:
                h[c] = True

            for k in h.keys():
                characters.append(k)

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

                pinyin = convert_pinyin(pinyin) 

                output.append("component\t{}\t{}\t{}\n".format(char, pinyin, meaning))
            except Exception as e:
                pass
                #meaning = decomposer.get_radical_meaning(char)
                #if meaning == None:
                #    meaning = ""
                #output.append("c\t{}\t??\t{}\n".format(char, meaning))
        else:
            output.append("component\t{}\n".format(char))

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
    s = line.split("\t")
    return s[1].strip()

def get_refold_word_info(w):
    w = w.split('\t')
    output = ""
    
    li = [3, 4, 5, 6, 7, 9, 10, 11, 12 ,13 ,14 ,15 ,16]

    for i in range(3, len(w)):
        if i in li:
            output += "{}\t".format(w[i])

    return "{}\n".format(output.strip())

def add_back_refold_words(output, file_name):
    refold_d = get_refold_dict(file_name)
    
    count = 0
    for count in range(len(output)):
        word = get_output_line_word(output[count])
        if word in refold_d:
            output[count] = "refold\t{}".format(get_refold_word_info(refold_d[word])) 
            #output[count] = refold_d[word] 
            #print(refold_d[word])
    
    return output 

def write_output(output, file_name):
    # write output to a file
    with open(file_name, "w") as file: 
        for line in output:
            s = line.split("\t")

            file.write(line)


# converts from pinyin with the tone represented as number at the end of the
# string i.e (yang2) to the tone above the appropriate vowel i.e (yang2) -> (yáng)
def convert_pinyin(pinyin):
    vowels = ['ai', 'ao', 'ei', 'ia', 'iao', 'ie', 'io', 'iu', 'ou', 'ua', 
              'uai', 'ue', 'ui', 'uo', 'üa', 'üe', 'a', 'e', 'i', 'o', 'u', 'ü']

    vowel = { 'a' : ['', 'ā', 'á', 'ǎ', 'à'],
              'e' : ['', 'ē', 'é', 'ě', 'è'],
              'i' : ['', 'ī', 'í', 'ǐ', 'ì'],
              'o' : ['', 'ō', 'ó', 'ǒ', 'ò'],
              'u' : ['', 'ū', 'ú', 'ǔ', 'ù'],
              'ü' : ['', 'ǖ', 'ǘ', 'ǚ', 'ǜ']}

    replacement = {'uai': 'a', 'iao': 'a', 'ai' : 'a', 'ao' : 'a', 'ei' : 'e', 
                   'ia' : 'a', 'ie' : 'e', 'io' : 'o', 'iu' : 'u', 'ou' : 'o', 
                   'ua' : 'a', 'ue' : 'e', 'ui' : 'i', 'uo' : 'o', 'üa' : 'a', 
                   'üe' : 'e', 'a'  : 'a', 'e'  : 'e', 'i'  : 'i', 'o'  : 'o',
                   'u'  : 'u', 'ü'  : 'ü'}

    # copy the tone number and remove 
    # it from the end of the pinyin
    tone = pinyin[-1]
    pinyin = pinyin[0:-1]

    if tone == 5:
        return pinyin

    found_v = None
    for v in vowels:
        if v in pinyin: 
            found_v = v
            break

    if found_v is not None:
        pinyin = pinyin.replace(replacement[v], vowel[replacement[v]][int(tone)])

    return pinyin

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
