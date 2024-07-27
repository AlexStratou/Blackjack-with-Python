# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 20:53:15 2024
Author: Alexandros Stratoudakis
e-mail: alexstrat4@gmail.com

Module that implements the Blackjack game using the bj_components module.

TODO: add split, slow mode, add a log, add insurance
"""
import time  # TODO add slow mode
import bj_components as bj
import sys
from utils import colors, is_numerical
fg = colors.fg
bg = colors.bg


class Blackjack():
    ''' Object oriented implementation of blackjack. '''

    def __init__(self, num_decks: int, starting_cash: int | float,
                 name: str):
        """
        Initializer for Blackjack object.

        Args:
            num_decks (int): Number of decks.
            starting_cash (int|float): Starting cash in $.
            name (str): DESCRIPTION.

        Raises:
            ValueError: DESCRIPTION.

        Returns:
            None.

        """

        if is_numerical(starting_cash) == False:
            raise ValueError('Starting cash must be a number.')
        if starting_cash <= 0:
            raise ValueError('Starting cash must be a positive number.')

        self.num_decks = num_decks
        self.Deck = bj.deck(self.num_decks)
        self.Deck.shuffle()
        self.Round = 0

        self.Dealer = bj.dealer([None])
        self.Player = bj.player([None], name)
        self.Player.cash = starting_cash

        # TODO: add bots here (maybe?)

    def play_round(self):
        if self.Player.cash <= 0:
            print('\n' + self.Player.name + ' is out of cash...\n' +
                  fg.red + 'Game Over!!!' + colors.reset)
            sys.exit()

        self.Round += 1
        self.Player.action = None  # reset participants
        self.Dealer.action = None

        print('______________________________________')
        print("Cash:" + fg.green + " $" + str(self.Player.cash) +
              colors.reset + ', Round: ' + str(self.Round))
        self.Player.place_bet()
        self.Dealer.dealer_cards = self.Deck.draw(2)
        self.Player.player_cards = self.Deck.draw(2)

        print("Dealer has " +
              self.Dealer.dealer_cards[1].as_str() + colors.reset+" and a hidden card.")
        print('--------------------------------------')

        # TODO insurrance goes here

        while self.Player.action != 'stay' and self.Player.action != 'blackjack' and self.Player.action != 'bust':
            self.Player.play()
            if self.Player.action == 'hit':
                self.Player.player_cards.append(self.Deck.draw())

            elif self.Player.action == 'double down':
                self.Player.cash -= self.Player.bet

                if self.Player.cash >= 0:
                    self.Player.bet = 2 * self.Player.bet
                    self.Player.player_cards.append(self.Deck.draw())
                    self.Player.play()
                else:
                    self.Player.cash += self.Player.bet   # return money to wallet
                    print(fg.orange + "Not enough cash to double down."+colors.reset + " You need " + fg.green + '$' + str(self.Player.bet) +
                          colors.reset + ' but only have' +
                          fg.green + " $" + str(self.Player.cash) + colors.reset + "...")
                    self.Player.action = None

        if self.Player.action == 'bust':
            print("Dealer wins!")
            print(self.Player.name + fg.red + ' loses' + colors.reset +
                  ' the bet of ' + fg.green + '$'+str(self.Player.bet) + colors.reset)
            self.Player.bet = 0
            return 0  # 0 = dealer wins
        else:  # player stays or has a bj

            print("\nDealer's hidden card is: " +
                  self.Dealer.dealer_cards[0].as_str() + colors.reset)
            print('--------------------------------------')
            while self.Dealer.action != 'stay' and self.Dealer.action != 'blackjack' and self.Dealer.action != 'bust':
                self.Dealer.play()
                if self.Dealer.action == 'hit':
                    self.Dealer.dealer_cards.append(self.Deck.draw())

            if self.Dealer.action == 'stay':
                if self.Dealer.value > self.Player.value:

                    print('Dealer wins!')
                    print(self.Player.name + fg.red + ' loses' + colors.reset +
                          ' the bet of ' + fg.green + '$' + str(self.Player.bet) + colors.reset)
                    self.Player.bet = 0
                    return 0
                elif self.Dealer.value < self.Player.value and self.Player.action != 'blackjack':

                    self.Player.bet = 2 * self.Player.bet
                    print(self.Player.name + fg.green + ' wins' + colors.reset +
                          '. The Dealer pays ' + fg.green+'$' + str(self.Player.bet) + colors.reset)
                    self.Player.cash += self.Player.bet

                    return 1  # player wins
                elif self.Dealer.action != 'blackjack' and self.Player.action == 'blackjack':
                    self.Player.bet = (1 + 3/2) * self.Player.bet
                    print(self.Player.name + fg.green + ' wins' + colors.reset +
                          ' with a' + fg.purple + ' Blackjack!' + colors.reset + " The Dealer pays " + fg.green + '$' + str(self.Player.bet) + colors.reset)

                    self.Player.cash += self.Player.bet
                elif self.Dealer.value == self.Player.value:
                    print(self.Player.name + ' and the Dealer' +
                          fg.cyan+' push.'+colors.reset)
                    self.Player.cash += self.Player.bet
                    return 2  # push

            elif self.Dealer.action == 'bust':
                self.Player.bet = 2 * self.Player.bet
                print(self.Player.name + fg.green + ' wins' + colors.reset +
                      '. The Dealer pays ' + fg.green+'$' + str(self.Player.bet) + colors.reset)

                self.Player.cash += self.Player.bet
                return 1  # player wins

            else:  # dealer has blackjack
                if self.Player.action == 'blackjack':
                    print(self.Player.name + ' and the Dealer' +
                          fg.cyan+' push.'+colors.reset)
                    self.Player.cash += self.Player.bet
                    return 2  # push
                else:  # player has no blackjack

                    print('Dealer wins!')
                    print(self.Player.name + fg.red + ' loses' + colors.reset +
                          ' the bet of ' + fg.green + '$' + str(self.Player.bet) + colors.reset)
                    self.Player.bet = 0
                    return 0
