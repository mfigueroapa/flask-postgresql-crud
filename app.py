from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db = SQLAlchemy(app)
CORS(app)


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(255))

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.name, self.age)


@app.route('/')
def index():
    return jsonify({
        'status': 'Server running! :D',
    })


# Create user and insert to db
@app.route('/create', methods=['POST'])
def create():
    body = request.json
    name = body['name']
    age = body['age']

    create = User(name, age)
    db.session.add(create)
    db.session.commit()

    return jsonify({
        'status': 'User inserted to db!',
        'name': name,
        'age': age
    })


# Get data from db
@app.route('/data', methods=['GET'])
def data():
    data = User.query.order_by(User.id).all()
    jsonData = []
    for i in range(len(data)):
        formattedData = {
            'id': str(data[i]).split('/')[0],
            'name': str(data[i]).split('/')[1],
            'age': str(data[i]).split('/')[2]
        }
        jsonData.append(formattedData)
    return jsonify(jsonData)


# Find user by id
@app.route('/data/<string:id>', methods=['GET'])
def findOne(id):
    data = User.query.get(id)
    formattedData = {
        'id': str(data).split('/')[0],
        'name': str(data).split('/')[1],
        'age': str(data).split('/')[2]
    }
    return jsonify(formattedData)


# Delete by id
@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    data = User.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    formattedData = {
        'id': str(data).split('/')[0],
        'name': str(data).split('/')[1],
        'age': str(data).split('/')[2]
    }
    return jsonify({'status': 'User with id: ' + id + ' was deleted from db.', "user": formattedData})


# Update by id
@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    body = request.json
    newName = body['name']
    newAge = body['age']
    updateData = User.query.filter_by(id=id).first()
    updateData.name = newName
    updateData.age = newAge
    updatedUser = User.query.filter_by(id=id).first()
    formattedData = {
        'id': str(updatedUser).split('/')[0],
        'name': str(updatedUser).split('/')[1],
        'age': str(updatedUser).split('/')[2]
    }
    db.session.commit()
    return jsonify({'status': 'User with id ' + id + ' was updated!', "user": formattedData})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
