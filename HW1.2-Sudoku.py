"""
PKU, INTRODUCTION TO AI
LECTURE 5 - GLOBAL SEARCH - HW 02 - Sudoku

DESCRIPTION
Sudoku is a very simple task. A square table with 9 rows and 9 columns is divided to 9 smaller squares 3x3 as shown
on the Figure. In some of the cells are written decimal digits from 1 to 9. The other cells are empty. The goal is to
fill the empty cells with decimal digits from 1 to 9, one digit per cell, in such way that in each row, in each column
and in each marked 3x3 subsquare, all the digits from 1 to 9 to appear. Write a program to solve a given Sudoku-task.

INPUT
The input data will start with the number of the test cases. For each test case, 9 lines follow, corresponding to
the rows of the table. On each line a string of exactly 9 decimal digits is given, corresponding to the cells
in this line. If a cell is empty it is represented by 0.

OUTPUT
For each test case your program should print the solution in the same format as the input data. The empty cells
have to be filled according to the rules. If solutions is not unique, then the program may print any one of them.

SAMPLE INPUT
1
103000509
002109400
000704000
300502006
060000050
700803004
000401000
009205800
804000107

SAMPLE OUTPUT
143628579
572139468
986754231
391542786
468917352
725863914
237481695
619275843
854396127
"""


def find_number(num):
    global a, x, end_flag
    if num == 81:  # fill ended, get back
        end_flag = True
        return 'いいよ！こいよ！'
    if a[num] != 0:  # this blank[num] is already filled in the question, so go to blank[num+1]
        find_number(num + 1)
        return 'いいよ！こいよ！'  # if blank[num+1] can't be filled and blank[num] is already filled
        # in this question, return here.
    else:
        for k in range(9):  # put in k+1, not k!
            a[num] = k+1  # set blank[num] to k+1
            if row[num // 9][k]:  # can we fill this number(k+1) in this blank? If not,
                # clear the number and get back to blank[num-1]
                a[num] = 0
                continue
            if col[num % 9][k]:
                a[num] = 0
                continue
            if gong[num // 9 // 3 * 3 + num % 9 // 3][k]:
                a[num] = 0
                continue
            row[num // 9][k] = True  # if can, all occupy modes of blank[num] set to True
            col[num % 9][k] = True
            gong[num // 9 // 3 * 3 + num % 9 // 3][k] = True

            find_number(num + 1)  # fill in the next blank

            if not end_flag:  # if the the blank[num+1] can't be filled, return here in blank[num]
                a[num] = 0  # reset blank[num] to 0
                row[num // 9][k] = False  # clear the occupy modes of blank[num]
                col[num % 9][k] = False
                gong[num // 9 // 3 * 3 + num % 9 // 3][k] = False
            else:  # fill ended
                return 'いいよ！こいよ！'  # back to previous num, eventually ends the function


def solve():
    find_number(0)  # start filling from the first blank(blank[0] or a[0])
    return 'いいよ！こいよ！'


def print_sudoku(sudoku):  # convert the sudoku list to answer form
    for i in range(1, 10):
        print(''.join(map(str, sudoku[9 * (i - 1): 9 * i])))
    return 'いいよ！こいよ！'


n = int(input())
for i in range(n):
    end_flag = False
    x = []
    row = [[False for s in range(9)] for j in range(9)]  # row[i][j] means whether there's j+1 in the i+1-th row
    col = [[False for s in range(9)] for j in range(9)]  # the same for col and gong
    gong = [[False for s in range(9)] for j in range(9)]
    for j in range(9):
        x.extend(list(map(int, list(input()))))  # convert the sudoku to a list(81 long)
    for j in range(81):  # scan the list, if the a blank has been filled (x[j]!=0), set its all occupy modes to True.
        if x[j]:
            row[j // 9][x[j] - 1] = True
            col[j % 9][x[j] - 1] = True
            gong[j // 9 // 3 * 3 + j % 9 // 3][x[j] - 1] = True
    a = x.copy()
    solve()
    print_sudoku(a)


"""
note: Simple dfs algorithm. An ordinary Sudoku takes 0.9-100 ms.

Memory used: 4052 kB
Time used: 9380 ms
"""
