#!/usr/bin/env python3
# coding: utf-8

import csv
import attractor_module as am
import pal_closure_module as pc
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="given a binary directive sequence, generates sturmian and corresponding rote word and outputs their attractors of size 2 that share similar positions")
    parser.add_argument("dir_seq", help="binary directive sequence over the alphabet {0, 1}; e.g. '0010011'", type=str)
    parser.add_argument("-v", "--verbal", help="write also individual words and their attractors", action="store_true")

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
    filename = 'sturmian-rote.tsv'

    args = set_args()
    dir_seq = get_word(args.dir_seq)
    verb = args.verbal
    sturmian = pc.pal_closure(dir_seq)
    stu_attrs = am.generate_size_attractors(sturmian, 2)
    rote = pc.get_rote_from_sturmian(sturmian)
    rote_attrs = am.generate_size_attractors(rote, 2)
    
    similar = pc.compare_attrs(stu_attrs, rote_attrs)

    if verb:
        print("sturmian:", "\n", *sturmian)
        print("rote", "\n", *rote)
        print("similar attractors:")
    print(similar)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([dir_seq, sturmian, stu_attrs, rote, rote_attrs, similar])

    return similar

if __name__ == "__main__":
    main()

