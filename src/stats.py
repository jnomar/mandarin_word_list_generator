# find the percentages of characters with 1, 2, 3, ... components in them
from hanzipy.decomposer import HanziDecomposer
decomposer = HanziDecomposer()

#file = "output/radical_test"
file = "output/word_component_list.txt"


with open(file, "r") as file:
    lines = file.readlines()

highest = 0
count = {}
components = {}
radicals = {}
character_components = {}
character_radicals = {}
total = 0

characters = {}
for line in lines:
    tmp = line.split("\t")

    if len(tmp[0]) == 1:
        characters[tmp[0]] = True

for line in lines:
    tmp = line.split("\t")

    if len(tmp) == 1:
        if len(tmp[0]) == 1:
            if tmp[0] not in characters:
                characters[tmp[0]] = True

    if len(tmp) == 2:
        comps = tmp[1].split(" ")
        for c in comps:
            if c not in characters:
                if decomposer.get_radical_meaning(c) is not None:
                    if c in radicals:
                        radicals[c] += 1
                    else:
                        radicals[c] = 1
                else:
                    if c in components:
                        components[c] += 1
                    else:
                        components[c] = 1
            else:
                if decomposer.get_radical_meaning(c) is not None:
                    if c in character_radicals:
                        character_radicals[c] += 1
                    else:
                        character_radicals[c] = 1
                else:
                    if c in character_components:
                        character_components[c] += 1
                    else:
                        character_components[c] = 1


        c_num = len(comps)
        if c_num > highest:
            highest = c_num

        if c_num in count:
            count[c_num] += 1
        else:
            count[c_num] = 1

        total += 1

print("number of components: {}".format(len(components) + len(radicals)))
print("number of radicals: {}".format(len(radicals)))

print()
print("characters with x number of components:")
for i in range(1, highest+1):
    if i in count:
        print("\t{} - {}".format(i, count[i]))


print()
for k in radicals.keys():
    print("{} - {}".format(k, radicals[k]))


count = {}

for k in components.keys():
    c = components[k]

    if c in count:
        count[c] += 1
    else:
        count[c] = 1


print("number of components used x times:")
for i in range(1, 1000):
    if i in count:
        print("\t{} - {}".format(i, count[i]))
