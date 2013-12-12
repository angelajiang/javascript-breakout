import matplotlib
import matplotlib.pyplot as plt

def parser(filename):
    results = dict()
    with open(filename, 'r') as f:
        for line in f:
            values = line.split()
            move = int(values[0])
            if (move > 15000000):
                move = move/1000000
                print 'here'
            hit = values[1]
            lose = values[2]
            win = values[3]
            dt = values[4]
            results[move] = dict(hit=hit,lose=lose,win=win,dt=dt)
    sortedResults = sorted(results.items(), key=lambda x: x[1])
    moves = []
    hits = []
    losses = []
    wins = []
    dts = []
    for r in sortedResults:
        moves.append(r[0])
        hits.append(r[1]['hit'])
        losses.append(r[1]['lose'])
        wins.append(r[1]['win'])
        dts.append(r[1]['dt'])

    plt.figure()
    plt.scatter(moves, hits)
    plt.ylabel('Hits')
    plt.savefig('plots/hits.pdf')

    plt.figure()
    plt.scatter(moves, losses)
    plt.ylabel('Losses')
    plt.savefig('plots/losses.pdf')

    plt.figure()
    plt.scatter(moves, losses)
    plt.ylabel('Losses')
    plt.savefig('plots/losses.pdf')

    plt.figure()
    plt.scatter(moves, wins)
    plt.ylabel('Wins')
    plt.savefig('plots/wins.pdf')

    plt.figure()
    plt.scatter(moves, dts)
    plt.ylabel('dt')
    plt.savefig('plots/dt.pdf')
    return results

if __name__ == '__main__':
    results = parser('logs/results_100')




