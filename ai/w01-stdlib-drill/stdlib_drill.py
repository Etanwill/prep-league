from collections import Counter, defaultdict, deque
import heapq, bisect
from multiprocessing import heap

res1 = Counter('abracadabra').most_common(1)
assert res1 == [("a", 5)]

groups = defaultdict(list)
word = ["apple", "ant", "banana", "ball", "cat"]
for w in word:
    groups[w[0]].append(w)
assert groups["a"] == ["apple", "ant"]
assert groups["b"] == ["banana", "ball"]
assert groups["c"] == ["cat"]

d = deque([1,2,3], maxlen=3)
d.append(4)
assert list(d) == [2, 3, 4]
d.popleft()
assert list(d) == [3, 4]
d.appendleft(6)
assert list(d) == [6, 3, 4]

min_heap = []
heapq.heappush(min_heap, 8)
heapq.heappush(min_heap, 2)
heapq.heappush(min_heap, 4)
heapq.heappush(min_heap, 20)
heapq.heappop(min_heap)
res2 = heapq.nlargest(2,min_heap)
assert res2 == [20, 8]

max_heap = []
heapq.heappush(max_heap, -8)
heapq.heappush(max_heap, -2)
heapq.heappush(max_heap, -4)
heapq.heappush(max_heap, -16)
heapq.heappop(max_heap)
res3 =[-x for x in heapq.nsmallest(2, max_heap)]
assert res3 == [8, 4]


nums = [1, 2, 3, 4, 5]
bisect.insort(nums, 3)
assert nums == [1, 2, 3, 3, 4, 5]
assert bisect.bisect_left(nums, 3) == 2

from dataclasses import dataclass

@dataclass(order=True)
class Person:
    age: int
    name: str

p1 = Person(30, "Alice")
p2 = Person(22, "Etan")
p3 = Person(25, "styve")
assert sorted([p1, p2, p3]) == [p2, p3, p1]

from itertools import groupby

notes = [15, 16, 19, 10, 15, 16, 19, 10, 16, 11, 15, 19]

for note, group in groupby(sorted(notes)):
    group = list(group)
    if note == 15:
        assert group == [15, 15, 15]
    if note == 16:
        assert group != [11]

import threading

counter = 0
lock = threading.Lock()
threads = []
def increment():
    global counter
    for _ in range(10000):
        with lock:
            counter += 1
for i in range(4):
    t = threading.Thread(target =increment)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
assert counter == 40000

import asyncio

async def work(number, delay):
    await asyncio.sleep(delay)
    return number
async def main():
    results = await asyncio.gather(work(1, 3), work(2, 1), work(3, 2))
    assert results == [1, 2, 3]


