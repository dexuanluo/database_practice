from sys import argv
import json
import requests

def nameFormatter(s):
    res = []
    for a in s:
        if a not in "/[]#.$":
            res.append(a)
            
    return "".join(res).replace(" ", "_")
    
    return s

URL = "https://ds551test-default-rtdb.firebaseio.com/.json"

if __name__ == "__main__":
    _, chats_path, roster_path = argv
    
    roster_js = {}
    name_list = []
    with open(roster_path, "r") as fd:
        res = []
        line = fd.readline()
        while line:
            res.append(line)
            line = fd.readline()
        roster_js = {"student" : {
            nameFormatter(tmp["Name"]) : {
                "location" : tmp["Participating from"], 
                "msg" : []} for tmp in json.loads("".join(res))}}

    for name in roster_js["student"]:
        name_list.append(name)
    
    roster_js["student"]["NAME_LIST"] = name_list
    with open(chats_path) as fd:
        res = []
        line = fd.readline()
        while line:
            res.append(line)
            line = fd.readline()
        chat_js = json.loads("".join(res))
        for chat in chat_js :
            name, msg, time = nameFormatter(chat["Person"]), chat["Message"], chat["Time"]

            if name in roster_js["student"]:
                roster_js["student"][name]["msg"].append([time, msg])

    requests.put(URL, data=json.dumps(roster_js))
    
