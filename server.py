import flask
import re
import time
import os
import numpy as np
import cPickle as pickle
import signal
import sys
import random
import appconfig
from math import exp
from random import randint
from os import listdir
from os.path import isfile, join
from flask import Flask, request

####################### INITIALIZE  ###########################

app = Flask(__name__)
try:
    configObj = 'appconfig.' + os.environ['APPMODE']
    app.config.from_object(configObj)
    print os.environ['APPMODE']
except: app.config.from_object(appconfig.Config) # print os.environ['APPMODE']

#Globals
TESTING = app.testing
CURSTATE = dict(paddleX=1, ballX=1, ballV=1, ballY=1, move=2)
LASTSTATE = dict()
SAMPLESIZE = 30
UPDATECOUNT = 0
WRITECOUNT = app.config['WRITECOUNT']
PERIOD = app.config['PERIOD']
HITCOUNT=0
LOSECOUNT=0
WINCOUNT=0
GAMECOUNT=1
STARTTIME=time.time()
#Tweakable parameters
#table
TABLEFILE = app.config['TABLEFILE']
TABLEDIR = app.config['TABLEDIR']
NUMACTIONS = 3
MAXPADDLEX = 24 #0-24
MAXBALLX = 30   #0-30
MAXBALLV = 6
MAXBALLY = 26
#velocity mappings
UPLEFT = 5
UP = 4
UPRIGHT = 3
DOWNLEFT = 2
DOWN = 1
DOWNRIGHT = 0
#algorithm
DEFAULTREWARD = .1
ALPHA = 1
DECAY = .9
GOODREWARD = 1
BADREWARD = -1000
WINREWARD = 10

#Get tables from directory to test
if (TESTING):
    if app.config['GETRESULTS']: 
        path = app.config['TABLEPATH']
        TABLES = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        TABLEINDEX = 0
        TABLEFILE = os.path.join(path, TABLES[TABLEINDEX])

####################### MODULES ###########################

@app.route('/create_table/<filename>')
def create_table(filename):
    #Creates persistent q-table. Writes table object to filename
    global DEFAULTREWARD
    global NUMACTIONS
    global MAXPADDLEX
    global MAXBALLX
    global MAXBALLV
    global MAXBALLY

    #+1 for zero indexing
    table = np.ones(shape=(NUMACTIONS, MAXPADDLEX+1, MAXBALLX+1, MAXBALLY+1, MAXBALLV)) * DEFAULTREWARD
    f = open(filename, 'w')
    pickle.dump(table, f);
    f.close()
    return "Table stored in filename: " + filename

def loadTable():
    global TABLEFILE
    global QTABLE
    QTABLE = None
    while (QTABLE == None):
        try:
            f = open(TABLEFILE, 'r')
            QTABLE = pickle.load(f)
            f.close()
        except:
            create_table(TABLEFILE)
    print 'Current table: '+TABLEFILE

#q-table
loadTable()

def indexTable(state, action):
   global QTABLE
   paddleX = state['paddleX']
   ballX = state['ballX']
   ballV = state['ballV']
   ballY = state['ballY']
   #-1 for zero indexing?
   return QTABLE[action, paddleX-1, ballX-1, ballY-1, ballV]

def updateTable(state, action, value):
    global QTABLE
    paddleX = state['paddleX']
    ballX = state['ballX']
    ballV = state['ballV']
    ballY = state['ballY']
    #-1 for zero indexing
    QTABLE[action, paddleX-1, ballX-1, ballY-1, ballV] = value
    #print id(QTABLE)
    return

def maxMove(state):
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    choice = max(leftVal, rightVal, stayVal)
    if (leftVal == rightVal) and (rightVal == stayVal):
        return random.choice([0,1,2])
    if (rightVal == choice):
        if (rightVal == leftVal):
            return random.choice([0,1])
        elif (rightVal == stayVal):
            return random.choice([1,2])
        else:
            return 1
    elif (leftVal == choice):
        if (leftVal == stayVal):
            return random.choice([0,2])
        else:
            return 0
    else:
        return 2

