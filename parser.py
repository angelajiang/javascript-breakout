#import matplotlib
#import matplotlib.pyplot as plt

def parser(filename):
    move = []
    hit = []
    lose = []
    win = []
    dt = []
    results = dict(move=move, hit=hit,lose=lose,win=win,dt=dt)
    with open(filename, 'r') as f:
        for line in f:
            values = line.split()
            move.append(values[0])
            hit.append(values[1])
            lose.append(values[2])
            win.append(values[3])
            dt.append(values[4])
    return results

if __name__ == '__main__':
    results = parser('results')




