#!/usr/bin/env python3
# coding: utf-8

from typing import Tuple
import pal_closure_module as pcm
from itertools import combinations
import math


# description:
    # takes spaces between attractor's positions one by one and checks the subfactors
    # starts from the shortest, once it isn't there, returns false
    # once it finds the factor crossing an attractor's position, it stores it in a dictionary

# checks whether a given set of positions is an attractor of the given word; if not, returns also the missing factor
def check_attractor(word: list, attr: list) -> Tuple[bool, list]:
    attr.sort()
    deduplicate(attr)
    start = 0
    factors = {}
    for i in range(0, len(attr)):
        if start != attr[i]:
            ok = False
            missing = []
            ok, missing = check_subfactors(start, attr[i]-1, word, attr, factors)
            if not ok:
                return False, missing
        start = attr[i]+1
    if len(word)-1 != attr[-1]:
        ok = False
        missing = []
        ok, missing = check_subfactors(attr[-1]+1, len(word)-1, word, attr, factors)
        if not ok:
            return False, missing
    return True, None
        
# check all subfactors of the given factor in the word, including start and end
def check_subfactors(start: int, end: int, word: list, attr: list, factors: dict) -> Tuple[bool, list]:
    for i in range(1, end-start+2): # goes through different lengths of factors
        for j in range(start, end+2-i):
            current = word[j:j+i]
            if str(current) not in factors.keys(): # if it is, it has been already checked before
                result = crosses_attractor(current, word, attr)
                if (result is not None):
                    factors[str(current)] = result
                else:
                    return False, word[j:j+i]
    return True, None
        
# returns which position in attractor is crossed by the given factor; if it is not, returns None
def crosses_attractor(factor: list, word: list, attr: list) -> int:
    for at in attr:
        if at not in range(len(word)):
            continue
        for i in range(max(0, at-len(word)+len(factor)), min(len(factor)-1, at)+1):
            is_in = True
            for j in range(0, len(factor)):
                if factor[j] != word[at-i+j]:
                    is_in = False
                    break
            if is_in:
                return at
    return None                 
    
def deduplicate(what: list) -> list:
    return list(dict.fromkeys(what))
    
def is_subfactor(subfactor: list, factor: list) -> bool:
    if len(subfactor) > len(factor):
        return False
    i = 0
    while (i+len(subfactor) <= len(factor)):
        is_subfactor = True
        for j in range(0, len(subfactor)):
            if subfactor[j] != factor[j+i]:
                is_subfactor = False
                break
        if is_subfactor:
            return True
        i+=1
    return False

# returns not only the palindromic closure-generated sequence but also the attractor as a list
def pal_attractor(dir: list, repeat=0, iters=10, develop=False) -> Tuple[list, list]:
    if repeat > len(dir): # check user input
        repeat = len(dir)
    attr = []
    seq = []
    lpp_index = [-1, -1] # two positions correspond to two-letter alphabet
    i = -1
    iter_count = 1
    while (iter_count <= iters and (i < len(dir)-1 or repeat > 0)):
        i = pcm.incr(i, repeat, len(dir)) # handles indexing in infinite sequence
        seq.append(dir[i])
        if (dir[i] != 0 and dir[i] != 1):
            print("Error: Unexpected character in directive sequence.")
            return None, None
        lpp_index[dir[i]] = len(seq)-1
        if dir[i] == 0 and lpp_index[1] > -1:
            seq.append(1)
            pcm.complete_from(seq, lpp_index[1])
        elif dir[i] == 1 and lpp_index[0] > -1:
            seq.append(0)
            pcm.complete_from(seq, lpp_index[0])
        attr = [lpp_index[0], lpp_index[1]]
        if (develop): # to print progress on screen
            print_attractor(seq, attr)
            print()
        iter_count += 1
    return seq, attr

# generates antipalindromic closure using longest antipalindromic prefix followed either by 0 or by 1, returns also the attractor
def antipal_attractor(dir, period=0, iters=10, develop=False) -> Tuple[list, list]:
    if(period > len(dir)):
        period = len(dir)
    seq = []
    lap_index = {} 
    attr = []
    i = -1
    iter_count = 1
    while (iter_count <= iters and (i < len(dir)-1 or period > 0)):
        i = pcm.incr(i, period, len(dir)) # handles indexing in infinite sequence
        seq.append(dir[i])
        to_index = len(seq)-1
        if dir[i] in lap_index:
            pcm.anticomplete_from(seq, len(seq)-lap_index[dir[i]]-2)
        else:
            pcm.anticomplete_from(seq, len(seq))
        lap_index[dir[i]] = to_index
        
        # we have the word and lap indexes, now we process the attractor
        attr = list(lap_index.values())
        if(len(lap_index.values()) == 1):
            attr.append(mirror(lap_index[dir[0]], len(seq)))
        else:
            attr.append(mirror(lap_index[0 if dir[0] == 1 else 1], len(seq)))
            
        if (develop): # to print progress on screen
            print_attractor(seq, attr)
            print()
        iter_count += 1

    return seq, attr

# returns the mirror position in the sequence, indexing from 0
def mirror(position: int, length: int) -> int:
    return length - position - 1;

# prints visually understandable sequence with underlined positions from the attractor
def print_attractor(seq: list, attr: list):
    for i in range (0, len(seq)):
        if i in attr:
            underline(str(seq[i]))
        else:
            print(seq[i], " ", end="")
    print()
            
def underline(text: str):
    print("\u0332", end="")
    print("\u0332".join(text), " ", end="")

# ------ functions for generating attractors ------ #

# finds the longest repeated factor in the word a returns its length
def longest_repeated_length(seq: list) -> int:
    longest = 1
    for i in range(len(seq)):
        for j in range(i+1, len(seq)):
            if longest >= len(seq)-j: # cannot obtain longer factor from this position
                break
            add = -1
            while seq[i+add+1] == seq[j+add+1]:
                add += 1
                if(add > len(seq)-j-2): # checks if the next round of comparison fits in the array range
                    break
            if add + 1 > longest:
                longest = add + 1
    return longest

# returns the number of distinct letters in the sequence
def number_of_letters(seq: list) -> int:
    chars = []
    for i in range(len(seq)):
        if seq[i] not in chars:
            chars.append(seq[i])
    return len(chars)

# generates all possible attractor candidates of the given size for word of length n, indexing from 0
def generate_subsets(size, n) -> list:
    positions_set = set(range(n))
    return list(combinations(positions_set, size))

# the attractor generator, returning the first (i.e. the smallest) found attractor using attractor checker
def get_smallest_attractor(seq) -> list:
    long_len = longest_repeated_length(seq)
    letters = number_of_letters(seq)
    lower_bound = max(math.floor(len(seq)/(long_len+1)), letters)
    for i in range(lower_bound, len(seq)+1):
        candidates = generate_subsets(i, len(seq))
        for candidate in candidates:
            if check_attractor(seq, list(candidate))[0]:
                return list(candidate)
    return []

# the given-size attractor generator, returning all attractors of the given size for the given word
def generate_size_attractors(seq, size) -> list:
    found = []
    long_len = longest_repeated_length(seq)
    letters = number_of_letters(seq)
    lower_bound = max(math.floor(len(seq)/(long_len+1)), letters)
    if size >= lower_bound:
        candidates = generate_subsets(size, len(seq))
        for candidate in candidates:
            if check_attractor(seq, list(candidate))[0]:
                found.append(list(candidate))
    return found