#!/usr/bin/env python3
# coding: utf-8

import attractor_module as am
from typing import Tuple
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="get the smallest possible set of positions forming an attractor of the given word")
    parser.add_argument("word", help="finite string, must be in quotation marks; e.g. '0010011'", type=str)
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

def main():  
    args = set_args()
    word = get_word(args.word)
    
    attractor = am.get_smallest_attractor(word)
    
    print(attractor)

if __name__ == "__main__":
    main()
