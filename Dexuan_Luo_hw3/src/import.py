import mysql.connector
import sys

def set_schema(db):
    cursor = db.cursor()
    cursor.execute("drop table if exists Chat;")
    cursor.execute("drop table if exists Student;")

    cursor.execute("""create table Chat(id BIGINT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                        studentID INT(6) not null,
                                        date varchar(15) not null,
                                        time varchar(10) not null,
                                        msg varchar(200));""")
    
    cursor.execute("""create table Student(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                        firstname varchar(50) not null,
                                        lastname varchar(50) not null,
                                        location varchar(50) not null);""")

def insensitify(raw_str):
    return raw_str.rstrip().lstrip().lower()

def extract_roster(raw_str):
    raw_str = raw_str.replace('"', '')
    firstname, lastname, location = raw_str.split(',')
    return (insensitify(firstname), insensitify(lastname), location.rstrip().lstrip())
    
def upload_roster(db, roster):
    cursor = db.cursor()
    for val in roster:
        query = "INSERT INTO Student (lastname, firstname, location) VALUES (%s, %s, %s)"
        cursor.execute(query, val)  
    db.commit()

def get_student_id(db):
    cache = {}
    cursor = db.cursor()
    cursor.execute("select id, firstname, lastname from Student;")
    for idx, firstname, lastname in cursor:
        cache[firstname + " " + lastname] = idx
    return cache
def extract_chat(raw_str):
    raw_str = insensitify(raw_str)
    datetime, timestamp, name, msg = raw_str.split("\t")
    datetime = insensitify(datetime)
    timestamp = insensitify(timestamp)
    name = insensitify(name.replace("from","").replace("to everyone:", ""))
    msg = msg.rstrip().lstrip()
    return (datetime, timestamp, name, msg)

def upload_chat(db, chats, idx_book):
    cursor = db.cursor()
    for datetime, timestamp, name, msg in chats:
        if name in idx_book:
            query = "INSERT INTO Chat (studentID, date, time, msg) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (idx_book[name], datetime, timestamp, msg))
    db.commit()



if __name__ == "__main__":

    _, roster_path, chat_path = sys.argv

    roster = []
    chats = []

    with open(roster_path, "r") as f:
        f.readline()
        line = f.readline()
        while line:
            roster.append(extract_roster(line))
            line = f.readline()

    with open(chat_path, "r") as f:
        line = f.readline()   
        while line:
            line = line.rstrip().lstrip()
            if line:
                chats.append(extract_chat(line))
                
            line = f.readline()

    db = mysql.connector.connect(
        host="localhost", 
        user="dsci551",
        password="Dsci-551", 
        database="dsci551",
        auth_plugin="mysql_native_password"
        )
    
    set_schema(db)
    upload_roster(db, roster)
    cache = get_student_id(db)
    upload_chat(db, chats, cache)
    

    db.close()
