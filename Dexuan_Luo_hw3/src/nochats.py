import sys
import json
import mysql.connector
query = """select firstname, lastname, location from 
                (select firstname, lastname, location, count(msg) 
                c from Student s left join Chat c on s.id=c.studentID 
                group by firstname, lastname, location) 
            as tmp where c=0;"""

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
    for firstname, lastname, location in cursor:
        lastname = capitalize_all(lastname)
        firstname = capitalize_all(firstname)
        name = firstname + " " + lastname
        
        res.append({"Person": name, "Participating from": location})
    
    with open(output_path, "w") as f:
        f.write(json.dumps(res))