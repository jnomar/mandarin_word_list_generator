# import dictionary
from hanzipy.decomposer import HanziDecomposer
decomposer = HanziDecomposer()

# import decomposer
from hanzipy.dictionary import HanziDictionary
dictionary = HanziDictionary()




if __name__ == "__main__":
    
    hanzi = [] 
    histo = {}
    output = []
    
    # get a list of hanzi
    for i in range(1, 3000):
        try:
            c = dictionary.get_character_in_frequency_list_by_position(i)
            r = dictionary.definition_lookup(c["character"])
            d = decomposer.decompose(r[0]["traditional"], 2)
            
            hanzi.append([c["number"], r[0]["traditional"], d["components"], c["pinyin"], c["meaning"]])
        except Exception as e:
            print(e)

    # process list
    for h in hanzi:
        index = len(h[2])
        if index in histo:
            histo[index].append(h) 
        else:
            histo[index] = [h]


    count = 1
    # create output
    for i in range(20):
        if i in histo:
            for h in histo[i]:
                output.append("{}({}) {}{}({}) - {}\n".format(count, h[0], h[1], h[2], h[3], h[4]))
                count += 1

    # write output to a file
    with open("word_list.txt", "w") as file: 
        for line in output:
            file.write(line)
