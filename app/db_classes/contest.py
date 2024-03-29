from app.imports import *
from app.sqlalchemy_custom_types import *


class Contest(db.Model):
    # --> INITIALIZE
    __tablename__ = "contest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=False)
    rating = db.Column(db.String, default="public") # 'public' | 'private'
    total_likes = db.Column(db.Integer, default=0)

    # --> RELATIONS
    contest_problems = db.relationship("Contest_Problem", backref="contest")
    contest_judges = db.relationship("Contest_Judge", backref="contest")
    contest_users = db.relationship("Contest_User", backref="contest")
    club_contests = db.relationship("Club_Contest", backref="contest")
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    # --> FUNCTIONS
    def is_liked(self):
        from app.dbc import Like
        return Like.query.filter_by(parent_type="Contest", parent_id=self.id, user_id=current_user.id).first() is not None

    def act_add_like(self):
        if self.is_liked():
            return
        from app.dbc import Like
        Like(parent_type="Contest", parent_id=self.id, user_id=current_user.id).add()
        return
    
    def act_remove_like(self):
        if not self.is_liked():
            return
        from app.dbc import Like
        Like.query.filter_by(parent_type="Contest", parent_id=self.id, user_id=current_user.id).remove()
        return

    def is_rating_public(self):
        return self.rating == "public"
    def is_rating_private(self):
        return self.rating == "private"
    def is_archived(self):
        return self.is_public

    def is_description_available(self, user=current_user):
        if user is None:
            return False
        return self.is_public or self.is_my(user)

    def is_my(self, user=current_user):
        if user is None:
            return False
        return user.is_pool_access(self.pool_id)

    def is_started(self):
        return self.start_date <= current_time()

    def is_ended(self):
        return self.end_date <= current_time()
    
    def is_rating_available(self, user=current_user):
        return (user.is_judge(self) or self.is_rating_public())
    
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
        if self.is_ended() or current_user.is_judge(self) or self.get_active_cu():
            return [cp for cp in self.contest_problems if cp.is_accessible()]
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
    
    def get_cu_by_mode_and_part(self, mode="all", part="real", user=current_user, club=None):
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
            tr[0] = cu # Contest_User object
            tr[1] = cu.get_total_score() # Total score
            tr[2] = [] # List of (Contest_Problem, Contest_User_Solution)
            tr[3] = -1 # User's place
            for cp in all_cp:
                cus = Contest_User_Solution.get_by_contest_problem_and_contest_user(cp, cu)
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
            if (t[i][1] == t[i - 1][1]):
                t[i][3] = t[i-1][3]
            else:
                t[i][3] = i + 1
        return t

    def act_set_name(self, name):
        self.name = name
        return self.save()
    
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
        from app.dbc import Contest_User, Contest_User_Solution

        if not self.is_archived():
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
            if (start is None) or (end is None) or (start > end) or (start < self.start_date) or (start < current_time()):
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

    def act_add_problem(self, problem, max_score=7):
        from app.dbc import Contest_Problem

        if problem is None:
            return self
        if not self.is_my():
            return self
        if problem.is_in_contest(self):
            return self
        cp = Contest_Problem(contest_id=self.id, problem_id=problem.id).add()
        cp.act_set_max_score(max_score)
        return self

    def act_add_problem_by_hashed_id(self, hashed_id, max_score=7):
        from app.dbc import Problem

        return self.act_add_problem(Problem.get_by_hashed_id(hashed_id), max_score)

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
            self.act_add_problem_by_hashed_id(hashes[i], scores[i])
        for i in range(len(hashes)):
            self.act_set_problem_score_by_hashed_id(hashes[i], scores[i])
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
    def get_by_id(id):
        return Contest.query.filter_by(id=id).first()

    @staticmethod
    def get_by_hashed_id(hashed_id):
        return Contest.query.filter_by(hashed_id=hashed_id).first()

    @staticmethod
    def get_all_by_pool(pool):
        return Contest.query.filter_by(pool_id=pool.id).all()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

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

    def save(self):
        db.session.commit()
        return self

    # TAGS BLOCK

    def get_tags(self):
        from app.dbc import Tag, Tag_Relation

        return sorted(
            [
                Tag.query.filter_by(id=sheet_tag.tag_id).first()
                for sheet_tag in Tag_Relation.query.filter_by(
                    parent_type=DbParent.fromType(type(self)), parent_id=self.id
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
    
    def act_add_tag(self, tag):
        from app.dbc import Tag_Relation

        if tag is None:
            return self
        if not self.is_my():
            return self
        if self.is_have_tag(tag):
            return self
        Tag_Relation(
            parent_type=DbParent.fromType(type(self)), parent_id=self.id, tag_id=tag.id
        ).add()
        return self

    def act_add_tag_by_name(self, tag_name):
        from app.dbc import Tag
        tag = Tag.get_by_name(tag_name)
        if tag is None:
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
    