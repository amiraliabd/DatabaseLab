import mariadb
import os
from .exceptions import NotFound, IntegrityError


class UserRepo:
    def __init__(self):
        self.conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_TYPE'))
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self._get_or_create_database()
        self._get_or_create_table()

    def _get_or_create_database(self):
        self.cur.execute("CREATE DATABASE IF NOT EXISTS AZ_DB")
        self.cur.execute("USE AZ_DB;")

    def _get_or_create_table(self):
        # todo: unique value for email
        self.cur.execute("CREATE TABLE IF NOT EXISTS USER("
                         "id INT NOT NULL AUTO_INCREMENT,"
                         "f_name VARCHAR(20) NOT NULL,"
                         "l_name VARCHAR(20) NOT NULL,"
                         "email VARCHAR(20) NOT NULL UNIQUE,"
                         "PRIMARY KEY (id)"
                         ")"
                         )

    def insert(self, f_name: str, l_name: str, email: str):
        try:
            self.cur.execute(f"INSERT INTO USER (f_name, l_name, email) VALUES ('{f_name}', '{l_name}', '{email}')")
        except mariadb.IntegrityError:
            raise IntegrityError(f"User with email {email} already exists")

    def delete(self, user_id: int):
        self.retrieve(user_id)
        self.cur.execute(f"DELETE FROM USER WHERE id='{user_id}'")

    def list(self):
        self.cur.execute("SELECT * FROM USER ORDER BY id DESC")
        return list(self.cur)

    def retrieve(self, user_id: str):
        self.cur.execute(f"SELECT * FROM USER WHERE id='{user_id}'")
        user_obj = list(self.cur)
        if not user_obj:
            raise NotFound(f"no such user with id {user_id}")
        return user_obj

    def update(self, user_id, new_data):
        self.retrieve(user_id)
        update_query = ''
        for column in new_data:
            if new_data[column]:
                update_query += f"{column}='{new_data[column]}', "
        query = f"UPDATE USER SET {update_query[:-2]} WHERE id={user_id}"
        try:
            self.cur.execute(query)
        except mariadb.IntegrityError:
            raise IntegrityError(f"User with email {new_data['email']} already exists")
