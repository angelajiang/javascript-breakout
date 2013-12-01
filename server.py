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
CURSTATE = dict(paddleX=1, ballX=1, ballY = 1, ballV=1, move=2)
LASTSTATE = dict()
#Tweakable parameters
#table
TABLEFILE = 'table'
NUMACTIONS = 3
MAXPADDLEX = 24 #0-24
MAXBALLX = 30   #0-30
MAXBALLY = 24   #0-24
MAXBALLV = 6
#velocity mappings
DOWNLEFT = 1
DOWN = 2
DOWNRIGHT = 3
UPLEFT = 4
UP = 5
UPRIGHT = 6

#algorithm
DEFAULTREWARD = .1
ALPHA = 1
DECAY = .9
GREEDYPROB = .5

#create_table must be before QTABLE references it
@app.route('/create_table/<filename>')
def create_table(filename):
    #Creates persistent q-table. Writes table object to filename
    global DEFAULTREWARD
    global NUMACTIONS
    global MAXPADDLEX
    global MAXBALLX
    global MAXBALLY
    global MAXBALLV

    #+1 for zero indexing
    table = np.ones(shape=(NUMACTIONS, MAXPADDLEX+1, MAXBALLX+1, MAXBALLY+1, MAXBALLV)) * DEFAULTREWARD
    f = open(filename, 'w+')
    pickle.dump(table, f);
    f.close()
    return "Table stored in filename: " + filename

#q-table
QTABLE = None
while (QTABLE == None):
    try:
        f = open(TABLEFILE, 'r')
        QTABLE = pickle.load(f)
        f.close()
    except:
        create_table(TABLEFILE)

### MODULES ###
def shrink(curVal, shrinkedMax, maxVal):
   return int((curVal/maxVal)*shrinkedMax)

def indexTable(state, action):
   global QTABLE
   paddleX = state['paddleX']
   ballX = state['ballX']
   ballY = state['ballY']
   ballV = state['ballV']
   #-1 for zero indexing
   return QTABLE[action, paddleX-1, ballX-1, ballY-1, ballV-1]

def updateTable(state, action, value):
    global QTABLE
    paddleX = state['paddleX']
    ballX = state['ballX']
    ballY = state['ballY']
    ballV = state['ballV']
    #-1 for zero indexing
    QTABLE[action, paddleX-1, ballX-1, ballY-1, ballV-1] = value
    return

def eGreedy(state):
    #Chooses a move due to eGreedy
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    maxVal = max(leftVal, rightVal, stayVal)
    if (rightVal == maxVal):
        return 1
    elif (leftVal == maxVal):
        return 0
    else:
        return 2

def maxQ(state):
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    return max(leftVal, rightVal, stayVal)

def signal_handler(signal, frame):
    #QTABLE written to file after ctrl-c
    frame = sys._getframe(0)
    global QTABLE
    global TABLEFILE
    f = open(TABLEFILE, 'w')
    pickle.dump(QTABLE, f)
    f.close()
    sys.exit(0)
    return 

def updateQ(state, stateMaxQ, reward):
    #Calculates q value that Q(s,a) of last state should be
    #Calls updateTable to update
    global DEFAULTREWARD
    global ALPHA
    global DECAY
    global GREEDYPROB

    action = state['move']
    lastQ = indexTable(state, action)
    q = (1-ALPHA)*lastQ + ALPHA*(reward+DECAY*stateMaxQ)
    updateTable(state, action, q)
    return

### ROUTABLE MODULES ###

@app.route('/')
@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory('', filename)

@app.route('/get_move', methods=['POST'])
def get_move():
    global QTABLE
    global CURSTATE
    global LASTSTATE
    global MAXBALLY
    global UP
    global UPLEFT
    global UPRIGHT

    #Game over?
    ballY = int(request.values["ballY"])
    if (ballY >= MAXBALLY):
        return "stay"

    #Get current state
    LASTSTATE = CURSTATE.copy()
    CURSTATE['paddleX'] = int(request.values["paddleX"])
    CURSTATE['ballX'] = int(request.values["ballX"])
    CURSTATE['ballV'] = int(request.values["ballV"])
    CURSTATE['ballY'] = int(request.values["ballY"])

    #Update last state
    ballV = CURSTATE['ballV']
    if (ballY == MAXBALLY) and (ballV == UP or ballV == UPLEFT or ballV == UPRIGHT):
        reward = 1
    else:
        reward = 0
    stateMaxQ = maxQ(CURSTATE)
    updateQ(LASTSTATE, stateMaxQ, reward);

    #Get move for current state
    move = eGreedy(CURSTATE)
    CURSTATE['move'] = move
    if (move == 1):
        return "right"
    elif (move == 2):
        return "stay"
    else:
        return "left"

@app.route('/update_table')
def update_table():
    #For debugging to check if updates are written to file
    global QTABLE
    global TABLEFILE
    QTABLE = QTABLE * 2
    tableStr = np.array_str(QTABLE)
    return tableStr

@app.route('/disp/<obj>')
def disp(obj):
    global QTABLE
    global LASTSTATE
    global CURSTATE
    if (obj == 'curstate'):
        state = CURSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballY = state['ballY']
        ballV = state['ballV']
        return str(paddleX) + ' ' + str(ballX) + ' ' + str(ballY) + ' ' + str(ballV)
    elif (obj == 'laststate'):
        state = LASTSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballY = state['ballY']
        ballV = state['ballV']
        return str(paddleX) + ' ' + str(ballX) + ' ' + str(ballY) + ' ' + str(ballV)
    elif (obj == 'lastq'):
        state = LASTSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballY = state['ballY']
        ballV = state['ballV']
        leftVal = indexTable(LASTSTATE, 0)
        rightVal = indexTable(LASTSTATE, 1)
        stayVal = indexTable(LASTSTATE, 2)
        statestr = str(paddleX) + ' ' + str(ballX) + ' ' + str(ballY) + ' ' + str(ballV)
        qstr = str(leftVal) + ' ' + str(rightVal) + ' ' + str(stayVal)
        return "state: " + statestr + '\n' + "q vals: " + qstr
    elif (obj == 'table'):
        tableStr = np.array_str(QTABLE)
        return tableStr
    else:
        return 'did not understand obj parameter'


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.debug = True
    app.run()
