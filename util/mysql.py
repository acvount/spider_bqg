import time
import pymysql
from util.color_log import Log
from util.key_map import KeyMap
import threading


class Database:
    def __init__(self, host, user, pwd, db):
        self.log = Log()
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self._lock = threading.Lock()

        try:
            self.conn = self._connect()
        except pymysql.err.OperationalError:
            time.sleep(2)
            self.conn = self._connect()

    def _connect(self):
        return pymysql.connect(
            host=self.host, user=self.user, password=self.pwd, database=self.db, connect_timeout=10)

    def get_connection(self):
        if not self.db:
            raise NameError("没有设置数据库信息")
        try:
            self.conn = self._connect()
        except pymysql.err.OperationalError:
            time.sleep(1)
            return self.get_connection()
        return self.conn.cursor()

    def _execute_sql(self, sql):
        with self._lock:
            with self.get_connection() as cursor:
                cursor.execute(sql)
                self.conn.commit()

    def _write_sql_to_file(self, sql):
        with open('redo.sql', 'a') as f:
            f.write(sql + '\n')

    def fetch_all_records(self, sql):
        with self._lock:
            with self.get_connection() as cursor:
                cursor.execute(sql)
                data_dict = [field[0] for field in cursor.description]
                return [dict(zip(data_dict, row)) for row in cursor.fetchall()]

    def execute_query(self, sql):
        return self.fetch_all_records(sql)

    def execute_non_query(self, sql, write_to_file=True):
        try:
            self.log.sql(sql)
            self._execute_sql(sql)
            if write_to_file:
                self._write_sql_to_file(sql)
        except pymysql.err.InternalError:
            self.log.sql(sql)

    def execute_insert(self, table, obj, write_to_file = False):
        cols = ', '.join(obj.keys())
        vals = ', '.join([f"'{value.replace(KeyMap.del_str, KeyMap.none_str)}'"
                          if isinstance(value, str) and value != 'now()' and 'select' not in value
                          else str(value) for value in obj.values()])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
        self.execute_non_query(sql,write_to_file=write_to_file)

    def execute_insert_by_index_column_not_repeat(self, table, obj, *args, write_to_file=False):
        conditions = " AND ".join([f"{column} = '{obj[column]}'" for column in args])
        sql = f"SELECT COUNT(*) AS c FROM {table} WHERE {conditions}"
        count = self.execute_query(sql)[0]['c']
        if count == 0:
            self.execute_insert(table, obj, write_to_file=write_to_file)
        else:
            self.log.error(f'The record already exists in the table {table} and the index columns are {args} and the index values are {", ".join([obj[column] for column in args])}')
