from sys import argv
import json
import requests

URL = "https://ds551test-default-rtdb.firebaseio.com/student/NAME_LIST.json"

def isMatch(key_words, name):
    name = name.lower()
    name = name.split("_")
    for word in key_words:
        if word in name:
            return True
    return False

if __name__ == "__main__":
    _, key_words = argv

    key_words = key_words.split(" ")

    for i in  range(len(key_words)):
        key_words[i] = key_words[i].lower()

    respond = requests.get(URL)

    name_list = json.loads(respond.text)

    res = []

    for name in name_list:
        if isMatch(key_words, name):
            res.append(" ".join(name.split("_")))
    
    if res:
        for name in res:
            print(name)
    else:
        print("Student Not Found")



    



