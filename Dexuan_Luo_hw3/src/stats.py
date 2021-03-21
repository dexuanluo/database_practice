import sys
import json
import mysql.connector
query = """select firstname, lastname, count(msg) from Student s 
            right join Chat c on s.id=c.studentID group by firstname, 
            lastname;"""

def capitalize_all(raw_str):
    raw_str = raw_str.split(" ")
    for i in range(len(raw_str)):
        raw_str[i] = raw_str[i].capitalize()
    return " ".join(raw_str)

if __name__ == "__main__":

    _, output_path = sys.argv
    res = []
    db = mysql.connector.connect(
        host="localhost", 
        user="dsci551",
        password="Dsci-551", 
        database="dsci551",
        auth_plugin="mysql_native_password"
        )
    cursor = db.cursor()
    cursor.execute(query)
    for firstname, lastname, count in cursor:
        lastname = capitalize_all(lastname)
        firstname = capitalize_all(firstname)
        name = firstname + " " + lastname
        res.append({"Person": name, "Message": count})
    
    with open(output_path, "w") as f:
        f.write(json.dumps(res))