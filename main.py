from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

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
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route('/location/<loc>', methods=["POST", "GET"] )
def find_cafe(loc):
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all() #the list has been made
    cafe_in_loc_list = []

    for cafe in all_cafes:
        if cafe.location == loc:
            cafe_in_loc_list.append(cafe)

    if len(cafe_in_loc_list) != 0:
        cafe_data_in_loc_list = []
        for cafe in cafe_in_loc_list:
            cafe_data_json = cafe.to_dict()
            cafe_data_in_loc_list.append(cafe_data_json)
        return jsonify(cafe=cafe_data_in_loc_list)
        
    else:
        return jsonify(error={
            "Not Found" : "Sorry, We dont have a Cafe at that location"
        })

@app.route('/suggest', methods=["POST", "GET"])
def add_cafe():
    new_cafe = Cafe(
        name = request.form.get("cafe_name_input"),
        map_url = request.form.get("url_name_input"),
        img_url = request.form.get("img_url"),
        location = request.form.get("location"),
        seats = request.form.get("seats"),
        has_toilet = int(request.form.get("has_toilet")),
        has_wifi = int(request.form.get("has_wifi")),
        has_sockets = int(request.form.get("has_sockets")),
        can_take_calls = int(request.form.get("can_take_calls")),
        coffee_price = request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

if __name__ == '__main__':
    app.run(debug=True)
