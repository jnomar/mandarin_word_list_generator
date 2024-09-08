# import dictionary
from hanzipy.decomposer import HanziDecomposer
decomposer = HanziDecomposer()

# import decomposer
from hanzipy.dictionary import HanziDictionary
dictionary = HanziDictionary()




if __name__ == "__main__":
    
    with open("word_list.txt", "w") as file: 

        for i in range(1, 3000):
            try:
                c = dictionary.get_character_in_frequency_list_by_position(i)
                r = dictionary.definition_lookup(c["character"])
                line = "{} {}({}) - {}\n".format(c["number"], r[0]["traditional"], c["pinyin"], c["meaning"]) # number, character, description
                file.write(line)
            except Exception as e:
                print(e)

