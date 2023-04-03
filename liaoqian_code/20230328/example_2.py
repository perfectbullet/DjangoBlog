import mysql.connector
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "apologizek24.",
    "database": "vega"
}
con = mysql.connector.connect(**config)
username = "1 OR 1=1"
password = "1 OR 1=1"
sql = "SELECT COUNT(*) FROM t_user WHERE username=%s "\
    "AND AES_DECRYPT(UNHEX(password),'Hello World')=%s";
cursor = con.cursor()
cursor.execute(sql, (username, password))
print(cursor.fetchone()[0])
con.close()
