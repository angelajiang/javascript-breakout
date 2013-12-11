#!/usr/bin/env python
import json
import cPickle as pickle
import sys

def main():
    if len(sys.argv) != 2:
        print sys.argv
        print 'wrong way!'
        sys.exit(1)

    f = open(sys.argv[1], 'r')
    table = pickle.load(f)

    out = json.dumps(table.tolist())

    print out

if __name__ == '__main__':
    main()
