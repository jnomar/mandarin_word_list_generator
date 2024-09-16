lines = []
with open("output/word_list.sv1", "r") as f:
    lines = f.readlines()

with open("output/word_list.sv1", "w+") as f:
    count = 1

    for line in lines:
        # leave headers and comments alone
        if line[0] == "#":
            f.write(line)
        else:
            fields = line.split("\t")
            f.write("{}\t{}".format(count, line)) 
            count += 1

