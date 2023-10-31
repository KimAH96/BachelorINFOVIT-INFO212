from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+ssc://f05d33fd.databases.neo4j.io"
AUTH = ("neo4j", "52cQIHi4QVIsIyNJig4s5rnx_4DccVqql4LbJPYOYy8")

def _get_connection() -> Driver:
    # driver = GraphDatabase.driver(URI, auth=AUTH)
    driver = GraphDatabase.driver(URI,auth=AUTH)
    driver.verify_connectivity()
    return driver


def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties


def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def save_car(make, model, reg, year, capacity, status):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg,year: $year, capacity:$capacity, status: $status}) RETURN a;", make = make, model = model, reg = reg, year = 
    year, capacity = capacity, status = status)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

def update_car(make, model, reg, year, capacity, status):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity, a.status = $status RETURN a;", reg=reg, make=make, model=model, year=year,
        capacity=capacity, status=status)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg =reg)

def customer(name, age, adress):
    customer = _get_connection().execute_query("MERGE (a:Customer{name: $name, age: $age, adress: $adress}) RETURN a;", name = name, age = age, adress = adress)
    nodes_json = [node_to_json(record["a"]) for record in customer]
    print(nodes_json)
    return nodes_json

def update_customer(name, age, adress):
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer{name:$name}) set a.name=$name, a.age=$age, a.adress = $adress RETURN a;", name=name, age=age, adress=adress)
        print(customers)
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json

def delete_customer(name):
    _get_connection().execute_query("MATCH (a:Customer{name: $name}) delete a;", name = name)

def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json

def employee(name, age, adress, branch):
    employee = _get_connection().execute_query("MERGE (a:Employee{name: $name, age: $age, adress: $adress, branch: $branch}) RETURN a;", name = name, age = age, adress = adress, branch = branch)
    nodes_json = [node_to_json(record["a"]) for record in employee]
    print(nodes_json)
    return nodes_json

def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees]
        print(nodes_json)
        return nodes_json

def delete_employee(name):
    _get_connection().execute_query("MATCH (a:Employee{name: $name}) delete a;", name = name)


# result = save_car(make="Toyota", model="Camry", reg="XYZ123", year=2023, capacity=5)
# print(result)

#customer(name='Per Hansen', age='24', adress='Skolegaten 1b, 2348 Skolebyem')
#employee(name='Thor Thodesen', age='39', adress='Bilveien 23, 3929 LangVekkIStan', branch='Bergen')

# update_car(reg='ZZZ123', year='2013', model='A3', make='Audi', capacity='5', status='Available')

# update_car(reg='XYZ123', year='2023', model='Camry', make='Toyota', capacity='5', status='Available')
# update_car(reg='su17778', year='2023', model='Camry', make='Toyata', capacity='5', status='Available')
# update_car(reg='SV14567', year='2003', model='240', make='Volvo', capacity='5', status='Available')

