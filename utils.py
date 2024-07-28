# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 18:10:07 2024
Author: Alexandros Stratoudakis
e-mail: alexstrat4@gmail.com

Utilities used throughout the project

"""
from colorama import just_fix_windows_console  # for colored output on CMD
from typing import Any, Tuple

bj_vals = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
           'J': 10, 'Q': 10, 'K': 10}

suits_map = {'heart': '♥', 'diamond': '♦', 'spade': '♠', 'club': '♣'}
vals_map = {'1': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', '10': '10', '11': 'J', '12': 'Q', '13': 'K'}


def count_value(cards: list[object]) -> Tuple[int, bool]:
    """
    Function that calculates the Blackjack-value of a given hand of cards.

    Args:
        cards (list): List (or tuple) of bj_components.card objects.

    Returns:
        val (int): The BJ value of the hand.
        soft (bool): Whether or not this value is with one or more Aces counting as 11 (instead of 1).

    """
    val = 0
    aces = 0  # num of Aces
    ace_cnt = 0
    soft = False  # if all A=1 or there are no A, soft = False
    for card in cards:
        val += card.bj_value()
        if card.value == 'A':
            aces += 1
            ace_cnt += 1  # aces with val 11
        else:
            continue
    while val > 21 and ace_cnt != 0:
        val -= 10
        ace_cnt -= 1
    if ace_cnt != 0:
        soft = True
    return val, soft


actions = {'h': 'hit', 's': 'stay', 'd': 'double down', 'x': 'split'}

delay = 0.1  # print delay #TODO


class colors:

    # Taken from https://www.geeksforgeeks.org/print-colors-python-terminal/
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''

    just_fix_windows_console()   # to be compatible with CMD
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        al = ''
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'  # white


def is_numerical(a: Any) -> bool:
    """
    Args:
        a (Any): Any object.

    Returns:
        bool: True if input can be converted to float, False otherwise.

    """
    try:
        float(a)
    except:
        return False
    else:
        return True
