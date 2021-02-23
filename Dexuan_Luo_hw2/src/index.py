import os
from sys import argv
from xml.etree import ElementTree as ET

PUNCTUATION = "!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
WHITE_SPACE = " "

def isXML(path):
    path = path.split(".")
    if path[-1] == "xml":
        return True
    return False

def tokenizer(val, delimiter):
    val = val.rstrip().lstrip()
    res = []
    if val:
        container = []
        for ch in val:
            if ch not in delimiter:
                container.append(ch)
            else:
                if container:
                    if container[-1].isnumeric() and ch == ".":
                        container.append(ch)
                    elif container[-1] != WHITE_SPACE:
                        container.append(WHITE_SPACE)
        tmp = "".join(container).split(WHITE_SPACE)
        for token in tmp:
            token = token.rstrip().lstrip()
            if token:
                res.append(token)
    return res
    
def record(fileName, path, tokens, indexTree):
    
    for token in tokens:
        if token not in indexTree:
            indexTree[token] = []
        indexTree[token].append((fileName, path))


def dfs(fileName, node, indexTree):
    stack = [(node, node.tag)]
    while stack:
        node, path = stack.pop()
        if node.text:
            tokens = tokenizer(node.text, PUNCTUATION)
            record(fileName, path, tokens, indexTree)
        
        for child in node:
            stack.append((child, path + "." + child.tag))

def serialize(indexTree, output_path):
    with open(output_path, "w") as file:
        file.write("<index>\n")
        for token in indexTree:
            res = []
            res.append("\t<token>\n")
            res.append("\t\t<value>{}</value>\n".format(token))
            for which, where in indexTree[token]:
                res.append("\t\t<provenance>\n")
                res.append("\t\t\t<which>{}</which>\n".format(which))
                res.append("\t\t\t<where>{}</where>\n".format(where))
                res.append("\t\t</provenance>\n")
            res.append("\t</token>\n")
            file.write("".join(res))
        file.write("</index>\n")

if __name__ == "__main__":
    _, input_path, output_path = argv
    indexTree = {}
    i = 0
    for _, _, files in os.walk(input_path):
        for f in files:
            if isXML(f):
                node = ET.parse(input_path + "/" + f).getroot()
                dfs(f, node, indexTree)

    serialize(indexTree, output_path)

    
    
                
                 
            

