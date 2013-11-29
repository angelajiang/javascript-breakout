import flask
import os
from os import listdir
from os.path import isfile, join
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory('', filename)

@app.route('/get_move/<paddleX>/<ballX>')
def get_move(paddleX, ballX):
    paddleX = float(paddleX)
    ballX = float(ballX)
    if (ballX > paddleX):
        return "right"
    else:
        return "left"

if __name__ == '__main__':
    app.debug = True
    app.run()
