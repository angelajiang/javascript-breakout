import flask
import os
import sqlite3
import numpy as np
import cPickle as pickle
import signal
import sys
from os import listdir
from os.path import isfile, join
from flask import Flask, request
app = Flask(__name__)

#Tweakable parameters
paddleXDim = 650
ballXDim = 650
numActions = 2
maxPaddleX = 65
maxBallX = 65
maxBallV = 3
defaultReward = .1
tableFile = 'table'


@app.route('/create_table/<filename>')
def create_table(filename):
    #Creates persistent q-table. Writes table object to filename
    global numActions
    global maxPaddleX
    global maxBallX
    global maxBallV
    global defaultReward

    table = np.ones(shape=(numActions, maxPaddleX, maxBallX, maxBallV)) * defaultReward
    f = open(filename, 'w+')
    pickle.dump(table, f);
    f.close()
    return "Table stored in filename: " + filename

#q-table
qTable = None
while (qTable == None):
    f = open(tableFile, 'r')
    try:
        qTable = pickle.load(f)
        f.close()
    except:
        f.close()
        create_table(tableFile)

def shrink(curVal, shrinkedMax, maxVal):
   return int((curVal/maxVal)*shrinkedMax)

@app.route('/')
@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory('', filename)

@app.route('/get_move', methods=['POST'])
def get_move():
    global qTable
    paddleX = float(request.values["paddleX"])
    ballX = float(request.values["ballX"])
    ballV = float(request.values["ballV"])

    paddleX = shrink(paddleX, maxPaddleX, paddleXDim)
    ballX = shrink(ballX, maxBallX, ballXDim)

    if (ballX > paddleX):
        return "right"
    else:
        return "left"

@app.route('/update_table')
def update_table():
    #For debugging to check if updates are written to file
    global qTable
    global tableFile
    qTable = qTable * 2
    tableStr = np.array_str(qTable)
    return tableStr

@app.route('/print_table')
def print_table():
    global qTable
    tableStr = np.array_str(qTable)
    return tableStr

def signal_handler(signal, frame):
    #qTable written to file after ctrl-c
    frame = sys._getframe(0)
    global qTable
    global tableFile
    f = open(tableFile, 'w')
    pickle.dump(qTable, f)
    f.close()
    sys.exit(0)
    return 

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.debug = True
    app.run()
