from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import APIAccess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CLASS_COLORS = ["#FF5733", "#33FF57", "#3357FF", "#FFC300", "#C70039", "#900C3F", "#581845"]


# Assignment Model
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

def get_canvas_assignments():
    """
    Fetch assignments from Canvas using APIAccess and store them in the database.
    """
    canvas_assignments = APIAccess.get_assignments()  # Modify this with your actual function

    for class_id, assignments_list in canvas_assignments.items():
        for assignment_name, due_date in assignments_list:
            # Convert date from ISO format
            formatted_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%SZ")

            # Check if assignment already exists
            existing = Assignment.query.filter_by(title=assignment_name, due_date=formatted_date).first()
            if not existing:
                new_assignment = Assignment(title=assignment_name, due_date=formatted_date, class_id=class_id)
                db.session.add(new_assignment)

    db.session.commit()
    return {'message': 'Canvas assignments synced successfully!'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sync_canvas', methods=['GET'])
def sync_canvas():
    """
    Trigger Canvas assignment fetch and store data.
    """
    result = get_canvas_assignments()
    return jsonify(result)

@app.route('/get_assignments')
def get_assignments():
    assignments = Assignment.query.all()
    formatted_events = []

    for a in assignments:
        color = CLASS_COLORS[a.class_id % len(CLASS_COLORS)]  # Assign consistent color
        formatted_events.append({
            'id': a.id,
            'title': a.title,
            'start': a.due_date.strftime('%Y-%m-%d'),
            'color': color
        })

    return jsonify(formatted_events)


@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    data = request.json
    new_assignment = Assignment(title=data['title'], due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'))
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
