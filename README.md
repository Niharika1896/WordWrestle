# WordWrestle
*__Input Received:__*\
The server will send the following information to the clients at the start of the game:
- server_word: The current root word on display in the game (Initially, if I am going first, this will be the rootword given by the server)
- words_played: list of all the words played by all the players so far in the order that the words were played
- turnsleft: Number of my turnsleft before the game gets over
- total_rounds: The total number of rounds to be played.
- turn: 1/2

*__Return Value:__*\
Powers used - List(String)\
The next words to play - List(String

*__Special Powers Dictionary:__*\
gotwice = 1\
flip = 1\
remove = 1\
mirror = 1
  
*__Rules:__*\
There are 4 power cards:
1. GoTwice - Player can play 2 turns
2. Flip - Reverse the server word and play a turn
3. Remove - Remove the last letter and play a turn
4. Mirror - Change b's to d's, w's to m's and vice versa and play a turn/ 

- The clients should ensure that they do not use the same power twice. They will be asked to make another play in case of violation.
- Here, playing a turn means submitting a word to play next. 
- A player can play one of the 4 power moves (at most once) or none at all. 
- The GoTwice card cannot be played by itself. You need to play NoPower/Flip/Remove/Mirror first and then play GoTwice.


Example:
  In every round, each player will be given the current server word, a list of all the words that have been played so far 
  (including the initial server word- there are no repetitions allowed), number of turns left for the player, 
  total number of rounds in the game and if the player goes first or second. The player has to send the powers they are using and the corresponding word. 
  For example:
  - In one turn, I 'flip' the server word and play a word 'batman'. I should return ['flip'],['batman'].
  - In one turn, I do not use any power, play a word 'thunder' and then decide to play my 'goTwice' card, and play 'error'. I should return ['nopower','gotwice'], ['thunder', 'error'].
  
*__Sample Round:__*\
SERVER WORD:    concurrent

_______________________________________________Round  1 _______________________________________________\
Player1: Power Used -  remove   | Word Played -  current   | Points Gained -  36   | Player1 Score -  36\
SERVER WORD:    concurrent\
Player2: Power Used -  nopower   | Word Played -  rental   | Points Gained -  16   | Player2 Score -  16\
SERVER WORD:    concurrental\
Player2: Power Used -  gotwice   | Word Played -  talk   | Points Gained -  9   | Player2 Score -  25\
SERVER WORD:    concurrentalk\

_______________________________________________Round  2 _______________________________________________\
Player1: Power Used -  nopower   | Word Played -  talky   | Points Gained -  16   | Player1 Score -  52\
SERVER WORD:    concurrentalky\
Player2: Power Used -  remove   | Word Played -  talkie   | Points Gained -  16   | Player2 Score -  41\
SERVER WORD:    concurrentalkie

