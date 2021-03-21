import sys
import mysql.connector

query = """select firstname, lastname from Student where firstname=%s or lastname=%s;"""

def insensitify(raw_str):
    return raw_str.rstrip().lstrip().lower()

def capitalize_all(raw_str):
    raw_str = raw_str.split(" ")
    for i in range(len(raw_str)):
        raw_str[i] = raw_str[i].capitalize()
    return " ".join(raw_str)

def lookup(db, keyword):
    res = []
    cursor = db.cursor()
    keyword = insensitify(keyword)
    cursor.execute(query, (keyword, keyword))
    for firstname, lastname in cursor:
        firstname = capitalize_all(firstname)
        lastname = capitalize_all(lastname)
        res.append(firstname + " " + lastname)
    return res

if __name__ == "__main__":
    _, keywords = sys.argv

    db = mysql.connector.connect(
        host="localhost", 
        user="dsci551",
        password="Dsci-551", 
        database="dsci551",
        auth_plugin="mysql_native_password"
        )

    res = set()
    keywords = keywords.replace("'", "").split(" ")

    for keyword in keywords:
        for name in lookup(db, keyword):
            res.add(name)
    
    for name in res:
        print(name)
    if not res:
        print("Student Not Found")
    


