# take a word list with words that contain multiple hanzi and break out the simpler words

included = {}
output = []

with open("resources/refold_hanzi", "r") as file:
    words = file.readlines()

for word in words:
    for char in word:
        if char == "\n":
            break

        if char not in included: 
            included[char] = True
            output.append("{}\n".format(char))

    
with open("resources/refold_hanzi_split", "w") as file:
    for char in output:
        file.write(char)

