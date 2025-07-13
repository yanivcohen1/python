import heapq
# complecity is O(logN) for push or pop element
h = []
heapq.heappush(h, (5, 'write code'))
heapq.heappush(h, (7, 'release product'))
heapq.heappush(h, (1, 'write spec'))
heapq.heappush(h, (3, 'create tests'))
print(heapq.heappop(h)) # (1, 'write spec')

dict1 = {2: "2", 1: "3", 4:"4"}
h = []
for key, val in dict1.items():
  heapq.heappush(h, (key, val))
print(heapq.heappop(h)) # (1, '1') the smolest
print(heapq.heappop(h)) # (2, '2')

h = []
for key, val in dict1.items():
  heapq.heappush(h, (key, val))
# Get the n smallest elements from the heap
n_smallest = heapq.nsmallest(2, h)

# Print the n smallest elements
print("Smallest 2 elements:", n_smallest)

# Get the n largest elements from the heap
n_largest = heapq.nlargest(2, h)

# Print the n largest elements
print("Largest 2 elements:", n_largest)
