#!/usr/bin/env python3
# coding: utf-8

from typing import Tuple
import pal_closure_module as pc
import argparse

# get arguments from commandline
def set_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="generate pseudostandard word using a given bisequence")
    parser.add_argument("dir_seq", help="directive sequence to generate from; can be either finite or infinite, must be in quotation marks; e.g. '00(10)'", type=str)
    parser.add_argument("clo_seq", help="sequence to determine which closure to use; can be either finite or infinite, must be in quotation marks; e.g. 'REE(RE)'", type=str)
    parser.add_argument("-d", "--develop", help="print also individual steps", action="store_true")
    parser.add_argument("-i", "--iters", help="number of iterations", type=int)
    args = parser.parse_args()
    return args

# parse dir_seq from commandline
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

# parse clo_seq from commandline
def get_clo_seq(user_arg: str) -> Tuple[list, int]:
    period = 0
    par = False
    clo = []
    for elem in user_arg:
        if elem == 'R':
            clo.append(0)
        if elem == 'E':
            clo.append(1)
        if par:
            period += 1
        if(par == False and elem == '('):
            par = True
        # anything else will be ignored
    return clo, period

def get_iters(user_arg: int, dir_period: int, clo_period: int, dir_len: int, clo_len: int) -> int:
    iters = user_arg
    if iters is None:
        if(dir_period == 0 or clo_period == 0):
                iters = min(dir_len, clo_len)
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
    
def print_clo_seq(clo: list, period: int):
    print("Closure sequence is: ", end="")
    n = len(clo)
    for i in range(0, n):
        if i == n-period:
            print("(", end=""),
        print('R' if clo[i] == 0 else 'E', end=""),
    if period > 0:
        print(")", end="")
        print(" = ", end="")
        for i in range(0, n-period):
            print('R' if clo[i] == 0 else 'E', end="")
        for i in range(0, 5):
            for j in range(n-period, n):
                print('R' if clo[j] == 0 else 'E', end="")
        if period>0:
            print("...", end="")
    print()

# main:
def main():
    args = set_args()
    dir, dir_period = get_dir_seq(args.dir_seq)
    clo, clo_period = get_clo_seq(args.clo_seq)
    iters = get_iters(args.iters, dir_period, clo_period, len(dir), len(clo))
    dev = args.develop
    
    if dev:
        print_dir_seq(dir, dir_period)
        print_clo_seq(clo, clo_period)
        
    done = pc.pseudostd_closure(dir, clo, dir_period, clo_period, iters, dev)
    if not dev and done is not None:
        print(*done)
    
if __name__ == "__main__":
    main()
