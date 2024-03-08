#!/usr/bin/env python3
# coding: utf-8

import attractor_module as am
import pal_closure as scr


# main:
def main():
    args = scr.set_args()
    dir, repeat = scr.get_dir_seq(args.dir_seq)
    iters = scr.get_iters(args.iters, repeat, len(dir))
    dev = args.develop
    
    if dev:
        scr.print_dir_seq(dir, repeat)    
        
    seq, attr = am.pal_attractor(dir, repeat, iters, dev)
    
    if dev:
        print("Attractor is: ", attr)
    
    if not dev and seq is not None:
        print(seq, attr)
        

if __name__ == "__main__":
    main()
