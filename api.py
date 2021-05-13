#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import request
import config

color = config.DEFAULT_COLOR

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
    print("API: Change color to default ", config.DEFAULT_COLOR)
    color = config.DEFAULT_COLOR
    return jsonify(config.DEFAULT_COLOR)

@app.route('/color/change', methods=['GET','PUT'])
def changeColor():
    global color

    if 'color' in request.args:
        print("API: Change color from", color, " to ", request.args['color'])
        color = [int(x.strip()) for x in request.args['color'].split(',')]
    else:
        if color == config.COLOR_WHITE:
            print("API: Change color from", color, " to ", config.COLOR_RED)
            color = config.COLOR_RED
        elif color == config.COLOR_RED:
            print("API: Change color from", color, " to ", config.COLOR_WHITE)
            color = config.COLOR_WHITE

    print("API: Change color")
    return jsonify(color)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)