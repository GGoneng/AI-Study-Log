# -----------------------------------------------------
# 데이터베이스의 테이블 정의 클래스
# -----------------------------------------------------
from DBWEB import DB

# -----------------------------------------------------
# Question 테이블 정의 클래스
# -----------------------------------------------------

class Question(DB.Model):
    # 컬럼 정의
    id = DB.Column(DB.Integer, primary_key = True)
    subject = DB.Column(DB.String(200), nullable = False)
    content = DB.Column(DB.Text(), nullable = False)
    create_date = DB.Column(DB.DateTime(), nullable = False)

class Answer(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    question_id = DB.Column(DB.Integer,
                            DB.ForeignKey('question.id', ondelete = 'CASCADE'))
    question = DB.relationship('Question', backref = DB.backref('answer_set', ))
    content = DB.Column(DB.Text(), nullable = False)
    create_date = DB.Column(DB.DateTime(), nullable = False)
