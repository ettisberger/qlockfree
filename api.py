#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import request
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['aargau']

color = config.get('default', 'color')

app = Flask(__name__)

@app.route('/')
def hello_world():
    print("API: Hello World")
    return jsonify(result='API: Hello World Welcome to Qlockfree.')

@app.route('/color', methods=['GET'])
def getColor():
    print("API: Get color ", color)
    return jsonify(color)

@app.route('/color/change/default', methods=['GET','PUT'])
def resetDefaultColor():
    global color
    print("API: Change color to default ", config.get('default', 'color'))
    color = config.get('default', 'color')
    return jsonify(config.get('default', 'color'))

@app.route('/color/change', methods=['GET','PUT'])
def changeColor():
    global color

    if 'color' in request.args:
        print("API: Change color from", color, " to ", request.args['color'])
        color = [int(x.strip()) for x in request.args['color'].split(',')]
    else:
        if color == config.get('default', 'colorWhite'):
            print("API: Change color from", color, " to ", config.get('default', 'colorRed'))
            color = config.get('default', 'colorRed')
        elif color == config.get('default', 'colorRed'):
            print("API: Change color from", color, " to ", config.get('default', 'colorWhite'))
            color = config.get('default', 'colorWhite')

    print("API: Change color")
    return jsonify(color)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
