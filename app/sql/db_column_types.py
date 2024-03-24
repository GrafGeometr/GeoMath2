class DBColumn:
    def __init__(self, default=None):
        self.default = default


class Int(DBColumn):
    def __init__(self, default=0, primary_key=False):
        super().__init__(default=default)
        self.type = "INTEGER" + (" PRIMARY KEY" if primary_key else "")


class String(DBColumn):
    def __init__(self, default=""):
        super().__init__(default=default)
        self.type = "TEXT"


class Boolean(DBColumn):
    def __init__(self, default=False):
        super().__init__(default=default)
        self.type = "BOOLEAN"


class relationship:
    def __init__(self, field, other_class, backref=None):
        self.field = field
        self.type = "INTEGER"
        self.other_class = other_class
        if backref is None:
            raise ValueError("backref must be not None")
        self.backref = backref
