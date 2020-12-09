from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)

db.create_all()
db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/survey')
def survey():
    questions = Questions.query.all()
    return render_template(
        "survey.html",
        questions=questions
    )

@app.route('/process', methods=['get'])
def answer_process():
    age = request.args.get('age')
    user = User(
        age=age,
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    q1 = request.args.get('q1')

    answer = Answers(id=user.id, q1=q1)
    db.session.add(answer)
    db.session.commit()

    return render_template("index.html")

@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q1_mean'] = db.session.query(func.avg(Answers.q1)).one()[0]
    q1_answers = db.session.query(Answers.q1).all()
    return render_template('stats.html', all_info=all_info)

if __name__ == "__main__":
    app.run(debug=False, port=8888)