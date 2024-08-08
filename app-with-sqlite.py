
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Clarusway_1@seymanur-mydbinstance.c9gc8sa2ih1i.us-east-1.rds.amazonaws.com:3306/clarusway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(name='Alice', email='alice@example.com'),
        User(name='Bob', email='bob@example.com'),
        User(name='Charlie', email='charlie@example.com')
    ]

    db.session.add_all(users)
    db.session.commit()

def find_emails(keyword):
    return User.query.filter(User.email.contains(keyword)).all()

def insert_email(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = find_emails(keyword)
        return render_template('emails.html', results=results)
    return render_template('emails.html')

@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        insert_email(name, email)
        return 'Email added successfully'
    return render_template('add-email.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
