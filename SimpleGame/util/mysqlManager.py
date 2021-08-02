import pymysql


class MysqlManager:

    def __init__(self, host, user, passwd, db):
        self._host = host
        self._user = user
        self._passwd = passwd
        self.db = db
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host=self._host, user=self._user, passwd=self._passwd, db=self.db)

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def close(self):
        self.conn.close()


# cursor.execute('create database if not exists testDB default charset utf8 collate utf8_general_cli;')
sql = """create table `user`(
        `id` int(11) not null auto_increment,
        `name` varchar(255) not null,
        `age` int (11) not null,
        primary key (`id`)
        ) engine=InnoDB default charset=utf8 auto_increment=0
        """
