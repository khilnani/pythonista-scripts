# coding: utf-8

import sys
if '.' not in sys.path:
    sys.path.insert(0, '.')
import sqlite3

class sqlite3utils (object):
    def __init__ (self,dbpath):
        self.conn = sqlite3.connect(dbpath)

    def run_query(self, sql):
        c = self.conn.execute(sql)
        data = c.fetchall()
        keys = [name[0] for name in c.description or []]
        return keys, data

    def get_table_data(self, table):
        return self.run_query('SELECT * FROM ' + table)

    def __get_tables (self):
        sql = 'SELECT * FROM sqlite_master WHERE type = "table"'
        return self.run_query(sql)

    def __get_views (self):
        sql = 'SELECT * FROM sqlite_master WHERE type = "view"'
        return self.run_query(sql)

    def get_all_tables_name(self):
        keys, tables = self.__get_tables()
        return [name[1] for name in tables]

    def get_all_tables(self):
        keys, tables = self.__get_tables()
        return [{key : value[i] for i, key in enumerate(keys)}
            for value in tables]

    def get_all_views_name(self):
        keys, views = self.__get_views()
        return [name[1] for name in views]

    def get_all_views(self):
        keys, views = self.__get_views()
        return [{key : value[i] for i, key in enumerate(keys)}
            for value in views]

    def get_all_system_tables(self):
        return ['sqlite_master']

    def table_info(self, tablename):
        return self.run_query('PRAGMA table_info('+tablename+')')[1]

    def index_info(self, tablename):
        return self.run_query('PRAGMA index_info('+tablename+')')[1]

    def close_db(self):
        self.conn.close()

if __name__ == '__main__':
    a = sqlite3utils(dbpath='../feeds1.db')
    print a.run_query('PRAGMA table_info(sqlite_master)')[1]
