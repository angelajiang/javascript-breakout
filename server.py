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

### GLOBALS ###
curState = dict(paddleX=0, ballX=0, ballV=0)
lastState = dict()
#Tweakable parameters
#table
numActions = 3
maxPaddleX = 24
maxBallX = 30
maxBallY = 24
maxBallV = 6
tableFile = 'table'
#algorithm
defaultReward = .1
alpha = 1
decay = .9
greedyProbability = .5

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
    try:
        f = open(tableFile, 'r')
        qTable = pickle.load(f)
        f.close()
    except:
        create_table(tableFile)

### MODULES ###
def shrink(curVal, shrinkedMax, maxVal):
   return int((curVal/maxVal)*shrinkedMax)

def indexTable(state, action):
   paddleX = state['paddleX']
   ballX = state['ballX']
   ballV = state['ballV']
   return qTable[action, paddleX, ballX, ballV]

def eGreedy(state):
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    if (rightVal > leftVal):
        return 1
    elif (rightVal == leftVal):
        return 2
    else:
        return 0

def maxQ(state):
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    if (rightVal > leftVal):
        return rightVal
    elif (rightVal == leftVal):
        return stayVal
    else:
        return leftVal

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

### ROUTABLE MODULES ###

@app.route('/')
@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory('', filename)

@app.route('/get_move', methods=['POST'])
def get_move():
    global qTable
    global curState
    global lastState
    lastState = curState.copy()

    #Get current state
    curState['paddleX'] = int(request.values["paddleX"])
    bcurState['ballX'] = int(request.values["ballX"])
    curState['ballV'] = int(request.values["ballV"])

    #Update last state
    #if ballY = paddleY, reward = 1, else 0
    stateMaxQ = maxQ(curState)
    #updateQ(lastState, reward);

    move = eGreedy(curState)
    if (move == 1):
        return "right"
    elif (move == 2):
        return "stay"
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

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.debug = True
    app.run()
