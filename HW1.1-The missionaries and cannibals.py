"""
PKU, INTRODUCTION TO AI
LECTURE 5 - GLOBAL SEARCH - HW 01 - The Missionaries and Cannibals

DESCRIPTION
The missionaries and cannibals problem is usually stated as follows: Three missionaries and three cannibals are on one
side of a river, along with a boat that can hold one or two people. Find a way to get everyone to the other side,
without ever leaving a group of missionaries in one place (including the boat) outnumbered by the cannibals
in that place. Now the problem has been extended to be more complicated. There are m missionaries and m cannibals
who want to cross the river. And the boat is also enlarged to be capable of supporting n people. In order to make
all of them cross the river safely what is the least number of steps? Notice that when the boat goes across the
river there must be at least one missionary or cannibal on the boat.

INPUT
The input consists of only one line, and is made of two positive number m and n, where m ≤ 1000 and n ≤ 100.

OUTPUT
Output the least number of steps needed. If the problem can't be solved, print -1 as the result.

SAMPLE INPUT
3 2

SAMPLE OUTPUT
11
"""
import queue


def check(state, d_mis, d_can):
    mis = state[1][0]
    can = state[1][1]
    boat = state[1][2]  # 0rtl 1ltr
    if mis and mis < can:
        return False
    if boat:  # start to goal
        if m - mis < d_mis or m - can < d_can:
            return False
        if m - mis > d_mis and m - mis - d_mis < m - can - d_can:
            return False
        if mis + d_mis > 0 and mis + d_mis < can + d_can:
            return False
        if tuple((state[1][0] + d_mis, state[1][1] + d_can, 0)) in close_nodes:
            return False
        return True
    else:  # goal to start
        if mis < d_mis or can < d_can:
            return False
        if mis > d_mis and mis - d_mis < can - d_can:
            return False
        if m - mis + d_mis > 0 and m - mis + d_mis < m - can + d_can:
            return False
        if tuple((state[1][0] - d_mis, state[1][1] - d_can, 1)) in close_nodes:
            return False
        return True


def update(state, d_mis, d_can):
    # f = 1  # you can try this f instead to see the difference
    if state[1][2]:  # start to goal
        f = 2 * (m - state[1][0] - d_mis) + 1 * (m - state[1][1] - d_can) - 2 * 0
        return tuple((f, (state[1][0] + d_mis, state[1][1] + d_can, 0, state[1][3] + 1)))
    else:  # goal to start
        f = 2 * (m - state[1][0] + d_mis) + 1 * (m - state[1][1] + d_can) - 2 * 1
        return tuple((f, (state[1][0] - d_mis, state[1][1] - d_can, 1, state[1][3] + 1)))


def bfs(m, n):
    # nodes = 0
    while not open_nodes.empty():
        current_state = open_nodes.get()
        close_nodes.add(current_state[1][:3])
        # nodes += 1
        if current_state[1][:2] == (m, m):  # FINISH! =)
            # print(nodes)  # debug, output the number of closed nodes
            return current_state[1][3]  # which is the step_count
        for i in range(1, n + 1):  # the total count of human on boat
            for j in range(0, i + 1):  # cannibals
                if check(current_state, i - j, j):  # do the state satisfy the rules after update?
                    open_nodes.put(update(current_state, i - j, j))  # If so, update the state.

    return -1  # can't find an answer =(


m, n = map(int, input().split())
open_nodes = queue.PriorityQueue()
open_nodes.put((3 * m - 2, (0, 0, 1, 0)))
# a status <- (f value, (missionaries at goal, cannibals at goal, boat state(0 means right/goal to left/start, vice versa), steps))
# f := a * missionaries at start + b * cannibals at start - c * boat state (in this program, a, b, c = 2, 1, 2), the node/state with less f value is expanded first.
# slight changes to f usually doesn't matter unless b >= a, which causes the program to carry too much cannibals to the goal.
close_nodes = set()
close_nodes.add((0, 0, 1))
# (missionaries at goal, cannibals at goal, boat status)
print(bfs(m, n))

"""
note:
Due to strange reasons, the priority queue didn't sort all nodes/states about their f values well. However, the program still
ran correctly and satisfied the time and memory limits. You can sort the nodes/states correctly to get a better result. For the size of the close_nodes_set is small, you
can even use a list, instead of a priority queue.
The most important part of the program is the function f. The order of scanning i-s and j-s is not that important.
Given the correct f, The length of the close_nodes_set is usually the same as (sometimes outnumbers a little bit) the number of the steps, which means the program can act 
almost perfectly at finding the shortest route instead of doing simple dfs searching. (For this problem, doing simple dfs in python always results in TLE)
"""
