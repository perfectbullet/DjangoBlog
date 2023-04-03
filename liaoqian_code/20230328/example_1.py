import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="apologizek24.",
    database="runoob_db"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE runoob_db")

# for x in mycursor:
#     print(x)

# mycursor.execute("CREATE TABLE sites (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url VARCHAR(255))")

# sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
# val = ("RUNOOB", "https://www.runoob.com")
# mycursor.execute(sql, val)
#
# mydb.commit()  # 数据表内容有更新，必须使用到该语句
#
# print(mycursor.rowcount, "记录插入成功。")


# 批量插入
# sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
# val = [
#     ('Google', 'https://www.google.com'),
#     ('Github', 'https://www.github.com'),
#     ('Taobao', 'https://www.taobao.com'),
#     ('stackoverflow', 'https://www.stackoverflow.com/')
# ]
#
# mycursor.executemany(sql, val)
#
# mydb.commit()
#
# print("1 条记录已插入, ID:", mycursor.lastrowid)


# 查询数据
# mycursor.execute("SELECT * FROM sites")
#
# myresult = mycursor.fetchall()  # fetchall() 获取所有记录
#
# for x in myresult:
#     print(x)


# 只读一条数据
# mycursor.execute("SELECT * FROM sites")
#
# myresult = mycursor.fetchone()
#
# print(myresult)


# where条件语句
# sql = "SELECT * FROM sites WHERE name ='RUNOOB'"
#
# mycursor.execute(sql)
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)

# sql = "SELECT * FROM sites WHERE url LIKE '%oo%'"
#
# mycursor.execute(sql)
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# sql = "SELECT * FROM sites WHERE name = %s"
# na = ("RUNOOB",)
#
# mycursor.execute(sql, na)
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# 排序
# sql = "SELECT * FROM sites ORDER BY name DESC"
#
# mycursor.execute(sql)
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# limit
# mycursor.execute("SELECT * FROM sites LIMIT 3")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# 指定起始位置
# mycursor.execute("SELECT * FROM sites LIMIT 3 OFFSET 1")  # 0 为 第一条，1 为第二条
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)


# 删除记录
# sql = "DELETE FROM sites WHERE name = %s"
# na = ("stackoverflow",)
#
# mycursor.execute(sql, na)
#
# mydb.commit()
#
# print(mycursor.rowcount, " 条记录删除")


# update
# sql = "UPDATE sites SET name = %s WHERE name = %s"
# val = ("Taobao", "Tb")
#
# mycursor.execute(sql, val)
#
# mydb.commit()
#
# print(mycursor.rowcount, " 条记录被修改")


# 删除表
sql = "DROP TABLE IF EXISTS sites"

mycursor.execute(sql)
