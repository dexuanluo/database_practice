from sys import argv
import json
import requests

URL = 'https://ds551test-default-rtdb.firebaseio.com/student.json?orderBy="$key"&equalTo='

def nameFormatter(name):
    name = name.lower().split(" ")
    for i in range(len(name)):
        name[i] = name[i].capitalize()

    return "_".join(name)

if __name__ == "__main__":

    _, name = argv

    name = nameFormatter(name)
    respond = json.loads(requests.get(URL + '"' + name + '"' ).text)

    if respond:
        if "msg" in respond[name]:
            for msg in respond[name]["msg"]:
                print("\t".join(msg))
        else:
            print("This student is quiet.")
    else:
        print("Student Not Found")
    