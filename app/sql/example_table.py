from app.sql.db_column_types import Int, String, relationship


class ExampleTable:
    __tablename__ = "example_table"

    some_int = Int(default=0)
    text = String(default="hello")


class OtherTable:
    __tablename__ = "other_table"

    some_int = Int(default=0)
    text = String(default="hello")

    example_table_id = Int(default=None)
    example_table = relationship(
        example_table_id, "example_table", backref="other_tables"
    )
