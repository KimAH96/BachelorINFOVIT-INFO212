from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+ssc://f05d33fd.databases.neo4j.io"
AUTH = ("neo4j", "52cQIHi4QVIsIyNJig4s5rnx_4DccVqql4LbJPYOYy8")


def _get_connection() -> Driver:
    # driver = GraphDatabase.driver(URI, auth=AUTH)
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver


def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties


# Car
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
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg,year: $year, capacity:$capacity, status: $status}) RETURN a;",
                                           make=make, model=model, reg=reg, year=year, capacity=capacity, status=status)
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
    _get_connection().execute_query(
        "MATCH (a:Car{reg: $reg}) delete a;", reg=reg)


# Customer
def customer(name, age, adress):
    customer = _get_connection().execute_query(
        "MERGE (a:Customer{name: $name, age: $age, adress: $adress}) RETURN a;", name=name, age=age, adress=adress)
    nodes_json = [node_to_json(record["a"]) for record in customer]
    print(nodes_json)
    return nodes_json


def update_customer(name, age, adress):
    with _get_connection().session() as session:
        customers = session.run(
            "MATCH (a:Customer{name:$name}) set a.name=$name, a.age=$age, a.adress = $adress RETURN a;", name=name, age=age, adress=adress)
        print(customers)
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json


def delete_customer(name):
    _get_connection().execute_query(
        "MATCH (a:Customer{name: $name}) delete a;", name=name)


def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json


# Employee
def employee(name, age, adress, branch):
    employee = _get_connection().execute_query(
        "MERGE (a:Employee{name: $name, age: $age, adress: $adress, branch: $branch}) RETURN a;", name=name, age=age, adress=adress, branch=branch)
    nodes_json = [node_to_json(record["a"]) for record in employee]
    print(nodes_json)
    return nodes_json


def update_employee(name, age, adress, branch):
    with _get_connection().session() as session:
        employees = session.run(
            "MATCH (a:Employee{name:$name}) set a.name=$name, a.age=$age, a.adress=$adress, a.branch=$branch RETURN a;", name=name, age=age, adress=adress, branch=branch)
        print(employees)
        nodes_json = [node_to_json(record["a"]) for record in employees]
        print(nodes_json)
        return nodes_json


def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees]
        print(nodes_json)
        return nodes_json


def delete_employee(name):
    _get_connection().execute_query(
        "MATCH (a:Employee{name: $name}) delete a;", name=name)


#i funksjonen så brukes name fra customer som id, usikker på om det er lurere at customer-nodes har en egen unik id som feks af432
#oppgaven sier også at "The system must check that the customer with customer-id has not booked other cars"
#så det må lages en slags betingelse/query-sjekk på at kunden allerede ikke har en booking fra før av



#Denne funker som den skal.
def orderCar(name, reg):
    _get_connection().execute_query(
        "MATCH (p:Customer {name: $name}) WHERE NOT (p)-[:BOOKED]->(:Car {status: 'BOOKED'}) MATCH (c:Car{reg: $reg, status: 'Available'}) CREATE (p)-[b:BOOKED]->(c) SET c.status = 'BOOKED';", name=name, reg=reg)
        

def rent_car1(customer_id, car_id):  # Uferdig - trenger kanskje bare orderCar funksjonen?
    _get_connection().execute_query(
        "MATCH (c:Customer{id: $customer_id}), (car:Car{id: $car_id}) CREATE (c)-[:RENTS]->(car)", customer_id=customer_id, car_id=car_id)

#cancel booking. Denne funksjonen tar utgangspunkt i delete-car funksjonen. Den funker! 
def cancel_booking(name, reg):
    _get_connection().execute_query(
        "MATCH (p:Customer{name: $name})-[b:BOOKED]->(c:Car{reg: $reg}) DELETE b set c.status = 'Available'",name=name, reg=reg)


def rent_car(name, reg):
    _get_connection().execute_query(
    "MATCH (p:Customer {name: $name})-[b:BOOKED]->(c:Car{reg: $reg}) CREATE (p)-[:RENTED]->(c) DELETE b set c.status = 'Rented';", name=name, reg=reg)


#hvis denne denne har damaged som condition så skal status på bil-noden endres til "Damaged"
#hvis condition er ok/noe annet enn damaged, så skal status på bil-noden endres til "ok"
#funksjonen må også sikre seg at customer har leid den aktuelle bilen 
#Ferdig kode, fungerer som tenkt
def return_car(name, reg, condition):
    if condition == 'Damaged':
        _get_connection().execute_query("MATCH (p:Customer {name: $name})-[r:RENTED]->(c:Car{reg: $reg}) DELETE r set c.status = 'Damaged';", name=name, reg=reg)
    else:
        _get_connection().execute_query("MATCH (p:Customer {name: $name})-[r:RENTED]->(c:Car{reg: $reg}) DELETE r set c.status = 'Available';", name=name, reg=reg)





# result = save_car(make="Toyota", model="Camry", reg="XYZ123", year=2023, capacity=5)
# print(result)
# customer(name='Per Hansen', age='24', adress='Skolegaten 1b, 2348 Skolebyem')
# employee(name='Thor Thodesen', age='39', adress='Bilveien 23, 3929 LangVekkIStan', branch='Bergen')
# update_car(reg='ZZZ123', year='2013', model='A3', make='Audi', capacity='5', status='Available')
# update_car(reg='XYZ123', year='2023', model='Camry', make='Toyota', capacity='5', status='Available')
# update_car(reg='su17778', year='2023', model='Camry', make='Toyata', capacity='5', status='Available')
# update_car(reg='SV14567', year='2003', model='240', make='Volvo', capacity='5', status='Available')
# customer(name='Tove Olsen', age='72', adress='Stasjonsgaten 41, 3232 Volda')
# update_customer(name='Jan Nygaard', age='33', adress='Gamle Steinestøvegen 55, 5108 Hordvik')
# orderCar(name='Per Hansen', reg='XYZ123')
orderCar(name='Jan Nygaard', reg='SV14567')
# rent_car(name='Per Hansen', reg='ZZZ123')
# return_car(name='Per Hansen', reg='ZZZ123', condition='Damaged')