def eGreedy(state):
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    eLeft = exp(leftVal)
    eRight = exp(rightVal)
    eStay = exp(stayVal)
    denom = float(eLeft + eRight + eStay)
    if (denom == 0):
        #If sum of eValues is 0, eVal/1 will be between 0 and 1
        denom = 1
    try:
        leftP = eLeft/denom
        rightP = eRight/denom
        stayP = eStay/denom
    except:
        leftP = .1
        rightP = .1
        stayP = .1
    greedyProb = max(leftP, rightP, stayP) 
    if random.random >= greedyProb:
        return randint(0,2)
    else:
        #Choose the move that maximizes q value.
        #If multiple valuse are equal, choose randomly between them
        if (leftVal == rightVal) and (rightVal == stayVal):
            return random.choice([0,1,2])
        if (rightVal == choice):
            if (rightVal == leftVal):
                return random.choice([0,1])
            elif (rightVal == stayVal):
                return random.choice([1,2])
            else:
                return 1
        elif (leftVal == choice):
            if (leftVal == stayVal):
                return random.choice([0,2])
            else:
                return 0
        else:
            return 2

def maxQ(state):
    #Returns the maximum q value of the state
    leftVal = indexTable(state, 0)
    rightVal = indexTable(state, 1)
    stayVal = indexTable(state, 2)
    return max(leftVal, rightVal, stayVal)

def signal_handler(signal, frame):
    #QTABLE written to file after ctrl-c
    global QTABLE
    frame = sys._getframe(0)
    print id(QTABLE)
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
    global BADREWARD
    global GOODREWARD

    action = state['move']
    lastQ = indexTable(state, action)
    q = (1-ALPHA)*lastQ + ALPHA*(reward+DECAY*stateMaxQ)
    updateTable(state, action, q)
    return

####################### ROUTABLES  ###########################

@app.route('/')
@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory('', filename)

@app.route('/get_move', methods=['POST'])
def get_move():
    #Algorithm globals
    global QTABLE
    global CURSTATE
    global LASTSTATE
    global WINREWARD
    global UP
    global UPLEFT
    global UPRIGHT
    #Results
    global TESTING
    global TABLES
    global TABLEINDEX
    global TABLEDIR
    global TABLEFILE
    global LOSECOUNT
    global WINCOUNT
    global STARTTIME
    global UPDATECOUNT
    global PERIOD
    global WRITECOUNT
    global HITCOUNT
    global GAMECOUNT
    global SAMPLESIZE

    #Get current state
    LASTSTATE = CURSTATE.copy()
    message = str(request.values['msgName'])
    wasHit = str(request.values['wasHit'])
    CURSTATE['paddleX'] = int(request.values["paddleX"])
    CURSTATE['ballX'] = int(request.values["ballX"])
    CURSTATE['ballV'] = int(request.values["ballV"])
    CURSTATE['ballY'] = int(request.values["ballY"])


    #Update last state
    ballV = CURSTATE['ballV']
    if (wasHit == 'true'):
        #Ball hit paddle
        reward = GOODREWARD
        HITCOUNT += 1
    elif (message == 'lose'):
        #Ball and paddle on same plane, just lost
        reward = BADREWARD
        print 'LOSE!!!!\n'
        GAMECOUNT+=1
        LOSECOUNT+=1
    elif (message == 'win'):
        reward = WINREWARD
        GAMECOUNT+=1
        WINCOUNT+=1
    elif (message == 'move'):
        reward = 0

    if (not TESTING):
        #Only update if learning or debugging
        stateMaxQ = maxQ(CURSTATE)
        updateQ(LASTSTATE, stateMaxQ, reward);

        #Periodically, write to new table
        if UPDATECOUNT > PERIOD:
            UPDATECOUNT = 0
            filename = TABLEDIR + '/' + str(WRITECOUNT)
            serialize(filename)
            WRITECOUNT+=1

    #Get move for current state
    if (TESTING):
        move = maxMove(CURSTATE)
    else:
        move = eGreedy(CURSTATE)
    CURSTATE['move'] = move
    UPDATECOUNT+=1

    #Reporting results
    if (GAMECOUNT == SAMPLESIZE and TESTING):
        if app.config['GETAVERAGES']:
            avgHits = float(HITCOUNT/GAMECOUNT)
            averagesfile = app.config['AVERAGESFILE']
            f = open(averagesfile, "a")
            s = str(WRITECOUNT*PERIOD) + ' ' + str(avgHits) + '\n'
            f.write(s)
            f.close()
        if app.config['GETRESULTS']:
            elapsedtime = round(time.time() - STARTTIME, 2)
            resultsfile = app.config['RESULTSFILE']
            f = open(resultsfile, "a")
            tablename = TABLES[TABLEINDEX]
            tablenumber = int((re.findall('\d+', tablename))[0])
            movecount = PERIOD*tablenumber
            s = str(movecount)+' '+str(HITCOUNT/float(SAMPLESIZE))+' '+str(LOSECOUNT/float(SAMPLESIZE))+' '+str(WINCOUNT/float(SAMPLESIZE))+' '+str(elapsedtime/SAMPLESIZE)+'\n'
            f.write(s)
            f.close()

            #If we've logged all tables in directory, we're done testing
            if tablenumber == len(TABLES):
                TESTING = False
            else:
                #Load next table as the q table
                path = app.config['TABLEPATH']
                TABLEINDEX += 1
                TABLEFILE = os.path.join(path, TABLES[TABLEINDEX])
                loadTable()
                #Reset parameters
                LOSECOUNT = 0
                HITCOUNT = 0
                GAMECOUNT = 1
                STARTTIME = time.time()

    #Return move to javascript
    if (move == 1):
        return "right"
    elif (move == 2):
        return "stay"
    else:
        return "left"



