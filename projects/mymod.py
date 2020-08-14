#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:14:47 2017

@author: bmjl
"""

class Point:
    """This is Point class"""
    
    def __init__(self):
        """This is the Point constructur"""
        print("Point created")
        
    def hello(self):
        """Hello method"""
        print("Hello")

def hello_module():
    """Hello function"""
    print("Hello from mymod.")

if __name__ == "__main__":
    print("My module")