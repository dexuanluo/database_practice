import os
from sys import argv
from lxml.etree import parse

PUNCTUATION = "!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
WHITE_SPACE = " "

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

if __name__ == "__main__":

    _, input_path, index_path, keywords = argv

    keywords = keywords.split(" ")

    document = parse(index_path)
    candidates = {}
    for keyword in keywords:
        for node in document.xpath('//value[text()="{}"]/..//provenance'.format(keyword)):
            where, which = "", ""
            for child in node:
                if child.tag == "where":
                    where = child.text
                elif child.tag == "which":
                    which = child.text
            if which and which not in candidates:
                candidates[which] = set()
            if where:
                candidates[which].add(where)
    res = []
    for which in candidates:
        doc = parse(input_path + "/" + which)
        for where in candidates[which]:
            address = "/" + where.replace(".", "/")
            for node in doc.xpath(address):
                if node.text:
                    tokens = tokenizer(node.text, PUNCTUATION)
                    for keyword in keywords:
                        if keyword in tokens:
                            res.append((node, which))
                            break
    
    for node, fileName in res:
        print("Element: <{}>{}</{}>".format(node.tag, node.text.rstrip().lstrip(), node.tag))
        print("File: {}".format(fileName))
    
    if not res:
        print("No such tokens")



        
        
        
            