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
    _, _, log_path, roster_path, output_path = argv

    
    freq = {}

    with open(log_path, "r") as fd:
        line = fd.readline()
        while line:
            line = txtPreClean(line)
            if line:
                name = getName(line, DELIMI)
                if name not in freq:
                    freq[name] = 0
                freq[name] += 1
            line = fd.readline()


    res = []

    with open(roster_path, "r") as fd:

        line = fd.readline()
        line = fd.readline()
        while line:
            
            line = line.split(",")
            last_name, first_name, location = line
            first_name = first_name.replace("\"", "")
            last_name = last_name.replace("\"", "")
            last_name = last_name.rstrip()
            last_name = last_name.lstrip()
            first_name = first_name.rstrip()
            first_name = first_name.lstrip()
            location = location.rstrip()

            name = first_name + " " + last_name
            if name not in freq:
                res.append({"Name" : name, "Participating from" : location})
            line = fd.readline()
    

    with open(output_path, "w") as fd:
        fd.write(json.dumps(res))
        
