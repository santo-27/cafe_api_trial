from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(cafe):
        inner_dict = {
            "can_take_calls" : cafe.can_take_calls,
            "coffee_price" : cafe.coffee_price,
            "has_sockets" : cafe.has_sockets,
            "has_toilet" : cafe.has_toilet,
            "has_wifi" : cafe.has_wifi,
            "id" : cafe.id,
            "img_url" : cafe.img_url,
            "location" : cafe.location,
            "map_url" : cafe.map_url,
            "name" : cafe.name,
            "seats" : cafe.seats
        }
        return inner_dict


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

@app.route('/random', methods=["GET"])
def random_cafe():
    if request.method == "GET":
        # index = random.randint(0, 21)
        # random_cafe_name = db.get_or_404(name, id)
        result = db.session.execute(db.select(Cafe))
        all_cafes = result.scalars().all()
        random_cafe = random.choice(all_cafes)
        inner_dict = {
            "can_take_calls" : random_cafe.can_take_calls,
            "coffee_price" : random_cafe.coffee_price,
            "has_sockets" : random_cafe.has_sockets,
            "has_toilet" : random_cafe.has_toilet,
            "has_wifi" : random_cafe.has_wifi,
            "id" : random_cafe.id,
            "img_url" : random_cafe.img_url,
            "location" : random_cafe.location,
            "map_url" : random_cafe.map_url,
            "name" : random_cafe.name,
            "seats" : random_cafe.seats
        }
        return jsonify(cafe=inner_dict)
        
@app.route('/all', methods=['GET'])
def show_all_cafes():
    # result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    # all_cafes = result.scalars().all()
    # all_cafes_list = []
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    #This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    for cafe in all_cafes:
        # inner_dict = {
        #     "can_take_calls" : cafe.can_take_calls,
        #     "coffee_price" : cafe.coffee_price,
        #     "has_sockets" : cafe.has_sockets,
        #     "has_toilet" : cafe.has_toilet,
        #     "has_wifi" : cafe.has_wifi,
        #     "id" : cafe.id,
        #     "img_url" : cafe.img_url,
        #     "location" : cafe.location,
        #     "map_url" : cafe.map_url,
        #     "name" : cafe.name,
        #     "seats" : cafe.seats
        # }
        inner_dict = cafe.to_dict()
        all_cafes_list.append(inner_dict)
    return jsonify(cafes=all_cafes_list)






## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