#@app.route('/serialize/<filename>')
def serialize(filename):
    #Writes qtable to filename
    global QTABLE
    #frame = sys._getframe(0)
    print id(QTABLE)
    f = open(filename, 'w')
    pickle.dump(QTABLE, f)
    f.close()
    return str(id(QTABLE)) + " written to " + filename

@app.route('/update_table')
def update_table():
    #For debugging to check if updates are written to file
    #Different like updateTable!
    global QTABLE
    global TABLEFILE
    QTABLE = QTABLE * 2
    tableStr = np.array_str(QTABLE)
    return tableStr

@app.route('/dispq/<paddleX>/<ballX>/<ballY>/<ballV>')
def dispq(paddleX, ballX, ballV):
    #Displays q values given a state
    global QTABLE
    tmp = dict()
    tmp['paddleX'] = int(paddleX)
    tmp['ballX'] = int(ballX)
    tmp['ballV'] = int(ballV)
    tmp['ballY'] = int(ballY)
    leftVal = indexTable(tmp, 0)
    rightVal = indexTable(tmp, 1)
    stayVal = indexTable(tmp, 2)
    statestr = str(paddleX) + ' ' + str(ballX) + ' ' + str(ballY) + ' '+ str(ballV)
    qstr = str(leftVal) + ' ' + str(rightVal) + ' ' + str(stayVal)
    return "state: " + statestr + '\n' + "q vals: " + qstr

@app.route('/disp/<obj>')
def disp(obj):
    global QTABLE
    global LASTSTATE
    global CURSTATE
    if (obj == 'config'):
        return
    if (obj == 'curstate'):
        state = CURSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballV = state['ballV']
        return str(paddleX) + ' ' + str(ballX) + ' ' +  str(ballV)
    elif (obj == 'laststate'):
        state = LASTSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballV = state['ballV']
        return str(paddleX) + ' ' + str(ballX) + ' ' + str(ballV)
    elif (obj == 'lastq'):
        state = LASTSTATE
        paddleX = state['paddleX']
        ballX = state['ballX']
        ballV = state['ballV']
        ballY = state['ballY']
        leftVal = indexTable(LASTSTATE, 0)
        rightVal = indexTable(LASTSTATE, 1)
        stayVal = indexTable(LASTSTATE, 2)
        statestr = str(paddleX) + ' ' + str(ballX) + ' ' + str(ballY) + ' '+ str(ballV)
        qstr = str(leftVal) + ' ' + str(rightVal) + ' ' + str(stayVal)
        return "state: " + statestr + '\n' + "q vals: " + qstr
    elif (obj == 'table'):
        tableStr = np.array_str(QTABLE)
        return tableStr
    else:
        return 'did not understand obj parameter'


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.run('127.0.0.1',5000)
