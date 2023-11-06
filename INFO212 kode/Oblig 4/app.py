from flask import render_template, request, redirect, url_for, Flask, jsonify
from neo4j import GraphDatabase
from my_dao import *


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Car rental company'

@app.route('/create_customer', methods=['POST'])
def create_customer():
    record = json.loads(request.data)
    print(record)
    customer(record['name'], record['age'], record['adress'])
    return "Customer created successfully"

@app.route('/update_customer', methods=['PUT'])
def customer_update():
    record = json.loads(request.data)
    print(record)
    return update_customer(record['name'], record['age'], record['adress'])

@app.route('/get_customers', methods=['GET'])
def all_customers():
    return findAllCustomers()

@app.route('/create_employee', methods=['POST'])
def create_employee():
    record = json.loads(request.data)
    print(record)
    return employee(record['name'], record['age'], record['adress'], record['branch'])

@app.route('/update_employee', methods=['PUT'])
def employee_update():
    record = json.loads(request.data)
    print(record)
    return update_employee(record['name'], record['age'], record['adress'], record['branch'])

@app.route('/find_employees', methods=['GET'])
def findEmployees():
    record = json.loads(request.data)
    print(record)
    return findAllEmployees()

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


@app.route('/order_car', methods=['POST', 'PUT'])
def booking_customer():
    record = dict(json.loads(request.data))
    print(record)
    orderCar(record['name'], record['reg'])
    reg_nr = record.get('reg')
    status = record.get('status')
    message = f"The booking of car {reg_nr} was successful"
    data = {"Message": message}
    return jsonify(data)
    

# Checks booking, changes car status to avaliable and deletes relationship
@app.route('/cancel_car', methods=['PUT'])
def cancel_car_booking():
    record = dict(json.loads(request.data))
    print(record)
    cancel_booking(record['name'], record['reg'])
    reg_nr = record.get('reg')
    message = f"The cancellation of {reg_nr} was successful"
    data = {"Message": message}
    return jsonify(data)


# Customer rents the car
@app.route('/rent_car', methods=['PUT'])
def rent_car_booking():
    record = dict(json.loads(request.data))
    print(record)
    rent_car(record['name'], record['reg'])
    regnr = record.get('reg')
    message = f"We can confirm that your rental of car {regnr}. You can pick up the car at the agreed time and place."
    data = {"Message": message}
    return jsonify(data)


# Returns the car
@app.route('/return_car', methods=['PUT'])
def return_car_booking():
    record = dict(json.loads(request.data))
    print(record)
    return_car(record['name'], record['reg'], record['condition'])
    regnr = record.get('reg')
    condition = record.get('condition')
    message = f"We confirm you have returned car {regnr}. The condition of the car when returned was {condition}"
    data = {"Message": message}
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
