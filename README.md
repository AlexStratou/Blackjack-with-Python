# Blackjack-with-Python
Object oriented implementation of the popular card game, Blackjack, using the Python programming language.

## Description of the code
At this point, the point of the project is to create a simple object oriented manifestation of Blackjack using Python. The code (so far) consists of four .py files.
1. bj_components.py contains the definitions of classes that define the objects nessecary to play Blackjack i.e. cards, decks, players and dealers.
2. In blackjack.py, we define the Blackjack class that piecies the game together using objects of bj_components.py.
3. The play_blackjack.py file creates a Blackjack object with a set of user defined parameters and runs the game.
4. utils.py contains utilities that did not conceptually fit on any of the other files.

## Running the code
To test the code for yourself tune the parameters on play_blackjack.py at will, open a command prompt, go to the code's directory and simply run

```
python play_blackjack.py
```

## Screenshots
Some examplary screenshots.

![image](https://github.com/user-attachments/assets/f20d92ee-20a5-4f20-b8a3-1de5d13faff6) ![image](https://github.com/user-attachments/assets/06ec7100-9962-4120-a9b4-3d2963b2ea2c)

![image](https://github.com/user-attachments/assets/2dc118f5-9663-4bdc-ac81-5b2a432d6064) ![image](https://github.com/user-attachments/assets/08fa8b86-2dbe-40b4-80f2-584cccbdcb67)

![image](https://github.com/user-attachments/assets/363d5782-e60e-40da-bae7-f73b1179f40c) ![image](https://github.com/user-attachments/assets/976a0714-7e59-454d-a7af-527f1323304a)





## To-do list
Possible things to do now.
1. Add 'split' functionality when Player has two cards of the same value.
2. Add insurance when the dealer has a visible Ace at the start.
3. Add shortcuts for blackjacks. i.e. the player does not need to play if the dealer gets a blackjack etc.
4. Add bots. Maybe explore the statistics of bots with given strategies.
5. Add a history log that saves data from played games.
6. Add a "slow mode" functionality that uses ```time.sleep(delay)``` to make terminal output look smoother.







