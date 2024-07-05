#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
# from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
# CORS(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route('/restaurants',methods=['GET'])
def restaurants():
    if request.method =='GET':
        restaurants= Restaurant.query.all()
        res_dict=[restaurant.to_dict(rules=['-restaurant_pizzas']) for restaurant in restaurants]
        response = make_response(jsonify(res_dict),200)
        return response
    

@app.route('/restaurants/<int:id>',methods=['GET','DELETE'])
def restaurant_by_id(id):
    if request.method == 'GET':
        restaurant = Restaurant.query.filter(id == Restaurant.id).first()
        if restaurant:
            res_dict = restaurant.to_dict()
            response =make_response(res_dict,200)
            return response
        else:
            response = make_response(jsonify({"error": "Restaurant not found"}),404)

        return response
    if request.method =='DELETE':
        restaurant  = Restaurant.query.filter(id == Restaurant.id).first()
        db.session.delete(restaurant)
        db.session.commit()
        res =restaurant.to_dict()
        response=make_response(jsonify(res),204)
        return response
    

@app.route('/pizzas',methods=['GET'])
def pizzas():
    pizzas =Pizza.query.all()
    pizzas_dict= [pizza.to_dict(rules=['-restaurant_pizzas'])for pizza in pizzas]
    response= make_response(jsonify(pizzas_dict),200)
    return response

@app.route('/restaurant_pizzas',methods=['GET','POST'])
def restaurant_pizzas():
        try: 
            if request.method == 'POST': 
                data =request.get_json()
                price = data.get('price')
                pizza_id = data.get('pizza_id')
                restaurant_id =data.get('restaurant_id')
        # pizza = Pizza.query.get(pizza_id)
        # restaurant = Restaurant.query.get(restaurant_id)
    
            new_res_piz = RestaurantPizza(
                        price = price,
                        pizza_id = pizza_id,
                        restaurant_id = restaurant_id,
            )
            db.session.add(new_res_piz)
            db.session.commit()
        
            res_piz_dict = new_res_piz.to_dict()
            

            response = make_response(jsonify(res_piz_dict),201)
            return response
        except: 
            msg = {"errors": ["validation errors"]}
            
            return (msg,400)
    

# @app.route('/restaurant_pizzas', methods=['POST'])
# def restaurant_pizzas():
#     # Extract data from request
#     price = request.form.get('price')
#     pizza_id = request.form.get('pizza_id')
#     restaurant_id = request.form.get('restaurant_id')
    
#     # Validate inputs
#     if not (price and pizza_id and restaurant_id):
#         # If any required field is missing
#         msg = {"errors": ["validation errors"]}
#         return jsonify(msg), 400
    
#     # Convert IDs to integers
#     try:
#         pizza_id = int(pizza_id)
#         restaurant_id = int(restaurant_id)
#     except ValueError:
#         msg = {"errors": ["Invalid pizza_id or restaurant_id format"]}
#         return jsonify(msg), 400
    
#     # Check if Pizza and Restaurant exist
#     pizza = Pizza.query.get(pizza_id)
#     restaurant = Restaurant.query.get(restaurant_id)
    
#     if not (pizza and restaurant):
#         msg = {"errors": ["Pizza or Restaurant not found"]}
#         return jsonify(msg), 404
    
#     # Create new RestaurantPizza
#     new_res_piz = RestaurantPizza(
#         price=price,
#         pizza_id=pizza_id,
#         restaurant_id=restaurant_id
#     )
    
#     # Add and commit to database
#     db.session.add(new_res_piz)
#     db.session.commit()
    
#     # Prepare response data
#     res_piz_dict = {
#         "id": new_res_piz.id,
#         "price": new_res_piz.price,
#         "pizza": pizza.to_dict(),
#         "pizza_id": new_res_piz.pizza_id,
#         "restaurant": restaurant.to_dict(),
#         "restaurant_id": new_res_piz.restaurant_id
#     }
    
#     # Return successful response with status code 201
#     response = make_response(jsonify(res_piz_dict), 201)
#     return response



if __name__ == "__main__":
    app.run(port=5555, debug=True)