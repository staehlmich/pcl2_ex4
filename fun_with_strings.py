#!/usr/bin/env python3
# coding: utf8
# Author: Michael Staehli

from typing import Iterable
import numpy as np

def longest_substrings(x: str, y: str) -> Iterable[str]:
    """

    :param x:
    :param y:
    :return:
    """
    pass

def _calc_edit_distance_table(source, target):
    """
    calculate the table for edit-distance
    Params:
        source: sequence
        target: sequence
    Return:
        d: 2D list
        m: int, source length
        n: int, target lenth
    """
    m = len(source)
    n = len(target)
    d = [[0 for _ in range(n+1)] for _ in range(m+1)]
    d[0][0] = 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if source[i-1].lower() == target[j-1].lower():
                d[i][j] = 1
                if source[i-2].lower() == target[j-2].lower():
                    d[i][j] = d[i - 1][j - 1] + 1
            else:
                d[i][j] = 0
    return d, m, n

#Idea: I have to get the max of the table and traverse it backwards until 0 is reached.
#Maybe it is also useful to use numpy arrays.

def get_max_table(table):
    """

    :param table:
    :return:
    """
    pass
def _calc_edit_distance_table2(source, target):
    """
    calculate the table for edit-distance
    Params:
        source: sequence
        target: sequence
    Return:
        d: 2D list
        m: int, source length
        n: int, target lenth
    """
    m = len(source)
    n = len(target)
    d = [[None for _ in range(n+1)] for _ in range(m+1)]
    d[0][0] = 0
    for i in range(1, m+1):
        d[i][0] = d[i-1][0] + 1     # fill first column
    for j in range(1, n+1):
        d[0][j] = d[0][j-1] + 1     # fill first row
    for i in range(1, m+1):
        for j in range(1, n+1):
            d[i][j] = min(
                d[i-1][j] + 1,   # del
                d[i][j-1] + 1,   # ins
                d[i-1][j-1] + (1 if source[i-1] != target[j-1] else 0)  # sub
                )
    return d, m, n

def _get_operations(table, m, n):
    """
    get the edit-operatinos necessary to take the shortest path in edit-dist table
    Params:
        table: 2D list
        m: int, length of source
        n: int, length of target
    Return:
        list of strings
    """
    codes = []

    while True:
        cur = table[m][n]       # get value of current position
        if m == 0 and n == 0:   # if at upper left corner
            break
        elif m == 0:            # if at top row
            codes.append('I')
            n -= 1
        elif n == 0:            # if at leftmost column
            codes.append('D')
            m -= 1
        else:
            # if not at a table border check values of three possible cells
            up_left = table[m-1][n-1]
            up = table[m-1][n]
            left = table[m][n-1]
            # find cell with min value and move to that cell
            if up_left <= up and up_left <= left:
                if cur == up_left:      # if values equal, no operatino was made
                    codes.append('E')
                else:                   # else a substitution was made
                    codes.append('S')
                m -= 1
                n -= 1
            elif up <= left and up <= up_left:
                codes.append('D')
                m -= 1
            elif left <= up and left <= up_left:
                codes.append('I')
                n -= 1
    return codes[::-1]  # reverse the codes into reading order

def opcodes(source, target):
    """
    Get a list of edit operations for converting source into target.
    Params:
        source: sequence
        target: sequence
    Return:
        list of strings
    """
    table, m, n = _calc_edit_distance_table(source, target)
    codes = _get_operations(table, m, n)
    return codes

def align_pretty(source, target):
    """
    Pretty-print the alignment of two sequences of strings.
    Params:
        source: sequence
        target: sequence
        outfile: file-like object
    """
    i, j = 0, 0
    lines = [[] for _ in range(4)]  # 4 lines: source, bars, target, codes
    for code in opcodes(source, target):
        # code = code[0].upper()
        s, t = source[i-1], target[j-1]
        if code == 'D':  # sDeletion: empty string on the target side
            t = '*'
        elif code == 'I':  # Insertion: empty string on the source side
            s = '*'
        elif code == 'E':  # Equal: omit the code
            code = ' '

        # Format all elements to the same width.
        width = max(len(x) for x in (s, t, code))
        for line, token in zip(lines, [s, '|', t, code]):
            line.append(token.center(width))  # pad to width with spaces

        # Increase the counters depending on the operation.
        if code != 'D':  # proceed on the target side, except for deletion
            j += 1
        if code != 'I':  # proceed on the source side, except for insertion
            i += 1

    # Print the accumulated lines.
    for line in lines:
        print(line)

def main():
    source = "Kleistermasse"
    target = "Meisterklasse"
    d,n,m = _calc_edit_distance_table(source, target)
    for line in d:
        print(line)
    print("\n")
    print(opcodes(source, target))
    align_pretty(source, target)
    # a = np.array(d)
    # print(np.where(a== np.amax(a)))
if __name__ == '__main__':
    main()