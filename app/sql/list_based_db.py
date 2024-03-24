from app.sql.abstract_db import AbstractDB
from app.sql.db_column_types import DBColumn, relationship


class ListBasedDB(AbstractDB):
    def __init__(self):
        self.table = {}  # self.table[cls.__tablename__][obj_id][col_name] = value

    def add_tables(self, *cls_list):
        for cls in cls_list:
            self.table[cls.__tablename__] = []

            properties = [
                (name, getattr(cls, name))
                for name in dir(cls)
                if isinstance(getattr(cls, name), DBColumn)
            ]

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
        self.table[cls.__tablename__].append({})
        return len(self.table[cls.__tablename__]) - 1

    def set_value(self, cls, obj_id, col_name, value):
        self.table[cls.__tablename__][obj_id][col_name] = value

    def get_value(self, cls, obj_id, col_name):
        return self.table[cls.__tablename__][obj_id].get(
            col_name, cls.defaults[col_name]
        )

    def query(self, cls, **kwargs):
        result = []
        for obj_id, row in enumerate(self.table[cls.__tablename__]):
            for key, value in kwargs.items():
                if row.get(key) != value:
                    break
            else:
                result.append(cls.get_by_id(id=obj_id))

        return result
