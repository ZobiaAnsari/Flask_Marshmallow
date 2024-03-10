from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Student'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    address = db.Column(db.String(30))


class StuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student


@app.route('/data', methods = ['POST'])

def info():
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        address = request.json['address']
        new_user = Student(name = name, email = email, address = address)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg':'data inserted'})
    

@app.route('/')
def index():
    users_schema = StuSchema(many=True)
    users=Student.query.all()
    output = users_schema.dump(users)
    return jsonify({'user':output})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

