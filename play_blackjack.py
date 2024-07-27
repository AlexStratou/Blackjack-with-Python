# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:09:45 2024
Author: Alexandros Stratoudakis
e-mail: alexstrat4@gmail.com

"""
from blackjack import Blackjack

#---------Parameters----------#
player_name = 'Alex'
number_of_decks = 8
starting_cash = 1000.0
play_speed = 'fast' #TODO
#-----------------------------#

if __name__ == '__main__':
    BJ = Blackjack(number_of_decks, starting_cash,  player_name)
    while (True):
        BJ.play_round()
        
        