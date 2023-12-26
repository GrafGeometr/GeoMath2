from app.imports import *
from sqlalchemy_custom_types import *

from app.db_classes.standard_model.normal import StandardModel
from .abstract import AbstractContest
from .null import NullContest
from .getter import ContestGetter


class Contest(ModelWithName):
    # --> INITIALIZE
    __tablename__ = "contest"

    null_cls_ = NullContest
    getter_cls_ = ContestGetter

    description_ = db.Column(db.String)
    grade_ = db.Column(GradeClassType)
    start_date_ = db.Column(db.DateTime)
    end_date_ = db.Column(db.DateTime)
    is_public_ = db.Column(db.Boolean, default=False)
    rating_ = db.Column(db.String, default="public")  # 'public' | 'private'
    total_likes_ = db.Column(db.Integer, default=0)
    total_dislikes_ = db.Column(db.Integer, default=0)

    # --> RELATIONS
    contest_problems_ = db.relationship("Contest_Problem", backref="contest_")
    contest_judges_ = db.relationship("Contest_Judge", backref="contest_")
    contest_users_ = db.relationship("Contest_User", backref="contest_")
    club_contests_ = db.relationship("Club_Contest", backref="contest_")
    pool_id_ = db.Column(db.Integer, db.ForeignKey("pool.id_"))
    olimpiad_id_ = db.Column(db.Integer, db.ForeignKey("olimpiad.id_"))

    # --> PROPERTIES
    @property
    def description(self) -> str:
        return self.description_ 

    @description.setter
    def description(self, description: str):
        self.description_ = description
        self.save()

    @property
    def grade(self) -> GradeClassType:
        return self.grade_

    @grade.setter
    def grade(self, grade: GradeClassType):
        self.grade_ = grade
        self.save()

    @property
    def start_date(self) -> datetime.datetime:
        return self.start_date_

    @start_date.setter
    def start_date(self, start_date: datetime.datetime):
        self.start_date_ = start_date
        self.save()

    @property
    def end_date(self) -> datetime.datetime:
        return self.end_date_

    @end_date.setter
    def end_date(self, end_date: datetime.datetime):
        self.end_date_ = end_date
        self.save()

    @property
    def is_public(self) -> bool:
        return self.is_public_

    @is_public.setter
    def is_public(self, is_public: bool):
        self.is_public_ = is_public
        self.save()

    @property
    def rating(self) -> str:
        return self.rating_

    @rating.setter
    def rating(self, rating: str):
        self.rating_ = rating
        self.save()

    @property
    def total_likes(self) -> int:
        return self.total_likes_

    @total_likes.setter
    def total_likes(self, total_likes: int):
        self.total_likes_ = total_likes
        self.save()

    @property
    def total_dislikes(self) -> int:
        return self.total_dislikes_

    @total_dislikes.setter
    def total_dislikes(self, total_dislikes: int):
        self.total_dislikes_ = total_dislikes
        self.save()
    
    @property
    def contest_problems(self) -> list("ContestToProblemRelation"):
        return self.contest_problems_

    @contest_problems.setter
    def contest_problems(self, contest_problems: list["ContestToProblemRelation"]):
        self.contest_problems_ = contest_problems
        self.save()

    @property
    def contest_judges(self) -> list("ContestToJudgeRelation"):
        return self.contest_judges_

    @contest_judges.setter
    def contest_judges(self, contest_judges: list["ContestToJudgeRelation"]):
        self.contest_judges_ = contest_judges
        self.save()

    @property
    def contest_users(self) -> list("ContestToUserRelation"):
        return self.contest_users_

    @contest_users.setter
    def contest_users(self, contest_users: list["ContestToUserRelation"]):
        self.contest_users_ = contest_users
        self.save()

    @property
    def club_contests(self) -> list["ClubToContestRelation"]:
        return self.club_contests_

    @club_contests.setter
    def club_contests(self, club_contests: list["ClubToContestRelation"]):
        self.club_contests_ = club_contests
        self.save()

    @property
    def pool_id(self) -> int:
        return self.pool_id_

    @pool_id.setter
    def pool_id(self, pool_id: int):
        self.pool_id_ = pool_id
        self.save()

    @property
    def olimpiad_id(self) -> int:
        return self.olimpiad_id_

    @olimpiad_id.setter
    def olimpiad_id(self, olimpiad_id: int):
        self.olimpiad_id_ = olimpiad_id
        self.save()

    # --> FUNCTIONS
    @staticmethod
    def get_by_olimpiad_season_and_grade(olimpiad_id: int, season: str, grade: Grade):
        return Contest.query.filter_by(
            olimpiad_id=olimpiad_id, season=season, grade=grade
        ).first()

    def is_liked(self):
        from app.dbc import Like

        return (
                Like.query.filter_by(
                    parent_type="Contest", parent_id=self.id, user_id=current_user.id
                ).first()
                is not None
        )

    def act_add_like(self):
        if self.is_liked():
            return
        from app.dbc import Like

        Like(parent_type="Contest", parent_id=self.id, user_id=current_user.id).add()
        return self

    def act_remove_like(self):
        if not self.is_liked():
            return
        from app.dbc import Like

        Like.query.filter_by(
            parent_type="Contest", parent_id=self.id, user_id=current_user.id
        ).remove()
        return self

    def act_make_non_public(self):
        self.is_public = False
        return self.save()

    def act_make_public(self):
        self.is_public = True
        return self.save()

    def is_rating_public(self):
        return self.rating == "public"

    def is_rating_private(self):
        return self.rating == "private"

    def is_archived(self):
        return self.is_public

    def is_description_available(self, user=current_user):
        if user is None:
            return False
        if (self.is_public) or (self.is_my(user)):
            return True
        from app.dbc import User_Club

        all_cc = [cc for cc in self.club_contests if cc.is_valid()]
        my_clubs = [uc.club for uc in User_Club.query.filter_by(user=user).all()]
        return any(cc.club in my_clubs for cc in all_cc)

    def is_my(self, user=current_user):
        if user is None:
            return False
        return user.is_pool_access(self.pool_id)

    def is_started(self):
        return (self.start_date is None) or self.start_date <= current_time()

    def is_ended(self):
        return (self.end_date is None) or self.end_date <= current_time()

    def is_rating_available(self, user=current_user):
        return user.is_judge(self) or self.is_rating_public()

    def is_problem_submitted(self, problem):
        from app.dbc import Contest_Problem, Contest_User_Solution

        if problem is None:
            return False
        cu = self.get_active_cu()
        if cu is None:
            return False
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is None:
            return False
        cus = Contest_User_Solution.get_by_contest_problem_and_contest_user(cp, cu)
        return (cus is not None) and (cus.content is not None)

    def is_tags_available(self, user=current_user):
        return self.is_description_available(user)

    def get_all_likes(self):
        from app.dbc import Like

        return Like.get_all_by_parent(self)

    def get_all_likes_good(self):
        return [like for like in self.get_all_likes() if like.good]

    def get_all_likes_bad(self):
        return [like for like in self.get_all_likes() if not like.good]

    def get_problems(self):
        from app.dbc import Problem, Contest_Problem

        result = list(
            filter(
                lambda x: x is not None,
                [
                    Problem.get_by_id(id=cp.problem_id)
                    for cp in Contest_Problem.get_all_by_contest(self)
                ],
            )
        )
        return result

    def get_judges(self):
        return [
            cj.user
            for cj in self.contest_judges
            if cj is not None and cj.user is not None
        ]

    def get_nonsecret_contest_problems(self):
        from app.dbc import Contest_Problem

        if (
                self.is_ended()
                or self.is_my()
                or current_user.is_judge(self)
                or self.get_active_cu()
        ):
            return [
                cp
                for cp in Contest_Problem.get_all_by_contest(self)
                if cp.is_accessible()
            ]
        else:
            return []

    def get_nonsecret_problems(self):
        return [cp.problem for cp in self.get_nonsecret_contest_problems()]

    def get_active_cu(self, user=current_user):
        from app.dbc import Contest_User

        return Contest_User.get_active_by_contest_and_user(self, user)

    def get_idx_by_contest_problem(self, contest_problem):
        cproblems = self.get_nonsecret_contest_problems()
        if contest_problem not in cproblems:
            return None
        return cproblems.index(contest_problem) + 1

    def get_cu_by_mode_and_part(
            self, mode="all", part="real", user=current_user, club=None
    ):
        if mode not in ["all", "my", "club"]:
            return None
        if part not in ["real", "virtual"]:
            return None
        all_cu = [cu for cu in self.contest_users if cu.is_any_cus_available(user)]

        if mode == "all":
            all_cu = all_cu
        elif mode == "my":
            all_cu = [cu for cu in all_cu if cu.user.id == user.id]
        elif mode == "club":
            all_cu = [cu for cu in all_cu if cu.user.get_club_relation(club.id)]

        if part == "real":
            all_cu = [cu for cu in all_cu if (not cu.virtual)]
        elif part == "virtual":
            all_cu = [cu for cu in all_cu if (cu.virtual)]
        return all_cu

    def get_rating_table(self, all_cu):
        from app.dbc import Contest_User_Solution

        t = []
        all_cp = self.get_nonsecret_contest_problems()
        for cu in all_cu:
            tr = [None, None, None, None]
            tr[0] = cu  # Contest_User object
            tr[1] = cu.get_total_score()  # Total score
            tr[2] = []  # List of (Contest_Problem, Contest_User_Solution)
            tr[3] = -1  # User's place
            for cp in all_cp:
                cus = Contest_User_Solution.get_by_contest_problem_and_contest_user(
                    cp, cu
                )
                print(cus)
                tr[2].append((cp, cus))
            t.append(tr)
        if self.is_rating_available():
            t.sort(key=lambda x: x[1], reverse=True)
        else:
            t.sort(key=lambda x: x[0].user.name)
        if len(t) == 0:
            return t
        t[0][3] = 1
        for i in range(1, len(t)):
            if t[i][1] == t[i - 1][1]:
                t[i][3] = t[i - 1][3]
            else:
                t[i][3] = i + 1
        return t

    def act_set_description(self, description):
        self.description = description
        return self.save()

    def act_set_date(self, start_date, end_date):
        if start_date is None or end_date is None or start_date > end_date:
            return self
        self.start_date = start_date
        self.end_date = end_date
        return self.save()

    def act_register(
            self, user=current_user, mode="real", start_date=None, end_date=None
    ):
        if user is None:
            return
        print(mode, start_date, end_date)
        # регистрация user на контест, если виртуально - то с указанием начала и завершения
        # mode = "real" / "virtual", start=end='%Y-%m-%dT%H:%M' (строка в таком формате, надо преобразовать в datetime)
        from app.dbc import Contest_User

        if not self.is_description_available():
            return
        if self.get_active_cu():
            return
        if mode == "real":
            if self.is_ended():
                return
            Contest_User(
                contest_id=self.id,
                user_id=user.id,
                start_date=self.start_date if not self.is_started() else current_time(),
                end_date=self.end_date,
                virtual=False,
            ).add()
            flash("Вы успешно зарегистрировались на контест", "success")
        else:
            start = dt_from_str(start_date)
            end = dt_from_str(end_date)
            if (
                    (start is None)
                    or (end is None)
                    or (start > end)
                    or (start < self.start_date)
                    or (start < current_time())
            ):
                return
            Contest_User(
                contest_id=self.id,
                user_id=user.id,
                start_date=start,
                end_date=end,
                virtual=True,
            ).add()
            flash("Вы успешно зарегистрировались на виртуальное участие", "success")
        return self

    def act_stop(self, user=current_user):
        if not self.is_archived():
            return self
        cu = self.get_active_cu(user)
        print(cu)
        if cu is None:
            return self
        cu.act_stop()
        return self

    def act_add_judge(self, user):
        from app.dbc import Contest_Judge

        if user is None:
            return self
        if not self.is_my(user):
            return self
        if user.is_judge(self):
            return self
        Contest_Judge(contest_id=self.id, user_id=user.id).add()
        return self

    def act_add_judge_by_name(self, name):
        from app.dbc import User

        return self.act_add_judge(User.get_by_name(name))

    def act_remove_judge(self, user):
        from app.dbc import Contest_Judge

        if user is None:
            return self
        if not self.is_my():
            return self
        cj = Contest_Judge.get_by_contest_and_user(self, user)
        if cj is not None:
            cj.remove()
        return self

    def act_remove_judge_by_name(self, name):
        from app.dbc import User

        return self.act_remove_judge(User.get_by_name(name))

    def act_set_judges(self, names):
        for judge in [
            cj.user
            for cj in self.contest_judges
            if cj is not None and cj.user is not None
        ]:
            self.act_remove_judge(judge)
        for name in names:
            self.act_add_judge_by_name(name)
        return self

    def act_remove_problem(self, problem):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is not None:
            cp.remove()
        return self

    def act_add_problem(self, problem, position=None, max_score=7):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        if problem.is_in_contest(self):
            cp = Contest_Problem.get_by_contest_and_problem(self, problem)
            cp.act_set_list_index(position)
            cp.act_set_max_score(max_score)
            return self
        cp = Contest_Problem(contest_id=self.id, problem_id=problem.id).add()
        cp.act_set_max_score(max_score)
        if position is None:
            return self
        if position > len(self.contest_problems):
            return self  # TODO write normal error handling
        cp.act_set_list_index(position)
        return self

    def act_add_problem_by_hashed_id(self, hashed_id, position=None, max_score=7):
        from app.dbc import Problem

        return self.act_add_problem(
            Problem.get_by_hashed_id(hashed_id), position, max_score
        )

    def act_set_problem_score(self, problem, score):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        if not problem.is_in_contest(self):
            return self
        cp = Contest_Problem.get_by_contest_and_problem(self, problem)
        if cp is not None:
            cp.act_set_max_score(score)
        return self

    def act_set_problem_score_by_hashed_id(self, hashed_id, score):
        from app.dbc import Problem

        return self.act_set_problem_score(Problem.get_by_hashed_id(hashed_id), score)

    def act_set_problems(self, hashes, scores):
        print(hashes, scores)
        if len(hashes) != len(scores):
            return self
        for i in range(len(hashes)):
            self.act_add_problem_by_hashed_id(
                hashes[i], i, scores[i]
            ).act_set_problem_score_by_hashed_id(hashes[i], scores[i])
        for cp in self.contest_problems:
            if cp.problem.hashed_id not in hashes:
                cp.remove()

    def act_set_rating_public(self):
        if not self.is_my():
            return
        self.rating = "public"
        db.session.commit()
        return self

    def act_set_rating_private(self):
        if not self.is_my():
            return
        self.rating = "private"
        db.session.commit()
        return self

    def act_toggle_rating(self, mode):
        if mode is None:
            return self.act_set_rating_private()
        else:
            return self.act_set_rating_public()

    @staticmethod
    def get_all_by_pool(pool):
        return Contest.query.filter_by(pool_id=pool.id).all()

    def remove(self):
        cp_s = self.contest_problems
        cu_s = self.contest_users
        cj_s = self.contest_judges
        cc_s = self.club_contests
        for cp in cp_s:
            cp.remove()
        for cj in cj_s:
            cj.remove()
        for cu in cu_s:
            cu.remove()
        for cc in cc_s:
            cc.remove()
        from app.dbc import Like

        for l in Like.get_all_by_parent(self):
            l.remove(par=self)
        db.session.delete(self)
        db.session.commit()

    # TAGS BLOCK

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation

        return sorted(
            [
                Tag.query.filter_by(id=sheet_tag.tag_id).first()
                for sheet_tag in Tag_Relation.query.filter_by(
                parent_type=DbParent.from_type(type(self)), parent_id=self.id
            ).all()
            ],
            key=lambda t: t.name.lower(),
        )

    def get_tag_names(self):
        return list(map(lambda t: t.name, self.get_tags()))

    def is_have_tag(self, tag):
        if tag is None:
            return False
        from app.dbc import Tag_Relation

        if Tag_Relation.get_by_parent_and_tag(self, tag) is None:
            return False
        return True

    def act_add_tags(self, tags):
        for tag in tags:
            self.act_add_tag(tag)
        return self

    def act_add_tag(self, tag):
        from app.dbc import Tag_Relation

        if tag is None:
            return self
        if not self.is_my():
            return self
        if self.is_have_tag(tag):
            return self
        Tag_Relation(
            parent_type=DbParent.from_type(type(self)), parent_id=self.id, tag_id=tag.id
        ).add()
        return self

    def act_add_tag_by_name(self, tag_name):
        from app.dbc import Tag

        tag = Tag.get_by_name(tag_name)
        if (tag is None) and (current_user.admin):
            tag = Tag(name=tag_name).add()
        return self.act_add_tag(tag)

    def act_remove_tag(self, tag):
        from app.dbc import Tag_Relation

        if tag is None:
            return self
        if not self.is_my():
            return self
        rel = Tag_Relation.get_by_parent_and_tag(self, tag)
        if rel is not None:
            rel.remove()
        return self

    def act_remove_tag_by_name(self, tag_name):
        from app.dbc import Tag

        return self.act_remove_tag(Tag.get_by_name(tag_name))

    def act_set_tags(self, names):
        for tag in self.get_tags():
            self.act_remove_tag(tag)
        for name in names:
            self.act_add_tag_by_name(name)
        return self
