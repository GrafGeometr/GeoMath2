from abc import ABC, abstractmethod

from app.sql.db_column_types import DBColumn


class AbstractDB(ABC):
    @abstractmethod
    def add_tables(self, cls):
        pass

    @abstractmethod
    def set_value(self, cls, obj_id, col_name, value):
        pass

    @abstractmethod
    def get_value(self, cls, obj_id, col_name):
        pass

    @abstractmethod
    def add_empty_row(self, cls):
        pass

    @abstractmethod
    def query(self, cls, **kwargs):
        pass


