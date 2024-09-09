
with open("refold_mandarin_1k.txt", "r") as file:
    lines = file.readlines()

output = []

for line in lines:
    s = line.split("\t")
    output.append("{}\n".format(s[2]))

with open("refold_mandarin_1k_hanzi.txt", "w") as file:
    for o in output:
        file.write(o)

