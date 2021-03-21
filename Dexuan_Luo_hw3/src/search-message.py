import sys
import mysql.connector

query_id = """select id from Student where firstname= %s and lastname = %s;"""
query_search = """select time, msg from Chat where studentID=%s;"""
def insensitify(raw_str):
    return raw_str.rstrip().lstrip().lower()
if __name__ == "__main__":
    _, name = sys.argv
    db = mysql.connector.connect(
        host="localhost", 
        user="dsci551",
        password="Dsci-551", 
        database="dsci551",
        auth_plugin="mysql_native_password"
        )
    name = insensitify(name.replace("'", "")).split(" ")
    lastname = name[-1]
    firstname = " ".join(name[:len(name) - 1])

    cursor = db.cursor()
    cursor.execute(query_id, (firstname, lastname))

    idx = []
    for i in cursor:
        idx = list(i)

    if not idx:
        print("Student Not Found")
    else:
        cursor = db.cursor()
        cursor.execute(query_search, idx)
        res = []
        for ts, msg in cursor:
            res.append((ts.replace(" ", ""), msg))
        for ts, msg in res:
            print(ts, msg)
        if not res:
            print("This student is quiet.")

    
    