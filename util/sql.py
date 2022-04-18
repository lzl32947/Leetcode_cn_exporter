import os.path
import sqlite3
import threading
from typing import List


class SQLiteDriver(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        if not hasattr(self, "dicts"):
            self.dicts = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(SQLiteDriver, "_instance"):
            with SQLiteDriver._instance_lock:
                if not hasattr(SQLiteDriver, "_instance"):
                    SQLiteDriver._instance = object.__new__(cls)
        return SQLiteDriver._instance

    def create_conn(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        conn = sqlite3.connect(os.path.join("data", "db", database_name))
        self.dicts[database_name] = conn
        if not self._has_init(conn):
            self._init_tabel(conn)

    def close_conn(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            self.dicts[database_name].close()

    def close_all(self):
        for k in self.dicts.keys():
            self.dicts[k].close()

    @staticmethod
    def _init_tabel(conn: sqlite3.Connection):
        with conn:
            conn.execute("""
                CREATE TABLE PROBLEMS(
                    problem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    identifier TEXT not null ,
                    title TEXT not null ,
                    link TEXT not null unique ,
                    difficulty INTEGER not null 
                );
            """)
            conn.execute("""
                CREATE TABLE TAGS(
                    tag_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                    tag_name TEXT not null unique,
                    tag_link TEXT not null 
                );
            """)

            conn.execute("""
                CREATE TABLE TAG_PROBLEMS(
                    problem_id INTEGER not null ,
                    tag_id INTEGER not null 
                );
            """)

    @staticmethod
    def _has_init(conn: sqlite3.Connection) -> bool:
        data = conn.execute(
            """
            SELECT count(*) 
            FROM sqlite_master 
            WHERE type= "table"
             AND name = "PROBLEMS";
            """
        )
        for result in data:
            if result[0] == 1:
                return True
            else:
                return False

    @staticmethod
    def _insert_into(conn: sqlite3.Connection, tabel: str, columns: List[str], data: List[tuple]):
        with conn:
            conn.executemany(
                "INSERT INTO {} ({}) VALUES ({})".format(tabel, ",".join(columns), ",".join(["?" for i in range(len(columns))])),
                data
            )

    @staticmethod
    def _find_in_single_table(conn: sqlite3.Connection, tabel: str, column: str, condition: str):
        ans = []
        res = conn.execute("SELECT * FROM {} WHERE {} {}".format(tabel, column, condition))
        for row in res:
            ans.append(row)
        return ans

    @staticmethod
    def _exist_in_single_table(conn: sqlite3.Connection, tabel: str, column: str, condition: str) -> bool:
        res = conn.execute("SELECT COUNT(*) FROM {} WHERE {} {}".format(tabel, column, condition))
        for row in res:
            if row[0] >= 1:
                return True
            else:
                return False

    @staticmethod
    def _find_tags_by_problem(conn: sqlite3.Connection):
        pass
