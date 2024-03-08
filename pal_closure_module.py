#!/usr/bin/env python3
# coding: utf-8

# This module contains palindromic, antipalindromic and pseudostandard closure, also the Rote generator from Sturmian

from typing import Tuple

# generates palindromic closure using longest palindromic prefix for any alphabet
def pal_closure(dir, period=0, iters=100, develop=False) -> list:
    if period > len(dir):
        period = len(dir)
    seq = []
    lpp_index = {} # we don't know which letters are there in the word yet
    i = -1
    iter_count = 1
    while (iter_count <= iters and (i < len(dir)-1 or period > 0)):
        i = incr(i, period, len(dir)) # handles indexing in infinite sequence
        seq.append(dir[i])
        to_index = len(seq)-1
        if dir[i] in lpp_index:
            complete_from(seq, len(seq)-lpp_index[dir[i]]-2)
        else:
            complete_from(seq, len(seq)-1)
        lpp_index[dir[i]] = to_index
        if (develop): # to print progress on screen
            print(*seq)
            print("- - - - - - -")
        iter_count += 1
    return seq

# generates antipalindromic closure using longest antipalindromic prefix followed either by 0 or by 1
def antipal_closure(dir, period=0, iters=100, develop=False) -> list:
    if period > len(dir):
        period = len(dir)
    seq = []
    lpp_index = {} 
    i = -1
    iter_count = 1
    while (iter_count <= iters and (i < len(dir)-1 or period > 0)):
        i = incr(i, period, len(dir)) # handles indexing in infinite sequence
        seq.append(dir[i])
        to_index = len(seq)-1
        if dir[i] in lpp_index:
            anticomplete_from(seq, len(seq)-lpp_index[dir[i]]-2)
        else:
            anticomplete_from(seq, len(seq))
        lpp_index[dir[i]] = to_index
        if (develop): # to print progress on screen
            print(*seq)
            #print(lpp_index)
            print("- - - - - - -")
        iter_count += 1
    return seq

# generates pseudopalindromic closure using longest palindromic and antipalindromic prefixes followed either by 0 or by 1
def pseudostd_closure(dir, clo, dir_period=0, clo_period=0, iters=10, develop=False) -> list:
    if dir_period > len(dir):
        dir_period = len(dir)
    if clo_period > len(clo):
        clo_period = len(clo)
    seq = []
    lap_index = {} # longest antipalindromic prefix
    lpp_index = {} # longest palindromic prefix
    dir_index = 0
    clo_index = 0
    prev_clo = clo[0]
    
    # first iteration has to be done separately because it's special
    seq.append(dir[0])
    lap_index[dir[0]] = 0 # have to add zero length word as the longest prefix for both
    lpp_index[dir[0]] = 0 
    if(clo[0] == 1): # if the first closure is antipalindromic, some lpp appears from the closure
        seq.append(0 if seq[0] == 1 else 1)
        lpp_index[0 if dir[0] == 1 else 1] = 1
    iter_count = 2
    if (develop): # to print progress on screen
            print(*seq)
            print("- - - - - - -")
    
    # other iterations
    while (iter_count <= iters and (dir_index < len(dir)-1 or dir_period > 0) and (clo_index < len(dir)-1 or clo_period > 0)):
        dir_index = incr(dir_index, dir_period, len(dir))
        clo_index = incr(clo_index, clo_period, len(clo))
        seq.append(dir[dir_index])
        to_index = len(seq)-1
        
        if(prev_clo == 0): # previous closure was palindromic
            if(clo[clo_index] == 0): # current closure is palindromic
                if(dir[dir_index] in lpp_index):
                    complete_from(seq, len(seq)-lpp_index[dir[dir_index]]-2)
                else:
                    complete_from(seq, len(seq)-1)
            else: # current closure is antipalindromic
                the_other = 0 if dir[dir_index] == 1 else 1
                if(the_other in lap_index):
                    anticomplete_from(seq, len(seq)-lap_index[the_other]-2)
                else:
                    anticomplete_from(seq, len(seq))
            lpp_index[dir[dir_index]] = to_index
            
        else: # previous closure was antipalindromic
            if(clo[clo_index] == 0): # current closure is palindromic
                the_other = 0 if dir[dir_index] == 1 else 1
                if(the_other in lpp_index):
                    complete_from(seq, len(seq)-lpp_index[the_other]-2)
                else:
                    complete_from(seq, len(seq)-1)
            else: # current closure is antipalindromic
                if(dir[dir_index] in lap_index):
                    anticomplete_from(seq, len(seq)-lap_index[dir[dir_index]]-2)
                else:
                    anticomplete_from(seq, len(seq))
            lap_index[dir[dir_index]] = to_index
        if (develop): # to print progress on screen
            print(*seq)
            print("- - - - - - -")
        iter_count += 1
        prev_clo = clo[clo_index]
    return seq

# handles incrementing index for both finite and infinite sequences
# if repeat = 0, throws index out of the array range! TODO?
def incr(i: int, repeat: int, size: int) -> int:
    if (i < size - 1):
        return i+1
    return size - repeat  

# completes sequence to palindromic given the position of the longest palindromic prefix
def complete_from(seq: list, position: int) -> list:
    index = position-1
    while index != -1:
        seq.append(seq[index])
        index -= 1
    return seq

# completes sequence to antipalindromic given the position of the longest palindromic prefix
def anticomplete_from(seq, position):
    index = position-1
    while index > -1:
        seq.append(0 if seq[index] == 1 else 1)
        index -= 1
    return seq

# given sum modulo 2 and first summand, returns the other summand such that the given sum is obtained; expects binary input
def get_summand(fst_summand, sum):
    return sum ^ fst_summand

# given sturmian word, outputs corresponding Rote starting with 0 using the XOR connection
def get_rote_from_sturmian(sturmian):
    rote = [0]
    for i in range(len(sturmian)):
        rote.append(get_summand(rote[i], sturmian[i]))
    return rote

# compares two lists of attractors, outputs those with same length and similar positions (admits additive factor up to 1)
def compare_attrs(fst_attrs, snd_attrs):
    similar = [] # list of pairs of similar attractors

    for fst_attr in fst_attrs:
        for snd_attr in snd_attrs:
            if (len(fst_attr) == len(snd_attr)):
                fst_attr.sort()
                snd_attr.sort()
                sim_flag = True
                for i in range(len(fst_attr)):
                    if abs(fst_attr[i] - snd_attr[i]) > 1:
                        sim_flag = False
                        break
                if sim_flag:
                    similar.append((fst_attr, snd_attr))

    return similar
