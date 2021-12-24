import pymysql
from utils.decorator import print_for_call
from libs.log_obj import LogObj


logger = LogObj().get_logger()


class MysqlObj(object):
    _conn = None

    def __init__(self, host, username, password, port=3306, database=None, autocommit=True):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.autocommit = autocommit

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))

    @property
    def conn(self):
        if self._conn is None:
            logger.info("Init conn for {host}:{port} ->> {db}".format(host=self.host, port=self.port, db=self.database))
            self._conn = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                database=self.database,
                autocommit=self.autocommit,
                cursorclass=pymysql.cursors.SSDictCursor)
        return self._conn

    def run_sql_cmd(self, sql_cmd):
        logger.debug(sql_cmd)
        self.conn.ping(reconnect=True)
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute(sql_cmd)
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                rows.append(row)
        return rows


if __name__ == '__main__':
    username = 'root'
    password = 'P@ssw0rd'
    host = '192.168.0.14'
    mysql_obj1 = MysqlObj(host, username, password)
    # mysql_obj2 = MysqlObj(host, username, password)
    # show_databases = 'show databases'

    def all_user_id_real_name(mysql_obj):
        all_users = {}
        for user in mysql_obj.run_sql_cmd("select id,name from devops.user"):
            all_users[user['id']] = user['name']
        return all_users

    print(all_user_id_real_name(mysql_obj1))
