#!/usr/bin/env python3
# coding: utf-8

from typing import Tuple
import pal_closure_module as pc
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="generate word using palindromic closure of the given sequence")
    parser.add_argument("dir_seq", help="directive sequence to generate from, can be either finite or infinite, must be in quotation marks; e.g. '00(10)'", type=str)
    parser.add_argument("-d", "--develop", help="print also individual steps", action="store_true")
    parser.add_argument("-i", "--iters", help="number of iterations", type=int)
    args = parser.parse_args()
    return args

# parse dirSeq from commandline
def get_dir_seq(user_arg: str) -> Tuple[list, int]:
    period = 0
    par = False
    dir = []
    for elem in user_arg:
        try:
            dir.append(int(elem))
            if par:
                period += 1
        except ValueError:
            if elem == '(':
                par = True
        # anything else will be ignored
    return dir, period

def get_iters(user_arg: int, period: int, length: int) -> int:
    iters = user_arg
    if iters is None:
        if period == 0:
            iters = length
        else:
            iters = 10
    return iters

def print_dir_seq(dir: list, period: int):
    print("Directive sequence is: ", end="")
    n = len(dir)
    for i in range(0, n):
        if i == n-period:
            print("(", end=""),
        print(dir[i], end=""),
    if period > 0:
        print(")", end="")
        print(" = ", end="")
        for i in range(0, n-period):
            print(dir[i], end="")
        for i in range(0, 5):
            for j in range(n-period, n):
                print(dir[j], end="")
        if period>0:
            print("...", end="")
    print()

# main:
def main():
    args = set_args()
    dir, period = get_dir_seq(args.dir_seq)
    iters = get_iters(args.iters, period, len(dir))
    dev = args.develop
    
    if dev:
        print_dir_seq(dir, period)
        
    done = pc.pal_closure(dir, period, iters, dev)
    
    if not dev and done is not None:
        print(done)
        return(done)
    
if __name__ == "__main__":
    main()
