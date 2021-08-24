import pymysql

conn = pymysql.connect(host="localhost", user="ribincao", passwd="Qq552425416.", db="game")
# print(conn)
# print(type(conn))

cursor = conn.cursor()
# print(cursor)

# cursor.execute('create database if not exists testDB default charset utf8 collate utf8_general_cli;')
sql = """create table `user`(
        `id` int(11) not null auto_increment,
        `name` varchar(255) not null,
        `age` int (11) not null,
        primary key (`id`)
        ) engine=InnoDB default charset=utf8 auto_increment=0
        """
cursor.execute(sql)
cursor.close()
conn.close()
print("ok")


