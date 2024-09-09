# create a dictionary with all of the characters in the single character list
hanzi = {}
with open("resources/hanzi_list", "r") as file:
            continue
    lines = file.readlines()

for line in lines:
    hanzi[line[0]] = True



with open("resources/refold_hanzi", "r") as file:
    lines = file.readlines()

output = []

include = True
for line in lines:
    for char in line:
        if char == "\n":
            break
        if char not in hanzi:
            print("{} not in list".format(char))
            include = False
            break

    if include:
        output.append(line)

    include = True


with open("resources/refold_hanzi_valid", "w") as file:
    for line in output:
        file.write(line)

