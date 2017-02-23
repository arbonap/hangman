Assuming you have Python 2 or 3 installed on your machine,
`sudo pip install virtualenv` to install a Virtual Environment for your dependencies.
It is highly recommended to do this instead of polluting your computer's global namespace.
After `pip install`ing, run:
- `virtualenv venv`
- `source venv/bin/activate` to activate your Virtual Environment.
- `pip install requirements.txt`

Run `python game.py` to run Hangman Game!
There are two difficulty modes, `easy` and `hard`.

Feel free to `python game.py --easy` for `easy` mode to try and guess more commonplace words,
and `python game.py --hard` if you want to guess a challenging word.

Once finished with the game, remember to `deactivate` your virtualenv (`venv`).
Have fun!
