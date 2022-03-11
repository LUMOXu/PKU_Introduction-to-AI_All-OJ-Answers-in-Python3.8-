"""
PKU, INTRODUCTION TO AI
LECTURE 6 - ADVERSARIAL SEARCH - HW 02 - A Star not a Tree

Total TL: 10000 ms (for Python)
ML: 65536 kB

DESCRIPTION
[Words from the author: The story is long and I'll simplify it. It gives you the coordinates of N (<= 100) points.
You need to find a point which has the smallest total length from the point to all points given in the question.
The point satisfying the rule is usually called a 'Fermat Point'.
You don't need to output the coordinate of the Fermat Point. Output the DISTANCE (rounded to the nearest mm) instead.]

Full Story: Luke wants to upgrade his home computer network from 10mbs to 100mbs. His existing network uses 10base2
(coaxial)cables that allow you to connect any number of computers together in a linear arrangement. Luke is particulary
proud that he solved a nasty NP-complete problem in order to minimize the total cable length.
Unfortunately, Luke cannot use his existing cabling. The 100mbs system uses 100baseT (twisted pair) cables.
Each 100baseT cable connects only two devices: either two network cards or a network card and a hub.
(A hub is an electronic device that interconnects several cables.) Luke has a choice: He can buy 2N-2 network cards
and connect his N computers together by inserting one or more cards into each computer and connecting them all together.
Or he can buy N network cards and a hub and connect each of his N computers to the hub. The first approach
would require that Luke configure his operating system to forward network traffic. However, with the
installation of Winux 2007.2, Luke discovered that network forwarding no longer worked. He couldn't
figure out how to re-enable forwarding, and he had never heard of Prim or Kruskal, so he settled on the
second approach: N network cards and a hub.

Luke lives in a loft and so is prepared to run the cables and place the hub anywhere. But he won't move his computers.
He wants to minimize the total length of cable he must buy.

INPUT
The first line of input contains a positive integer N <= 100, the number of computers. N lines follow; each gives
the (x,y) coordinates (in mm.) of a computer within the room. All coordinates are integers between 0 and 10,000.

OUTPUT
Output consists of one number, the total length of the cable segments, rounded to the nearest mm.

SAMPLE INPUT
4
0 0
0 10000
10000 10000
10000 0

SAMPLE OUTPUT
28284
"""


import math
#import time


def d(points, hub):  # total distance from the hub to all points
    return sum([math.sqrt((point[1]-hub[1])**2 + (point[0]-hub[0])**2) for point in points])


def x_iter(points, hub):  # iteratively compute x
    try:
        return sum([point[0] / math.sqrt((point[1]-hub[1])**2 + (point[0]-hub[0])**2) for point in points])\
            / sum([1 / math.sqrt((point[1]-hub[1])**2 + (point[0]-hub[0])**2) for point in points])
    except ZeroDivisionError:
        return hub[0]


def y_iter(points, hub):  # iteratively compute y
    try:
        return sum([point[1] / math.sqrt((point[1]-hub[1])**2 + (point[0]-hub[0])**2) for point in points])\
             / sum([1 / math.sqrt((point[1]-hub[1])**2 + (point[0]-hub[0])**2) for point in points])
    except ZeroDivisionError:
        return hub[1]


def find_fermat_point(points, hub, steps):
    dist = d(points, hub)
    hub[0] = x_iter(points, hub)
    hub[1] = y_iter(points, hub)
    old_dist = dist
    dist = d(points, hub)
    if abs(old_dist - dist) <= 0.5:  # Compare the results, the bigger difference, the faster.
        # Strangely, the difference can be up to 1.54 while the program can still be accepted, showing the OJ system
        # don't give too strong test cases.
        return dist, steps
    steps += 1
    dist, steps = find_fermat_point(points, hub, steps)
    return dist, steps  # returns a tuple (steps for debugging)


n = int(input())
computers = []
for i in range(n):
    computers.append(tuple(map(int, input().split())))
#a = time.time()
hub_pos = [sum([computer[0] for computer in computers]) / n, sum([computer[1] for computer in computers]) / n]
step = 1
dist = d(computers, hub_pos)
final_dist, final_steps = find_fermat_point(computers, hub_pos, step)
#b = time.time()
#print(b-a)
print(round(final_dist))
#print(final_dist)

"""
note: Actually, this problem isn't an adversarial search problem.
See https://www.cnblogs.com/maoerbao/p/11532649.html for more details on the algorithm.
"""