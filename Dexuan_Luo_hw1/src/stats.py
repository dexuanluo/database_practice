from sys import argv
import json

DELIMI = "\t"

def txtPreClean(line):
    line = line.rstrip()
    line = line.lstrip()
    return line
def getName(line, delimiter):
    lines = line.split(delimiter)
    name = lines[2].split("from ")[1].split(" to everyone:")[0]
    return name

if __name__ == "__main__":
    input_path = argv[1]
    output_path = argv[2]

    freq = {}

    with open(input_path, "r") as fd:
        line = fd.readline()

        while line:
            line = txtPreClean(line)
            if line:
                name = getName(line, DELIMI)
                if name not in freq:
                    freq[name] = 0
                freq[name] += 1
                
            line = fd.readline()
    
    with open(output_path, "w") as fd:
        fd.write(json.dumps(freq))