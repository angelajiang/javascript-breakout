#!/usr/bin/env python
import json
import cPickle as pickle
import sys

def main():
    if len(sys.argv) != 3:
        print 'Usage: jsonify [table file] [output table name]'
        sys.exit(1)

    inF = sys.argv[1]
    outTable = sys.argv[2]    
    f = open(inF, 'r')
    table = pickle.load(f)
    f.close()
    
    out = 'var ' + outTable + ' = ' + json.dumps(table.tolist()) + ';'
    outFname = outTable + '.js'
    outF = open(outFname, 'w')
    outF.write(out)

if __name__ == '__main__':
    main()
