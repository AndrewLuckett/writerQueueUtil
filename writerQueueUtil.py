"""
Author: Andrew Luckett
License: CC-BY
Module name: WriteQueueUtil
Version 2

This module is a utility tool to allow safe sequential writes to disk
using an asynchronous function to improve performance
Write attempts will await the previous

Warning: Multiple processes calling this will incur write the write
nonsequential issues those processes would have by writing by themselves
"""
from multiprocessing import Process
from time import sleep

__proc = None

def addToQueue(path, *lines):
    """
Add to the write queue.
call as:
    addToQueue("Spam.txt", "line")
    addToQueue("Eggs.txt, "line1", "line2", "line3")
    addToQueue("Bacon.txt", *myListOfLines)
"""
    global __proc
    if __proc is not None:
        __proc.join()
    __proc = Process(target = __writerProcessFunc, args = (path, *lines))
    __proc.start()


def __writerProcessFunc(path, *lines):
    with open(path, mode = 'a') as file:
        for line in lines:
            file.write(str(line))


def waitUntilSafe():
    # Not strictly necessary unless you have other processes
    global __proc
    if __proc is not None:
        __proc.join()

