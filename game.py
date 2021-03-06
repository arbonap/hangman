"""
Hangman Game with Easy and Hard Levels
"""


import urllib2
import random
import sys
import emoji #does this work with users without iTerm?
import string
import requests
import json
import argparse
from hangmanstatus import hangmanstatus
from environment import HEADERS

# =============== Meta Data ================
__description__ = 'Hangman Commandline Game'
__version__ = '0.0.1'
__author__ = 'Patricia Arbona (@arbonap)'


TXT = urllib2.urlopen('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words')
WORD_LIST = TXT.read().split('\n')


parser = argparse.ArgumentParser(description='Hangman')
parser.add_argument('--hard',
                    action='store_true',
                    help='Play Hangman on Hard Mode! Feel like taking on a challenge? \
                    Try guessing a difficult word. Use the --hard flag to begin.')

parser.add_argument('--easy',
                    action='store_true',
                    help='Play Hangman on Easy Mode! Feel like a warm-up? \
                    Try guessing a more commonplace word. Use the --easy flag to begin.')

args = parser.parse_args()

def shuffled_word(WORD_LIST):
    """

    >>> WORD_LIST = ['apples']

    >>> shuffled_word(WORD_LIST)
    'apples'

    """
    word = random.shuffle(WORD_LIST)
    word = WORD_LIST[0]
    return word

def get_difficulty(word):
    """
    >>> word = 'apples'

    >>> type(get_difficulty(word))
    <type 'dict'>

    """
    r = requests.get("https://twinword-word-graph-dictionary.p.mashape.com/difficulty/?entry={}".format(word), headers=HEADERS)
    adict = r.json()
    return adict


def get_random_word(WORD_LIST):
    """
    Takes in list, returns single string.

    >>> WORD_LIST = ['apples']

    >>> type(get_random_word(WORD_LIST))
    <type 'str'>

    """
    headers = HEADERS
    if args.hard:
        while True:
            try:
                word = shuffled_word(WORD_LIST)
                adict = get_difficulty(word)
                #TODO: improve catching exceptions, give more helpful message and how to fail gracefully
                if adict['result_code'] != '200' or adict['ten_degree'] < 5:
                    raise Exception
                break
            except Exception:
                continue

    elif args.easy:
        while True:
            try:
                word = shuffled_word(WORD_LIST)
                adict = get_difficulty(word)
                #TODO: improve catching exceptions, give more helpful message and how to fail gracefully
                if adict['result_code'] != '200' or int(adict['ten_degree']) > 2:
                    raise Exception
            except Exception:
                continue
            break
    else:
        word = shuffled_word(WORD_LIST)
    return word

def display_board(hangmanstatus, missed_letters, correct_letters, secret_word):
    #TODO: add docstring test
    print(hangmanstatus[len(missed_letters)])

    print('Missed letters:')
    for letter in missed_letters:
        print letter,
    blanks = '_' * len(secret_word)
    print "\n"

    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            # TODO: use join() instead of concatenate
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks:
        print letter,

def get_guess(already_guessed):
    #TODO: add docstring test
    while True:
        print(emoji.emojize('\nPlease guess a letter. :abc: ',
                            use_aliases=True))
        guess = raw_input().lower()
        if len(guess) != 1:
            print(emoji.emojize('Please only enter one letter. :capital_abcd: ',
                                use_aliases=True))
        elif guess in already_guessed:
            print('You have already guessed that letter, please choose again.')
        elif guess not in string.ascii_lowercase:
            print(emoji.emojize('Please enter a letter. :capital_abcd:',
                                use_aliases=True))
        else:
            return guess

def play_again():
    print(emoji.emojize("Would you like to play again? :cherries: ",
                        use_aliases=True))
    return raw_input().lower().startswith('y')

def main():
    print(emoji.emojize(":sparkles: *~H A N G P E R S O N~* :sparkles:",
                        use_aliases=True))
    print(emoji.emojize("A Hangman Game implemented in Python :snake:",
                        use_aliases=True))
    missed_letters = ''
    correct_letters = ''
    secret_word = get_random_word(WORD_LIST)
    game_is_done = False

    while True:
        display_board(hangmanstatus, missed_letters, correct_letters, secret_word)

        guess = get_guess(missed_letters + correct_letters)

        if guess in secret_word:
            correct_letters += guess

            found_all_letters = True
            for i in range(len(secret_word)):
                if secret_word[i] not in correct_letters:
                    found_all_letters = False
                    break
            if found_all_letters:
                print(emoji.emojize(':raised_hands: Congratulations! :tada: \
                                    You correctly figured out that the secret hangman \
                                    word is %s! You won!',
                                    use_aliases=True) % secret_word)
                game_is_done = True
        else:
            missed_letters = missed_letters + guess

            if len(missed_letters) >= 6:
                display_board(hangmanstatus, missed_letters, correct_letters, secret_word)
                print(emoji.emojize("You have run out of guesses! :frowning:",
                                    use_aliases=True))
                print "You incorrectly guessed %d letters" % len(missed_letters)
                print "The secret word was '%s'" % secret_word
                game_is_done = True

        if game_is_done is True:
            if play_again():
                missed_letters = ''
                correct_letters = ''
                game_is_done = False
                secret_word = get_random_word(WORD_LIST)
            else:
                print(emoji.emojize("Goodbye! Have a wonderful day :sunny:",
                                    use_aliases=True))
                sys.exit()

if __name__ == "__main__":
    # inititalize hangman game
    main()

    # # ======== TESTING =========
    # import doctest
    # doctest.testmod(verbose=True)
