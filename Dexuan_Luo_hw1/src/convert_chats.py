from sys import argv
import json

DELIMI = "\t"

def txtPreClean(line):
    line = line.rstrip()
    line = line.lstrip()
    return line

def getElements(line, delimiter):
    _, time, name, msg = line.split(delimiter)
    time = txtPreClean(time)
    name = name.split("from ")[1].split(" to everyone:")[0]
    msg = txtPreClean(msg)
    return time, name, msg

if __name__ == "__main__":
    input_path = argv[1]
    output_path = argv[2]

    res = []
    with open(input_path, "r") as fd:
        line = fd.readline()
        while line:
            line = txtPreClean(line)
            if line:
                time, name, msg = getElements(line, DELIMI)
                res.append({"Time":time, "Person":name, "Message":msg})
            line = fd.readline()

    

    with open(output_path, "w") as fd:
        fd.write(json.dumps(res))