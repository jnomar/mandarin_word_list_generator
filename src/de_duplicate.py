import sys

f = open(sys.argv[1])

lines = f.readlines()
found = {}

for line in lines:
    l = line.split()

    if l[0] not in found:
        found[l[0]] = True
    else:
        continue

    print(line.strip())
