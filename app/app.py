"""Main Flask APP file"""

from datetime import datetime

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


# init flask app
app = Flask(__name__)

# allow cross origin requests
CORS(app)

# set configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swagger UI
SWAGGER_URL = '/swagger'    
API_URL = '/static/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Todo API"
    })

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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

# error handler
@app.errorhandler(404)
def not_found(error):
    """Error handler"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    """Error handler"""
    return make_response(jsonify({'error': 'Internal server error'}), 500)

@app.errorhandler(400)
def bad_request(error):
    """Error handler"""
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    """Error handler"""
    return make_response(jsonify({'error': 'Unauthorized'}), 401)





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

        return todo_schema.jsonify(todo), 201
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


# update a todo
@app.route('/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    """Update a todo"""
    try:
        todo = Todo.query.get_or_404(id)

        title = request.json['title']
        description = request.json['description']
        completed = request.json['completed']

        todo.title = title
        todo.description = description
        todo.completed = completed

        db.session.commit()

        return todo_schema.jsonify(todo)
    except Exception as e:
        return jsonify({"error": str(e)})


# delete a todo
@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """Delete a todo"""
    try:
        todo = Todo.query.get_or_404(id)

        db.session.delete(todo)
        db.session.commit()

        return todo_schema.jsonify(todo)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)