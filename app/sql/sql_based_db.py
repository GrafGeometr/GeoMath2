from app.sql.abstract_db import AbstractDB
from app.sql.db_column_types import DBColumn, Int, relationship
import sqlite3


class SQLBasedDB(AbstractDB):
    def __init__(self, filename):
        self.filename = filename

    def add_tables(self, *cls_list):
        for cls in cls_list:
            properties = [
                (name, getattr(cls, name))
                for name in dir(cls)
                if isinstance(getattr(cls, name), DBColumn)
            ]

            # add table if not exists
            print(self.filename)
            conn = sqlite3.connect(self.filename)
            cur = conn.cursor()
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} "
                f"({','.join([f'{name} {col.type}' for name, col in [('id', Int(primary_key=True))] + properties])})"
            )
            conn.commit()
            conn.close()

            print(properties)

            cls.defaults = {name: col.default for name, col in properties}

            for name, col in properties:

                def getter(obj, name=name):
                    return self.get_value(cls, obj.id, name)

                def setter(obj, value, name=name):
                    self.set_value(cls, obj.id, name, value)

                setattr(cls, name, property(getter, setter))

            def get_by_id(id):
                result = cls()
                result.id = id
                return result

            setattr(cls, "get_by_id", get_by_id)

            def new(**kwargs):
                result = cls()
                id = self.add_empty_row(cls)
                for key, value in kwargs.items():
                    self.set_value(cls, id, key, value)
                result.id = id
                return result

            setattr(cls, "new", new)

        for cls in cls_list:
            relations = [
                (
                    name,
                    getattr(cls, name).field,
                    getattr(cls, name).other_class,
                    getattr(cls, name).backref,
                )
                for name, col in map(lambda x: (x, getattr(cls, x)), dir(cls))
                if isinstance(getattr(cls, name), relationship)
            ]
            for name, field, other_class_table_name, backref in relations:
                other_cls = [
                    cls
                    for cls in cls_list
                    if cls.__tablename__ == other_class_table_name
                ][0]

                def getter1(obj, name=name):
                    return other_cls.get_by_id(self.get_value(cls, obj.id, field))

                def getter2(obj, name=backref):
                    return self.query(cls, **{field: obj.id})

                setattr(cls, name, property(getter1))
                setattr(other_cls, backref, property(getter2))

    def add_empty_row(self, cls):
        tablename = cls.__tablename__
        # add row filled with cls.defaults
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        keys = []
        values = []
        for key, val in cls.defaults.items():
            keys.append(key)
            values.append(val)
        cur.execute(
            f"INSERT INTO {tablename} ({','.join(keys)}) VALUES ({','.join(['?'] * len(values))})",
            values,
        )
        id = cur.lastrowid
        conn.commit()
        conn.close()

        return id

    def set_value(self, cls, obj_id, col_name, value):
        tablename = cls.__tablename__
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(
            f"UPDATE {tablename} SET {col_name} = ? WHERE id = ?",
            (value, obj_id),
        )
        conn.commit()
        conn.close()

    def get_value(self, cls, obj_id, col_name):
        tablename = cls.__tablename__
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(f"SELECT {col_name} FROM {tablename} WHERE id = ?", (obj_id,))
        return cur.fetchone()[0]

    def query(self, cls, **kwargs):
        tablename = cls.__tablename__
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        keys = []
        values = []
        for key, val in kwargs.items():
            keys.append(key)
            values.append(val)
        cur.execute(
            f"SELECT * FROM {tablename} WHERE {keys[0]} = ?",
            values,
        )
        result = []
        for row in cur.fetchall():
            result.append(cls.get_by_id(row[0]))
        conn.close()
        return result
