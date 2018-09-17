import heapq

li = [10, 5, 9, 4]
heapq.heapify(li)
print(str(li))
elem = heapq.heappop(li)
print('elem', elem)
print('list after pop', str(li))