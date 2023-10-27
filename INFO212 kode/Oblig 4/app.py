from flask import render_template, request, redirect, url_for, Flask
from neo4j import GraphDatabase

app = Flask(__name__)

@app.route('/')
def helloJson():
    return {'message':'Hello world'}


if __name__ == '__main__':
    app.run(debug=True)

