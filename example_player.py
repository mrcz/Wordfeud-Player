# -*- coding: utf-8 -*-

# (c) 2011, Marcus Svensson <macke77@gmail.com>
# See gpl-2.0.txt for license

import heapq

from wordfeudplayer.wordlist import Wordlist
from wordfeudplayer.board import Board


def example():
    # create a Wordlist and tell it to read one or more wordlists
    w = Wordlist()
    print 'Reading wordlist...'
    dsso_id = w.read_wordlist('ordlista.txt')
    print 'Done'

    # create a Board with standard bonus square placement and
    # set the current state of the game (where tiles are placed)
    b = Board()
    state = [u'               ',
             u'               ',
             u'            d  ',
             u'            r  ',
             u'          m ärm',
             u'         bang  ',
             u'         ex g  ',
             u'       tar se  ',
             u'       j  lät  ',
             u'       o  ån g ',
             u'    påtat skarv',
             u'       t   t i ',
             u'        cidErs ',
             u'         lus ed',
             u'          o  nu']
    b.set_state(state)

    # the letters we have on hand, '*' is a blank tile
    letters = '*shetgj'

    print 'The board is:\n%s' % b

    # calculate all possible words and their scores
    print '\nThinking...'
    top20 = calc_best_moves(b, w, letters, dsso_id)

    (x, y, horizontal, word, score) = top20[0]
    print '\nBest word is "%s", playing it' % word
    b.play_word(word, x, y, horizontal)

    print '\nBoard is:\n%s' % b

    print "\nOpponent's turn, thinking..."
    next_top20 = calc_best_moves(b, w, letters, dsso_id)


def calc_best_moves(b, w, letters, variant):
    words = b.calc_all_word_scores(letters, w, variant)

    # pick out the 20 words with highest score and print them
    top20 = heapq.nlargest(20, words, lambda w: w[4])

    if len(top20) == 0:
        print 'There are no possible words'
        return []

    print 'Score StartX StartY  Direction Word (capital letter means "use wildcard")'
    for (x, y, horizontal, word, score) in top20:
        print '%5d %6d %6s %10s %s' % (score, x, y, 'Horizontal' if horizontal else 'Vertical', word)

    return top20

if __name__ == '__main__':
    example()
