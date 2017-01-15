from cornetometro import Cornetometro
import sys

# THIS FILE USES THE CLASSIFIER ON A MATCH FILE AND COMPUTES THE STATS OF THE PLAYERS
# IF VERBOSE IS ACTIVATED, EACH TWEET WILL BE PRINTED WITH ITS RESPECTIVE CLASSIFICATION
# OTHERWISE ONLY THE PLAYER STATS WILL BE PRINTED

def main():
    verbose = False
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == '-v':
            verbose = True
            del sys.argv[i]
        else:
            i += 1

    if len(sys.argv) < 3:
        print "ERROR: Less arguments than expected"
        print "python test_cornetometro.py <input file> <output file> [-v]"
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    input_file = open(input_path)
    output_file = open(output_path, 'w')

    teams = input_file.readline().split()

    player_names = input_file.readline()
    # Check if player names are separated with commas or spaces
    if ',' in player_names:
        players = player_names.split(',')
    else:
        players = player_names.split()

    c = Cornetometro(teams, players)
    c.load('classifier.obj')

    tweet = ''

    for line in input_file:
        if line[:4] == '####':
            clazz = c.classify(tweet)
            tweet += line[:-1]
            tweet += ' ===> {}\n'.format(clazz.upper())
            if verbose:
                output_file.write(tweet)
            tweet = ''
        else:
            tweet += line

    input_file.close()

    if verbose:
        output_file.write('\n')

    for player in c.players:
        stats = c.get_stats(player)
        output_file.write("{}: {} / {} ==> {}\n".format(player, stats['positive'], stats['negative'], c.get_score(player)))
    output_file.close()

if __name__ == "__main__":
    main()
