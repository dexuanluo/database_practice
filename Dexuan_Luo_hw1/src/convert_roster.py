from sys import argv
import json


if __name__ == "__main__":
    _, _, roster_path, output_path = argv

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
            res.append({"Name" : name, "Participating from" : location})
            line = fd.readline()

    with open(output_path, "w") as fd:
        fd.write(json.dumps(res))