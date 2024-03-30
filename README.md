The program contains three classes (with pretty self-explanatory names):

- game.py: runs n games of Wordle coordinating the other two classes and keeps track of the scores.

- wordle.py: implements the game of Wordle, from choosing the word to guess to checking the correctness of a guess.

- guesser.py: produces a guess word.

You also have a list of ~4K words along with their frequency in a corpus in a tab-separated file (and in yaml format).

Game creates a new guesser object for every run. 

You can run 10 games of Wordle with the following command:

   python game.py --r 10

When you run it, program will output some stats about your success rate. 
