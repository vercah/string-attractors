#!/usr/bin/env python3
# coding: utf-8

import bwt_module as bwt
from typing import Tuple
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="performs the Burrows-Wheeler transformation and returns the first and last column of the BW matrix")
    parser.add_argument("word", help="finite sequence, must be in quotation marks; e.g. '0010011'", type=str)
    args = parser.parse_args()
    return args

def get_word(user_arg: str) -> list:
    word = []
    for elem in user_arg:
        word.append(str(elem))
    return word

# main:
def main():  
    args = set_args()
    word = get_word(args.word)
   
    first, last = bwt.get_bwt(word)
    
    # visually pleasing output
    for i in range(len(first)):
        print(first[i], " ... ", last[i])

if __name__ == "__main__":
    main()
