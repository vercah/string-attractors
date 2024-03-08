#!/usr/bin/env python3
# coding: utf-8

from typing import Tuple
from functools import cmp_to_key

# returns first and last column of the Burrows-Wheeler transformation matrix
def get_bwt(word: list) -> Tuple[list, list]:
    word.append('$')
    bwm = get_bwm(word)
    first = [bwm[i][0] for i in range(len(word))] # gets the first char of each row
    bwt = [bwm[i][-1] for i in range(len(word))] # gets the last char of each row
    return first, bwt

# returns B-W matrix sorted
def get_bwm(word: list) -> list:
    bwm = create_bwm(word)
    bwm = sorted(bwm, key=cmp_to_key(compare))
    return bwm

# custom function to compare lists of strings using the priority of '$'
def compare(a: list, b: list) -> int:
    cut = min(len(a), len(b))
    i = 0
    while i < cut:
        if a[i] == b[i]:
            i += 1
        else:
            if a[i] == '$' or str(a[i]) < str(b[i]):
                return -1
            return 1
    if len(a) == len(b):
        return 0
    return 1 if len(a) > len(b) else -1 # case one is prefix of the other
        
# generates B-W matrix unsorted
def create_bwm(word: list) -> list:
    matrix = []
    for i in range(len(word)):
        rotation = []
        for j in range(len(word)):
            if i + j < len(word)-1:
                rotation.append(word[i+j])
            else:
                rotation.append(word[i+j-len(word)])
        matrix.append(rotation)
    return matrix
