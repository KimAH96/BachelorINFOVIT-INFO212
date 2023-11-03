from flask import render_template, request, redirect, url_for, Flask, jsonify
from neo4j import GraphDatabase
from my_dao import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/get_cars', methods=['GET'])
def query_records():
    return findAllCars()


@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = json.loads(request.data)
    print(record)
    print(record['reg'])
    return findCarByReg(record['reg'])


# The method uses the registration number to find the car
# object from database

@app.route('/save_car', methods=["POST"])
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'], record['status'])

# The method uses the registration number to find the car
# object from database and updates other information from
# the information provided as input in the json object


@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])


# The method uses the registration number to find the car
# object from database and removes the records
@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()


# denne metoden brukes for å registrere at en kunde lager en booking av bil
# metoden må testes. usikker på hvordan den skal lages
# @app.route('/order_car', methods=['POST', 'PUT'])
# def booking_customer():
#     record = json.loads(request.data)
#     print(record)
#     return orderCar(record['name'], record['reg'])

@app.route('/order_car', methods=['POST', 'PUT'])
def booking_customer():
    record = json.loads(request.data)
    print(record)
    print(orderCar(record['name'], record['reg']))
    return jsonify({"Message":"Test"})


# Checks booking, changes car status to avaliable and deletes relationship
@app.route('/cancel_car', methods=['PUT'])
def cancel_car_booking():
    record = json.loads(request.data)
    print(record)
    return cancel_booking(record['name'], record['reg'])


# Customer rents the car it has booked
@app.route('/rent_car', methods=['PUT'])
def rent_car_booking():
    record = json.loads(request.data)
    print(record)
    return rent_car(record['name'], record['reg'])


# Returns the car
@app.route('/return_car', methods=['PUT'])
def return_car_booking():
    record = json.loads(request.data)
    print(record)
    return return_car(record['name'], record['reg'], record['condition'])


if __name__ == '__main__':
    app.run(debug=True)
