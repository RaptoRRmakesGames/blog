import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def connect():
    db = mysql.connector.connect(
        host='localhost',
        user = 'root',
        passwd = '',
        database='blogsjunior',
        port = 3307
    )
    return db, db.cursor()

def login(username, password):

    db,c = connect()

    c.execute("SELECT * from `users` WHERE username=%s", [username])

    all_users = c.fetchall()

    if len(all_users) <= 0:
        return f"User '{username}' does not exist"
    
    logined =  check_password_hash(all_users[0][2], password)

    if logined:
        return 'Login Successfull'
    return 'Wrong Password'


def create_db():

    db,c = connect()

    c.execute("""
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(24),
    password VARCHAR(255)
);

CREATE TABLE blogs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    header VARCHAR(50),
    content VARCHAR(3000),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

""", multi=True)
    db.commit()

def add_blog(userid, header, content):
    db,c=  connect()

    c.execute("INSERT INTO `blogs` (user_id, header, content) VALUES (%s,%s,%s)", [userid,header,content])
    db.commit()

def add_user(username, password):
    db,c=  connect()

    c.execute("INSERT INTO `users` (username, password) VALUES (%s,%s)", [username,password])
    db.commit()

if __name__ == '__main__':
    try:
        connect()
        print("Database connected!")
    except Exception as e:
        print(e)

    e = input("what do you want to do?\n'check') checks connection \n'add') adds a record\n'create') creates the database\n'login') pseudo logins\n")

    match e:
        case 'check':
            try:
                connect()
                print("Database connected!")
            except Exception as e:
                print(e)

        case 'add':
            what = input("which table? (blogs/users) \n")

            if what == 'blogs':
                add_blog(int(input("user id: ")), input("header: "), input("content: "))
            elif what == "users":
                add_user(input("username: "), generate_password_hash(input("password: ")))

        case 'create':
            try:
                create_db()
                print("database created")
            except Exception as e:
                print(e, "\nError while creating database, most likely already created")
            
        case 'login':
            print(login(input("username: "), input("password: ")))
