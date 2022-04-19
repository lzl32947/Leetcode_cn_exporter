import os.path
import sqlite3
import threading
from typing import List, Optional


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
        conn = sqlite3.connect(os.path.join("data", "db", database_name), check_same_thread=False)
        self.dicts[database_name] = conn
        if not self._has_init(conn):
            self._init_tabel(conn)

    def insert_into_problems(self, database_name: str, data: List[tuple]):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            self._insert_into(self.dicts[database_name], "PROBLEMS", ["problem_id", "identifier", "title", "full_title", "link", "difficulty"], data)

    def insert_into_tags(self, database_name: str, data: List[tuple]):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            self._insert_into(self.dicts[database_name], "TAGS", ["tag_name", "tag_link"], data)

    def insert_into_problems_tags(self, database_name: str, data: List[tuple]):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            self._insert_into(self.dicts[database_name], "PROBLEMS_TAGS", ["problem_id", "tag_id"], data)

    def find_tag_id(self, database_name: str, tag_name: Optional[str] = None, tag_link: Optional[str] = None):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            return self._find_tag_id(self.dicts[database_name], tag_name, tag_link)

    def find_problem_not_exist_tag(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            result = self._find_problem_not_exist_tag(self.dicts[database_name])
            return result
        else:
            return None

    def find_exist(self, database_name: str, tabel: str, column: str, condition: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            return self._exist_in_single_table(self.dicts[database_name], tabel, column, condition)
        else:
            return None

    def find_all_problems(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            result = self._all_problems(self.dicts[database_name])
            return result
        else:
            return None

    def find_all_problems_with_tags(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            result = []
            problem_result = self._all_problems(self.dicts[database_name])
            for problem in problem_result:
                problem_id = problem[0]
                tag_list = self._find_tag_by_problem_id(self.dicts[database_name], problem_id)
                item = [i for i in problem]
                item.append(tag_list)
                result.append(item)
            return result
        else:
            return None

    def find_all_problem_by_tags(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            result = {}
            tag_result = self._all_tags(self.dicts[database_name])
            for tag in tag_result:
                tag_id = tag[0]
                tag_name = tag[1]
                problem_list = self._find_problems_by_tag(self.dicts[database_name], tag_id)
                result[tag_name] = problem_list
            return result
        else:
            return None

    def close_conn(self, database_name: str):
        if not database_name.endswith(".sqlite"):
            database_name = database_name + ".sqlite"
        if database_name in self.dicts.keys():
            self.dicts[database_name].close()
            del self.dicts[database_name]

    def close_all(self):
        for k in self.dicts.keys():
            self.dicts[k].close()

    @staticmethod
    def _init_tabel(conn: sqlite3.Connection):
        with conn:
            conn.execute("""
                CREATE TABLE PROBLEMS(
                    problem_id INTEGER NOT NULL PRIMARY key ,
                    identifier TEXT not null ,
                    title TEXT not null ,
                    full_title TEXT not null ,
                    link TEXT not null unique ,
                    difficulty TEXT not null 
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
                CREATE TABLE PROBLEMS_TAGS(
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
                "INSERT OR IGNORE INTO {} ({}) VALUES ({});".format(tabel, ",".join(columns), ",".join(["?" for i in range(len(columns))])),
                data
            )

    @staticmethod
    def _find_in_single_table(conn: sqlite3.Connection, tabel: str, column: str, condition: str):
        ans = []
        res = conn.execute("SELECT * FROM {} WHERE {} {};".format(tabel, column, condition))
        for row in res:
            ans.append(row)
        return ans

    @staticmethod
    def _exist_in_single_table(conn: sqlite3.Connection, tabel: str, column: str, condition: str) -> bool:
        res = conn.execute("SELECT COUNT(*) FROM {} WHERE {} {};".format(tabel, column, condition))
        for row in res:
            if row[0] >= 1:
                return True
            else:
                return False

    @staticmethod
    def _find_problem_not_exist_tag(conn: sqlite3.Connection):
        ans = []
        res = conn.execute(
            """
            SELECT PROBLEMS.problem_id,PROBLEMS.link
            FROM PROBLEMS LEFT JOIN PROBLEMS_TAGS ON PROBLEMS.problem_id = PROBLEMS_TAGS.problem_id 
            WHERE PROBLEMS_TAGS.problem_id is NULL;
            """)
        for row in res:
            ans.append(row)
        return ans

    @staticmethod
    def _find_tag_id(conn: sqlite3.Connection, tag_name: Optional[str], tag_link: Optional[str]):
        if tag_name is None and tag_link is None:
            return None
        elif tag_name is None:
            result = SQLiteDriver._find_in_single_table(conn, "TAGS", "tag_link", "=\"{}\"".format(tag_link))
            return result[0][0]
        else:
            result = SQLiteDriver._find_in_single_table(conn, "TAGS", "tag_name", "=\"{}\"".format(tag_name))
            return result[0][0]

    @staticmethod
    def _find_tag_by_problem_id(conn: sqlite3.Connection, problem_id: int):
        result = conn.execute("SELECT tag_name FROM PROBLEMS NATURAL JOIN PROBLEMS_TAGS NATURAL JOIN TAGS WHERE problem_id={};".format(problem_id))
        ans = []
        for row in result:
            ans.append(row[0])
        return ans

    @staticmethod
    def _all_problems(conn: sqlite3.Connection):
        result = conn.execute("SELECT * FROM PROBLEMS;")
        ans = []
        for row in result:
            ans.append(row)
        return ans

    @staticmethod
    def _all_tags(conn: sqlite3.Connection):
        result = conn.execute("SELECT * FROM TAGS;")
        ans = []
        for row in result:
            ans.append(row)
        return ans

    @staticmethod
    def _find_problems_by_tag(conn: sqlite3.Connection, tag_id: int):
        result = conn.execute(
            "SELECT problem_id,identifier,title,full_title,link,difficulty FROM PROBLEMS NATURAL JOIN PROBLEMS_TAGS NATURAL JOIN TAGS WHERE tag_id={};".format(
                tag_id))
        ans = []
        for row in result:
            ans.append(row)
        return ans
