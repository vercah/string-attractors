#!/usr/bin/env python3
# coding: utf-8

import attractor_module as am
from typing import Tuple
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="generates all possible attractors of given size for given word")
    parser.add_argument("word", help="finite string, must be in quotation marks; e.g. '0010011'", type=str)
    parser.add_argument("size", help="positive integer size of the attractors to find", type=int)
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
    size = args.size
    
    attractors = am.generate_size_attractors(word, size)
    
    print(attractors)

if __name__ == "__main__":
    main()
