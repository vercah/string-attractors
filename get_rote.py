#!/usr/bin/env python3
# coding: utf-8

import pal_closure_module as pc
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="generates Rote word given a Sturmian one, via XOR summing")
    parser.add_argument("sturmian", help="finite sturmian word over alphabet {0, 1}; e.g. '01001010010'", type=str)
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
    sturmian = get_word(args.sturmian)
    
    rote = pc.get_rote_from_sturmian(sturmian)
    print(rote)
    return rote

if __name__ == "__main__":
    main()
