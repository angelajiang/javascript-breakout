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
tableFile = 'table'
dim = dict()
dim['numActions'] = 3
dim['maxPaddleX'] = 24 #0-24
dim['maxBallX'] = 30   #0-30
dim['maxBallY'] = 24   #0-24
dim['maxBallV'] = 6
#velocity mappings
vMap = dict()
vMap['downLeft'] = 1
vMap['down'] = 2
vMap['downRight'] = 3
vMap['upLeft'] = 4
vMap['up'] = 5
vMap['upRight'] = 6

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

    #+1 for zero indexing
    table = np.ones(shape=(numActions, maxPaddleX+1, maxBallX+1, maxBallY+1, maxBallV)) * defaultReward
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
   #-1 for zero indexing
   return qTable[action, paddleX-1, ballX-1, ballV-1]

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
    global dim
    global vMap

    lastState = curState.copy()

    #Get current state
    curState['paddleX'] = int(request.values["paddleX"])
    curState['ballX'] = int(request.values["ballX"])
    curState['ballV'] = int(request.values["ballV"])
    curState['ballY'] = int(request.values["ballY"])

    ballY = curState['ballY']
    ballV = curState['ballV']

    #Update last state
    #if ballY = paddleY, reward = 1, else 0
    if (ballY == dim['maxBallY']) and (ballV == vMap['up'] or ballV == vMap['upLeft'] or ballV == vMap['upRight']):
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
