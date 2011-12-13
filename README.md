# wordfeudplayer

A python library for calculating the best moves in a game of
wordfeud.

This is just a library, it has no GUI. If you just want to cheat, or
maybe want to try it out without any programming, see
[http://www.wordfeusk.se/](http://www.wordfeusk.se/)

It has a nice web interface to the library.


## Quick start

For wordfeudplayer to be able to play in a certain language a wordlist
is needed. One is included here, it is the one that wordfeud
originally used for games in Swedish. It is called ["Den stora svenska
ordlistan"](http://www.dsso.se) and is made by Göran Andersson. It has
been slightly modified by the wordfeud author and was previously
downloadable from [here](http://wordfeud.com/dictionaries/). It is
licensed under the [Creative Commons Attribution-Share
Alike](http://creativecommons.org/licenses/by-sa/3.0/) license. The
rest of the project is licensed under GPL version 2.

A wordlist must be in UTF-8 encoding (no BOM) and contain one word per line.

An example of how to use the library is available in
example_player.py. It is tested with both regular Python 2.7 and PyPy.

```python
import heapq

from wordfeudplayer.wordlist import Wordlist
from wordfeudplayer.board import Board


def example():
    # create a Wordlist and tell it to read one or more wordlists from disk
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
```
