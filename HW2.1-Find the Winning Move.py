"""
PKU, INTRODUCTION TO AI
LECTURE 6 - ADVERSARIAL SEARCH - HW 01 - Find the Winning Move

Total TL: 30000 ms (for Python)
ML: 65536 kB

DESCRIPTION
4x4 tic-tac-toe is played on a board with four rows (numbered 0 to 3 from top to bottom) and four columns (numbered
0 to 3 from left to right). There are two players, x and o, who move alternately with x always going first.
The game is won by the first player to get four of his or her pieces on the same row, column, or diagonal. If the board
is full and neither player has won then the game is a draw.
Assuming that it is x's turn to move, x is said to have a forced win if x can make a move such that no matter
what moves o makes for the rest of the game, x can win. This does not necessarily mean that x will win on the
very next move, although that is a possibility. It means that x has a winning strategy that will guarantee an
eventual victory regardless of what o does.

Your job is to write a program that, given a partially-completed game with x to move next, will determine
whether x has a forced win. You can assume that each player has made at least two moves, that the game has
not already been won by either player, and that the board is not full.

INPUT
The input contains one or more test cases, followed by a line beginning with a dollar sign that signals
the end of the file. Each test case begins with a line containing a question mark and is followed by
four lines representing the board; formatting is exactly as shown in the example. The characters used
in a board description are the period (representing an empty space), lowercase x, and lowercase o.
For each test case, output a line containing the (row, column) position of the first forced win for x,
or '#####' if there is no forced win. Format the output exactly as shown in the example.

OUTPUT
For this problem, the first forced win is determined by board position, not the number of moves required
for victory. Search for a forced win by examining positions (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), ...,
(3, 2), (3, 3), in that order, and output the first forced win you find. In the second test case below,
note that x could win immediately by playing at (0, 3) or (2, 0), but playing at (0, 1) will still ensure
victory (although it unnecessarily delays it), and position (0, 1) comes first.

SAMPLE INPUT
?
....
.xo.
.ox.
....
?
o...
.ox.
.xxx
xooo
$

SAMPLE OUTPUT
#####
(0,1)
"""


def check(board):  # returns 1 if 1/x wins, -1 if 2/o wins, else 0
    for i in range(4):  # check rows
        row = board[4*i:4*i+4]
        if row == [1, 1, 1, 1]:
            return 1
        if row == [2, 2, 2, 2]:
            return -1
    for i in range(4):  # check columns
        column = board[i::4]
        if column == [1, 1, 1, 1]:
            return 1
        if column == [2, 2, 2, 2]:
            return -1
    left_diag = board[0:16:5]  # check diags
    if left_diag == [1, 1, 1, 1]:
        return 1
    if left_diag == [2, 2, 2, 2]:
        return -1
    right_diag = board[3:13:3]
    if right_diag == [1, 1, 1, 1]:
        return 1
    if right_diag == [2, 2, 2, 2]:
        return -1
    return 0


def check_forced_win(board, dep, alpha, beta):  # analyze the first step
    for k in range(16):
        if board[k]:  # occupied
            continue
        else:
            board[k] = 1
            res = alpha_beta(board, dep+1, alpha, beta)
            if res == 1:  # 1/x wins!
                return '({},{})'.format(k // 4, k % 4)
            board[k] = 0  # don't forget to reset
    return '#####'  # for all possibilities, it's not sure that 1/x can win


def alpha_beta(board, dep, alpha, beta):
    result = check(board)
    if result:  # if the game has ended...
        return result
    if dep == 16:  # ...or the checkerboard is full, consider it as a leaf node
        return result
    if dep % 2 == 0:  # the step of 1/x
        for j in order:  # iterate in a special order
            if board[j]:  # the place is already occupied
                continue
            else:
                board[j] = 1
                new_alpha = alpha_beta(board, dep+1, alpha, beta)  # alpha-beta pruning
                board[j] = 0
                alpha = max(alpha, new_alpha)
                if alpha >= beta:
                    break
        return alpha
    if dep % 2 != 0:  # the step of 2/o
        for j in order:
            if board[j]:
                continue
            else:
                board[j] = 2
                new_beta = alpha_beta(board, dep+1, alpha, beta)  # alpha-beta pruning
                board[j] = 0
                beta = min(beta, new_beta)
                if alpha >= beta:
                    break
        return beta


order = [0, 3, 5, 6, 9, 10, 12, 15, 1, 2, 4, 7, 8, 11, 13, 14]  # the iterating order, which is important
s = input()
while s != '$':  # deal with input, 'x'->1, 'o'->2, '.'->0. The checkerboard is transformed into a list[16].
    if s == '?':
        state = []
        for i in range(4):
            state.extend(list(map(int, list(input().replace('.', '0').replace('x', '1').replace('o', '2')))))
        depth = state.count(1) + state.count(2)  # depth is the number of the 'x's and 'o's combined
        print(check_forced_win(state, depth, -2, 2))
    s = input()

"""
note: Simple alpha-beta pruning algorithm. The most important part of the program is the list 'order', which 
iterates diagonal elements first. Putting your piece on the diagonal position can make it possible for you to win
by having 4 pieces in one row, column OR DIAGONAL, while putting the piece to other positions can only result in 4
pieces in a row or column. So it's wiser for you and your opponent to put your pieces on the diagonal to simplify
the pruning algorithm.
If the 'order' is [i for i in range(16)], running the program on OJ will result in TLE. Using the order shown in 
the program shortens the time to around 1300 ms.

Memory used: 3804 kB
Time used: 1324 ms
"""
