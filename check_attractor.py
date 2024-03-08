#!/usr/bin/env python3
# coding: utf-8

import attractor_module as am
from typing import Tuple
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="check whether the given set of position is an attractor of the word; if not, returns the missing factor")
    parser.add_argument("word", help="finite sequence, must be in quotation marks; e.g. '0010011'", type=str)
    parser.add_argument("attractor", help="set of positions (indexing from 0), must be in quotation marks separated by coma; e.g. '0,1,5'", type=str)
    parser.add_argument("-d", "--develop", help="print also individual steps", action="store_true")
    args = parser.parse_args()
    return args

def get_word(user_arg: str) -> list:
    word = []
    for elem in user_arg:
        try:
            word.append(int(elem))
        except ValueError:
            pass # ignores anything else than numbers
    return word

def get_attractor(user_arg: str) -> list:
    attr = []
    digits = []
    for elem in user_arg:
        try:
            digits.append(int(elem))
        except ValueError:
            if elem==',':
                number = 0
                for i in range(0, len(digits)):
                    number += digits[i]*(10**(len(digits)-1-i))
                attr.append(number)
                digits = []
    number = 0
    for i in range(0, len(digits)):
        number += digits[i]*(10**(len(digits)-1-i))
    attr.append(number)
    return attr

# main:
def main():  
    args = set_args()
    word = get_word(args.word)
    attr = get_attractor(args.attractor)
    dev = args.develop
    
    ok, factor = am.check_attractor(word, attr)
    
    if dev:
        print("word: ", word, ", attractor: ", attr)
    
    if ok:
        print("Yes")
    else:
        print("No, attractor does not cover ", factor)

if __name__ == "__main__":
    main()
