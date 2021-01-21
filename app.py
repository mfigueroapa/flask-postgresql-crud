from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db = SQLAlchemy(app)
CORS(app)


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


if __name__ == '__main__':
    app.run(debug=True, port=5002)