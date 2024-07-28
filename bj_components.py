# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:09:45 2024
Author: Alexandros Stratoudakis
e-mail: alexstrat4@gmail.com

Module of classes that are essential to make the game.

TODO: Make bot player class, add split
"""

import random
import sys
from utils import bj_vals, count_value, actions, is_numerical, suits_map, vals_map
from utils import colors
bg = colors.bg
fg = colors.fg


class card():

    """ A class that represents a playing card."""

    def __init__(self, suit: str, value: str | int):
        """
        Initializer function of the card object.
        Args:
            suit (str): Card's suit ( one of '♥', '♦', '♠', '♣' or 'heart', 'diamond', etc)
            value (str | int): Card's value. ( can be 'A', '2', '3', '4', '5', '6', 
            '7', '8', '9', '10', 'J', 'Q', 'K' or int from 1 to 13)

        Raises:
            ValueError: If it cannot cast input to a known suit or value.

        Returns:
            None.

        """
        try:
            # figure wheather we are using '♥', '♦', '♠', '♣' by symbol or name
            suits_map[suit]
        except:
            self.suit = suit
        else:
            self.suit = suits_map[suit]

        try:
            # figure wheather we are using symbols or number for the values
            vals_map[str(value)]
        except:
            self.value = str(value)  # typecast if integer
        else:
            self.value = vals_map[str(value)]

        if (self.value not in vals_map.values()) or (self.suit not in suits_map.values()):
            raise ValueError('Incorrect suit or value.')

    def bj_value(self) -> int:
        """
        Method that return the BJ value of the card object.

        Returns:
            int: BJ value.

        """
        return bj_vals[self.value]

    def as_str(self, colored=True) -> str:
        """
        Method that returns the card objects specs as a string.

        Args:
            colored (bool, optional): Wheather we want a colored output. Defaults to True.

        Returns:
            str: playing card value and suit in a single string.

        """
        if colored == False:
            return self.suit + self.value
        if self.suit == '♥' or self.suit == '♦':
            color = fg.red + bg.lightgrey
        else:  # other suits
            color = fg.black + bg.lightgrey
        return color + self.suit + self.value + colors.reset


class deck():
    ''' Class that represents a playing cards deck'''

    def __init__(self, N_decks=1):
        """
        Initializer funtion for deck objects

        Args:
            N_decks (int, optional): Number of decks. Defaults to 1. Must be a
            positive integer. Defaults to 1.

        Raises:
            ValueError: If N_decks is not a positive integer.

        Returns:
            None.

        """
        if N_decks <= 0 or not isinstance(N_decks, int):
            raise ValueError('The number of decks must be a positive integer.')
        suits = ['♥', '♦', '♠', '♣']
        values = ['A', '2', '3', '4', '5', '6',
                  '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = []
        for n in range(N_decks):
            for suit in suits:
                for val in values:
                    self.cards.append(card(suit, val))

    def shuffle(self):
        """
        Method that shuffles the deck(s).

        Returns:
            None.

        """
        random.shuffle(self.cards)

    def draw(self, N_cards=1) -> card | list[card]:
        """
        Method that draws one or more card objects from a
        deck object.

        Args:
            N_cards (int, optional): How many cards to draw. Defaults to 1.

        Raises:
            ValueError: If N_cards is not a positive integer.

        Returns:
            card | list[card]: card object or list of card objects. The list is
            returned if N_cards>1.

        """
        if N_cards <= 0 or not isinstance(N_cards, int):
            raise ValueError('The number of cards must be a positive integer.')
        if N_cards == 1:
            return self.cards.pop()
        else:
            cds = []
            for j in range(N_cards):
                cds.append(self.cards.pop())
            return cds


class player():
    """Class that represents a (human) BJ player"""

    def __init__(self, player_cards: list[card], name: str):
        """
        Initializer function for player objects.

        Args:
            player_cards (list[card]): List of the initial player cards.
            name (str): Player's name.

        Returns:
            None.

        """

        self.player_cards = player_cards
        self.name = name
        self.action = None
        self.cash = None
        self.bet = None
        self.state = None
        self.value = None

    def play(self) -> str:
        """
        Method that prompts player to play his hand.

        Returns:
            str: Players action: 'stay', 'hit', 'double down', 'bust' or 'blackjack'

        TODO: add 'split' action.

        """
        print(self.name+"'s cards:")
        self.value, _ = count_value(self.player_cards)

        for c in self.player_cards:
            print(c.as_str(), end=colors.reset + ' ')
        print('total =', self.value)

        if self.action == 'double down':
            if self.value > 21:
                self.action = 'bust'
                print(self.name + ' busts at ' + str(self.value)+'!')
                print('--------------------------------------')
                return self.action
            else:
                self.action = 'stay'
                print(self.name + ' is forced to stay at', self.value)
                print('--------------------------------------')
                return self.action

        if self.value == 21 and len(self.player_cards) == 2:
            print('Blackjack for ' + self.name+'!')
            print('--------------------------------------')
            self.action = 'blackjack'
            return self.action

        if self.value > 21:
            self.action = 'bust'
            print(self.name + ' busts at ' + str(self.value)+'!')
            print('--------------------------------------')
            return self.action

        if (len(self.player_cards) == 2 and self.player_cards[0].value != self.player_cards[1].value) or len(self.player_cards) == 1:
            # different cards or single card after split
            tmp = input('Choose an action (h/s/d)\n')

            while tmp != 'h' and tmp != 's' and tmp != 'd' and tmp != 'exit':
                print(fg.orange + 'Invalid input...' +
                      colors.reset+'\nTry again,')
                tmp = input(
                    'Choose an action (h/s/d). Type "exit" to quit game.\n')
        elif len(self.player_cards) == 2 and self.player_cards[0].value == self.player_cards[1].value:
            # equal cards
            tmp = input('Choose an action (h/s/d/x)\n')

            while tmp != 'h' and tmp != 's' and tmp != 'exit' and tmp != 'd' and tmp != 'x':
                print(fg.orange + 'Invalid input...' +
                      colors.reset+'\nTry again,')
                tmp = input(
                    'Choose an action (h/s/d/x). Type "exit" to quit game.\n')
        else:
            tmp = input('Choose an action (h/s)\n')

            while tmp != 'h' and tmp != 's' and tmp != 'exit':
                print(fg.orange + 'Invalid input...' +
                      colors.reset+'\nTry again,')
                tmp = input(
                    'Choose an action (h/s). Type "exit" to quit game.\n')

        if tmp == 'exit':
            print('Quiting game...')
            sys.exit()
        self.action = actions[tmp]

        print(self.name + ' ' + self.action + 's on', self.value)
        print('--------------------------------------')
        return self.action

    def place_bet(self):
        """
        Method that prompts player to place his bet and checks for its
        validity.

        Returns:
            None.

        """
        valid_input = False

        while (valid_input == False):
            tmp = input("Please place your bet:\n"+fg.green + "$")
            if tmp == 'exit':
                print(colors.reset + "Quiting game...")
                sys.exit()
            print(colors.reset)

            numerical_input = is_numerical(tmp)
            positive_input = False
            enough_cash = False
            if numerical_input == True:

                if self.cash - float(tmp) < 0:
                    enough_cash = False
                    print(fg.orange + "Insufficient funds."+colors.reset+" You only have " +
                          fg.green + "$" + str(self.cash) + colors.reset + "...")
                elif float(tmp) <= 0:
                    positive_input = False
                    print(fg.orange + "Invalid input." + colors.reset +
                          " A bet has to be more than " + fg.green + '$0' + colors.reset)
                elif float(tmp) > 0:
                    positive_input = True
                    enough_cash = True

            else:
                print(fg.orange + "Invalid input." + colors.reset +
                      " Please enter a valid amount.")
            if numerical_input == True and positive_input == True and enough_cash == True:
                valid_input = True

        self.bet = float(tmp)
        self.cash = self.cash - self.bet


class dealer():
    ''' Class that represents the BJ Dealer.'''

    def __init__(self, dealer_cards: list[card]):
        """
        Initializer function for the dealer object.

        Args:
            dealer_cards (list[card]): List of initial cards.

        Returns:
            None.

        """

        self.hidden = dealer_cards[0]
        self.dealer_cards = dealer_cards
        self.action = None

    def play(self) -> str:
        """
        Method that playes the dealer's hand'

        Returns:
            str: Dealer's action: 'stay', 'hit', 'bust' or 'blackjack'

        """
        print("Dealer's cards:")
        self.value, self.soft = count_value(self.dealer_cards)

        for c in self.dealer_cards:
            print(c.as_str(), end=colors.reset + ' ')
        print('total =', self.value)

        if self.value == 21 and len(self.dealer_cards) == 2:
            self.action = 'blackjack'
            print('Blackjack for the Dealer!')
            print('--------------------------------------')
            self.action = 'blackjack'
            return self.action

        if self.value > 21:
            self.action = 'bust'
            print('Dealer busts at ' + str(self.value)+'!')
            print('--------------------------------------')
            return self.action
        if self.value > 17:
            self.action = 'stay'
        elif self.value <= 16:
            self.action = 'hit'
        elif self.value == 17:
            if self.soft == True:
                self.action = 'hit'
            else:
                self.action = 'stay'

        print("Dealer " + self.action+'s at ' + str(self.value))
        print('--------------------------------------')
        return self.action


class player_bot():
    """
    TODO
    """

    def __init__(self):
        pass


if __name__ == '__main__':
    pass
    card1 = card('heart', 3)
    card2 = card('club',3)
    cards = [card1, card2]
    Player = player(cards, 'Joe')
    Player.play()
