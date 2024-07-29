# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 20:53:15 2024
Author: Alexandros Stratoudakis
e-mail: alexstrat4@gmail.com

Module that implements the Blackjack game using the bj_components module.

TODO:  add a log, add insurance
"""
import bj_components as bj
import sys
from utils import colors, is_numerical, Mute, win_lose, slow_print
fg = colors.fg
bg = colors.bg


class Blackjack():
    ''' Object oriented implementation of blackjack. '''

    def __init__(self, num_decks: int, starting_cash: int | float,
                 name: str, game_delay='fast'):
        """
        Initializer for Blackjack object.

        Args:
            num_decks (int): Number of decks.
            starting_cash (int|float): Starting cash in $.
            name (str): Player name.
            game_delay (str, Optional): Delay, in seconds, after each print. Defaults to 'fast' (no delay)

        Raises:
            ValueError: If starting cash is not a valid number.

        Returns:
            None.

        """

        if is_numerical(starting_cash) == False:
            raise ValueError('Starting cash must be a number.')
        if starting_cash <= 0:
            raise ValueError('Starting cash must be a positive number.')
        if game_delay == 'fast':
            pass
        else:
            slow_print(delay=game_delay)

        self.num_decks = num_decks
        self.Deck = bj.deck(self.num_decks)
        self.Deck.shuffle()
        self.Round = 0

        self.Dealer = bj.dealer([None])
        self.Player = bj.player([None], name)
        self.Player.cash = starting_cash
       # self.Player.splitted = False
        # TODO: add bots here (maybe?)

    def play_round(self, splitted=False, verbose_dealer=True) -> int:
        """


        Args:
            splitted (bool, optional): If True, no initial deal happens. Defaults to False.
            verbose_dealer (bool, optional): If False, dealer's play gives no printed output. Defaults to True.

        Returns:
            int: 0,1,2, representin lose/win/push

        """
        def init_deal(Player: bj.player):
            if Player.cash <= 0:
                print('\n' + Player.name + ' is out of cash...\n' +
                      fg.red + 'Game Over!!!' + colors.reset)
                sys.exit()

            self.Round += 1
            Player.action = None  # reset participants
            self.Dealer.action = None

            print('______________________________________')
            print("Cash:" + fg.green + " $" + str(Player.cash) +
                  colors.reset + ', Round: ' + str(self.Round))
            Player.place_bet()
            self.Dealer.dealer_cards = self.Deck.draw(2)
            Player.player_cards = self.Deck.draw(2)

            print("Dealer has " +
                  self.Dealer.dealer_cards[1].as_str() + colors.reset+" and a hidden card.")
            print('--------------------------------------')

        if splitted == False:
            init_deal(self.Player)
        # TODO insurrance goes here
        # Player plays

        while self.Player.action != 'stay' and self.Player.action != 'blackjack' and self.Player.action != 'bust' and self.Player.action != 'split':
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
                    print(fg.orange + "Not enough cash to double down." + colors.reset + " You need " + fg.green + '$' + str(self.Player.bet) +
                          colors.reset + ' but only have' +
                          fg.green + " $" + str(self.Player.cash) + colors.reset + "...")
                    self.Player.action = None

        if self.Player.action == 'bust':
            print("Dealer wins!")
            print(self.Player.name + fg.red + ' loses' + colors.reset +
                  ' the bet of ' + fg.green + '$'+str(self.Player.bet) + colors.reset)
            self.Player.bet = 0
            return 0  # 0 = dealer wins

        elif self.Player.action == 'split':
            if self.Player.cash - self.Player.bet >= 0:

                self.Player.action = None
                self.Player.cash -= self.Player.bet
                print('\n'+self.Player.name + ' is playing their first hand.')

                init_bet = self.Player.bet
                self.Player.player_cards = [self.Player.player_cards[0]]
                hand1 = self.play_round(splitted=True, verbose_dealer=False)

                self.Player.player_cards = [self.Player.player_cards[1]]
                self.Dealer.dealer_cards = self.Dealer.dealer_cards[0:2]
                self.Dealer.action = None
                self.Player.action = None
                self.Player.bet = init_bet
                print('\n'+self.Player.name + ' is playing their second hand.')

                self.play_round(splitted=True)
                print('\r'+'on their second hand', end='')
                print(' and ' + win_lose[hand1] +
                      ' the same bet from the first hand.')
                self.Player.splitted = False

            else:
                print(fg.orange + "Not enough cash to split." + colors.reset + " You need " + fg.green + '$' + str(self.Player.bet) +
                      colors.reset + ' but only have' +
                      fg.green + " $" + str(self.Player.cash) + colors.reset + "...")
                self.Player.action = None
                self.Player.splitted = False
                self.play_round(splitted=True)  # True to not init deal again

        else:  # player stays or has a bj
            # dealer plays
            def dealer_play(Player: bj.player, Dealer: bj.dealer):
                print("\nDealer's hidden card is: " +
                      Dealer.dealer_cards[0].as_str() + colors.reset)
                print('--------------------------------------')
                while Dealer.action != 'stay' and Dealer.action != 'blackjack' and Dealer.action != 'bust':

                    Dealer.play()

                    if Dealer.action == 'hit':
                        Dealer.dealer_cards.append(self.Deck.draw())

                if Dealer.action == 'stay':
                    if Dealer.value > Player.value:

                        print('Dealer wins!')
                        print(Player.name + fg.red + ' loses' + colors.reset +
                              ' the bet of ' + fg.green + '$' + str(Player.bet) + colors.reset)
                        Player.bet = 0
                        return 0
                    elif Dealer.value < Player.value and Player.action != 'blackjack':

                        Player.bet = 2 * Player.bet
                        print(Player.name + fg.green + ' wins' + colors.reset +
                              '. The Dealer pays ' + fg.green+'$' + str(Player.bet) + colors.reset)
                        Player.cash += Player.bet

                        return 1  # player wins
                    elif Dealer.action != 'blackjack' and Player.action == 'blackjack':
                        Player.bet = (1 + 3/2) * Player.bet
                        print(Player.name + fg.green + ' wins' + colors.reset +
                              ' with a' + fg.purple + ' Blackjack!' + colors.reset + " The Dealer pays " + fg.green + '$' + str(Player.bet) + colors.reset)

                        Player.cash += Player.bet
                    elif Dealer.value == Player.value:
                        print(Player.name + ' and the Dealer' +
                              fg.cyan+' push.'+colors.reset)
                        Player.cash += Player.bet
                        return 2  # push

                elif Dealer.action == 'bust':
                    Player.bet = 2 * Player.bet
                    print(Player.name + fg.green + ' wins' + colors.reset +
                          '. The Dealer pays ' + fg.green+'$' + str(Player.bet) + colors.reset)

                    Player.cash += Player.bet
                    return 1  # player wins

                else:  # dealer has blackjack
                    if Player.action == 'blackjack':
                        print(Player.name + ' and the Dealer' +
                              fg.cyan+' push.'+colors.reset)
                        Player.cash += Player.bet
                        return 2  # push
                    else:  # player has no blackjack

                        print('Dealer wins!')
                        print(Player.name + fg.red + ' loses' + colors.reset +
                              ' the bet of ' + fg.green + '$' + str(Player.bet) + colors.reset)
                        Player.bet = 0
                        return 0

            if verbose_dealer == False:
                with Mute():
                    outcome = dealer_play(self.Player, self.Dealer)

                    return outcome
            else:
                outcome = dealer_play(self.Player, self.Dealer)
                return outcome


"""

