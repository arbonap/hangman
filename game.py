import click
import requests
from pprint import pprint
import json
import urllib2
import random
import sys

txt = urllib2.urlopen('http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words')
word_list = txt.read().split('\n')
print len(word_list)

HANGMANPICS = ['1', '2', '3', '4', '5', '6', '7']
def getRandomWord(wordList):
    random.shuffle(word_list)
    print word_list[0]
    return word_list[0]

def displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord):
    print(HANGMANPICS[len(missedLetters)])
    print()

    print('Missed letters:')
    for letter in missedLetters:
        print(letter)
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks:
        print(letter)
    print()

def getGuess(alreadyGuessed):

    while True:
        print('Guess a letter.')
        guess = raw_input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please only enter one letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter, please choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a letter.')
        else:
            return guess

def playAgain():
    print('Do you want to play again?')
    return input().lower().startswith('y')


print('H A N G M A N')
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(word_list)
gameIsDone = False

while True:
    displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord)

    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters += guess

        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Congratulations! The secret hangman word is ' + secretWord + '! You won!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        if len(missedLetters) >= 6:
            displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord)
            print("You have run out of guesses!")
            # print("Number of missed letters %d" % str(len(missedLetters))
            # print("The secret word was %s" % secretWord)
            gameIsDone = True

    if gameIsDone is True:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = getRandomWord(word_list)
        else:
            print "Goodbye!"
            sys.exit(1)

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
