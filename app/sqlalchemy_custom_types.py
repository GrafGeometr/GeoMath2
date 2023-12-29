from sqlalchemy import TypeDecorator, String


# from app.dbc import Problem, Sheet, Contest, Contest_User_Solution


class Role:
    def __init__(self, name):
        self.name = name

    def __eq__(self, object):
        return self.name == object.name

    def is_owner(self):
        return self.name == Owner.name

    def set_owner(self):
        self.name = Owner.name

    def is_participant(self):
        return self.name == Participant.name

    def set_participant(self):
        self.name = Participant.name

    def is_invited(self):
        return self.name == Invited.name

    def set_invited(self):
        self.name = Invited.name


Owner = Role("Owner")
Participant = Role("Participant")
Invited = Role("Invited")
Null_Role = Role("NullRole")


class RoleType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return value.name

    def process_result_value(self, value, dialect):
        return Role(value)


class DbParent:
    def __init__(self, name):
        self.name = name

    def __eq__(self, object):
        return self.name == object.name

    def to_type(self):
        from app.dbc import Contest, Problem, Sheet, ContestUserSolution, Pool, Club

        return {
            "Contest": Contest,
            "Problem": Problem,
            "Sheet": Sheet,
            "Contest_User_Solution": ContestUserSolution,
            "Pool": Pool,
            "Club": Club,
        }.get(self.name, None)

    @staticmethod
    def from_type(type):
        from app.dbc import Contest, Problem, Sheet, ContestUserSolution, Pool, Club

        return DbParent(
            {
                Contest: "Contest",
                Problem: "Problem",
                Sheet: "Sheet",
                ContestUserSolution: "Contest_User_Solution",
                Pool: "Pool",
                Club: "Club",
            }.get(type, None)
        )


class DbParentType(TypeDecorator):
    cache_ok = False

    impl = String

    def process_bind_param(self, value, dialect):
        return value.name

    def process_result_value(self, value, dialect):
        return DbParent(value)


class Grade:
    def __init__(self, name):
        self.name = name

    def __eq__(self, object):
        return self.name == object.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_grades_list(self):
        for grades_list in list_of_grades_lists:
            if self in grades_list:
                return grades_list

    def are_same_grades_types(self, other):
        return self.get_grades_list() == other.get_grades_list()

    def __lt__(self, other):
        if not self.are_same_grades_types(other):
            pass  # TODO raise something
        return self.get_grades_list().index(self) < other.get_grades_list().index(other)

    def __le__(self, other):
        if not self.are_same_grades_types(other):
            pass  # TODO raise something
        return self.get_grades_list().index(self) <= other.get_grades_list().index(
            other
        )


School_Grades_list = [
    Sixth_Grade,
    Seventh_Grade,
    Eighth_Grade,
    Ninth_Grade,
    Tenth_Grade,
    Eleventh_Grade,
] = list(
    map(
        Grade,
        ["6 класс", "7 класс", "8 класс", "9 класс", "10 класс", "11 класс"],
    )
)

IGO_Grades_list = [Beginner, Intermediate, Advanced] = list(
    map(Grade, ["Начинающие", "Продолжающие", "Профессионалы"])
)

list_of_grades_lists = [School_Grades_list, IGO_Grades_list]


class GradeClassType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return value.name

    def process_result_value(self, value, dialect):
        return Grade(value)
