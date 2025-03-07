from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Assignment Model
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_assignments')
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([
        {'id': a.id, 'title': a.title, 'start': a.due_date.strftime('%Y-%m-%d')}
        for a in assignments
    ])

@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    data = request.json
    new_assignment = Assignment(title=data['title'], due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'))
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