@todo
class Blackjack2:
    def __init__(self, starting_cash=1000, name='Alex', human_player=True, N_decks=8, N_bots=0, strategies=None):
        if is_numerical(starting_cash) == False:
            raise ValueError('Starting cash must be a number.')
        if starting_cash <= 0:
            raise ValueError('Starting cash must be a positive number.')

        self.num_decks = N_decks
        self.Deck = bj.deck(self.num_decks)
        self.Deck.shuffle()
        self.Round = 0
        self.Dealer = bj.dealer([None])
        
        self.Bots = []
        
        for i in range(N_bots):

            self.Bots.append(bj.player_bot())  
        
        if human_player == True:
            
            self.Player = bj.player([None], name)
            self.Player.cash = starting_cash
            self.Players = self.Bots.insert(0, self.Player)
        
        

        

    def init_deal(self):
        self.Round += 1
        for Player in self.Players:
            if Player.cash <= 0:
                print('\n' + Player.name + ' is out of cash...\n' +
                      fg.red + 'Game Over!!!' + colors.reset)
                sys.exit()
            Player.action = None  # reset participants
        self.Dealer.action = None

        print('______________________________________')
        print("Cash:" + fg.green + " $" + str(Player.cash) +
              colors.reset + ', Round: ' + str(self.Round))
        Player.place_bet()
        self.Dealer.dealer_cards = self.Deck.draw(2)
        Player.player_cards = self.Deck.draw(2)

        print("Dealer has " +
              self.Dealer.dealer_cards[1].as_str() + colors.reset+" and a hidden card.")
        print('--------------------------------------')

    def player_play(Player: bj.player):
        pass

    def dealer_play(Dealer: bj.dealer):
        pass

    def play_round(Dealer: bj.dealer, Players: list[bj.player | bj.player_bot]):
        pass
"""
