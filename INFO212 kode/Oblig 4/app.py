from flask import render_template, request, redirect, url_for, Flask
from neo4j import GraphDatabase
from my_dao import *


app = Flask(__name__)

@app.route('/get_cars', methods=['GET'])
def query_records():
    return findAllCars()

@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = json.loads(request.data)
    print(record)
    print(record['reg'])
    return findCarByReg(record['reg'])


if __name__ == '__main__':
    app.run(debug=True)

