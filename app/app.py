"""Main Flask APP file"""

from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init flask app
app = Flask(__name__)

# set configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# create todo table
class Todo(db.Model):
    """Todo model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Todo('{self.id}')"

# create todo schema
class TodoSchema(ma.Schema):
    """Todo schema"""
    class Meta:
        fields = ('id', 'title', 'description', 'completed', 'date_created')

# init schema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


# create todo
@app.route('/todo', methods=['POST'])
def add_todo():
    """Add a todo"""
    try:
        title = request.json['title']
        description = request.json['description']

        todo = Todo(title=title, description=description)

        db.session.add(todo)
        db.session.commit()

        return todo_schema.jsonify(todo)
    except Exception as e:
        return jsonify({"error": str(e)})


# get all todos
@app.route('/todo', methods=['GET'])
def get_todos():
    """Get all todos"""
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)


# get a todo
@app.route('/todo/<int:id>', methods=['GET'])
def get_todo(id):
    """Get a todo"""
    todo = Todo.query.get_or_404(id)
    return todo_schema.jsonify(todo)


if __name__ == '__main__':
    app.run(debug=True)