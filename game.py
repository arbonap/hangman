import click
import urllib2
import random
import sys
import emoji
import string
from hangmanstatus import hangmanstatus

txt = urllib2.urlopen('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words')
word_list = txt.read().split('\n')
print len(word_list)

def get_random_word(word_list):
    random.shuffle(word_list)
    print word_list[0]
    return word_list[0]

def display_board(hangmanstatus, missed_letters, correct_letters, secret_word):
    print(hangmanstatus[len(missed_letters)])
    print()

    print('Missed letters:')
    for letter in missed_letters:
        print(letter)
        print "_____"

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks:
        print(letter)
    print "______"

def getGuess(alreadyGuessed):

    while True:
        print(emoji.emojize('Guess a letter. :abc: ', use_aliases=True))
        guess = raw_input()
        guess = guess.lower()
        if len(guess) != 1:
            print(emoji.emojize('Please only enter one letter. :capital_abcd: ', use_aliases=True))
        elif guess in alreadyGuessed:
            print('You have already guessed that letter, please choose again.')
        elif guess not in string.ascii_lowercase:
            print(emoji.emojize('Please enter a letter. :capital_abcd:', use_aliases=True))

        else:
            return guess

def playAgain():
    print(emoji.emojize("Would you like to play again? :cherries: ", use_aliases=True))
    return raw_input().lower().startswith('y')


print(emoji.emojize(":sparkles: *~H A N G M A N~* :sparkles:", use_aliases=True))
print(emoji.emojize("A Hangman Game implemented in Python :snake:", use_aliases=True))
missed_letters = ''
correct_letters = ''
secret_word = get_random_word(word_list)
game_is_done = False

while True:
    display_board(hangmanstatus, missed_letters, correct_letters, secret_word)

    guess = getGuess(missed_letters + correct_letters)

    if guess in secret_word:
        correct_letters += guess

        found_all_letters = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                found_all_letters = False
                break
        if found_all_letters:
            print(emoji.emojize(':raised_hands: Congratulations! :tada: The secret hangman word is %s! You won!', use_aliases=True) % secret_word)
            game_is_done = True
    else:
        missed_letters = missed_letters + guess

        if len(missed_letters) >= 6:
            display_board(hangmanstatus, missed_letters, correct_letters, secret_word)
            print(emoji.emojize("You have run out of guesses! :frowning:", use_aliases=True))
            print "You incorrectly guessed %d letters" % len(missed_letters)
            print "The secret word was '%s'" % secret_word
            game_is_done = True

    if game_is_done is True:
        if playAgain():
            missed_letters = ''
            correct_letters = ''
            game_is_done = False
            secret_word = get_random_word(word_list)
        else:
            print(emoji.emojize("Goodbye! Have a wonderful day :sunny:", use_aliases=True))
            sys.exit()

#
# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)
#
# if __name__ == '__main__':
#     hello()
