Absolutely. Here is the **Markdown version** you can copy into a file named `DSA_Interview_Patterns.md`.

:::writing{variant="document" id="58321" title="DSA Interview Patterns — Complete Recognition & Solving Guide"}

# DSA Interview Patterns — Complete Recognition & Solving Guide

> **Goal:** Learn to recognize the pattern in an interview question, choose the correct technique, and solve it systematically.

---

# Table of Contents

1. How to Recognize DSA Patterns
2. Arrays & Hashing
3. Two Pointers
4. Sliding Window
5. Prefix Sum
6. Binary Search
7. Linked List
8. Stack
9. Monotonic Stack
10. Intervals
11. Heap / Priority Queue
12. Trees
13. Binary Search Tree
14. Graphs
15. BFS
16. DFS
17. Topological Sort
18. Union Find / DSU
19. Backtracking
20. Greedy
21. Dynamic Programming
22. Trie
23. Bit Manipulation
24. Fast & Slow Pointers
25. Matrix / Grid
26. Advanced Graph Patterns
27. Pattern Recognition Cheat Sheet
28. Interview Solving Framework
29. Complexity Cheat Sheet

---

# 1\. How to Recognize DSA Patterns

Before coding, ask these questions:

### Step 1 — What is the data structure?

- Array?
- String?
- Linked List?
- Tree?
- Graph?
- Grid?
- Heap?
- HashMap?

### Step 2 — What is the question asking?

- Find?
- Count?
- Maximum?
- Minimum?
- Longest?
- Shortest?
- All possible answers?
- Number of ways?
- Can it be done?

### Step 3 — Look for keywords

| Question clue | First pattern to consider |
| --- | --- |
| Pair / two numbers | Two Pointers / HashMap |
| Sorted array | Binary Search / Two Pointers |
| Subarray | Sliding Window / Prefix Sum |
| Substring | Sliding Window |
| Subarray sum = K | Prefix Sum + HashMap |
| Longest substring | Sliding Window |
| Shortest substring | Sliding Window |
| Top K | Heap |
| Kth largest | Heap / Quickselect |
| Next greater | Monotonic Stack |
| Previous smaller | Monotonic Stack |
| Overlapping intervals | Sort + Greedy |
| All combinations | Backtracking |
| All permutations | Backtracking |
| Minimum steps | BFS |
| Dependencies | Topological Sort |
| Connected components | DFS / BFS / DSU |
| Shortest weighted path | Dijkstra |
| Repeated states | Dynamic Programming |
| Prefix / autocomplete | Trie |
| Unique number using XOR | Bit Manipulation |

---

# 2\. Arrays & Hashing

## When to think about it

Use HashMap/HashSet when you need:

- Fast lookup
- Frequency counting
- Duplicate detection
- Mapping values
- "Have I seen this before?"
- Pair matching

## Pattern: Frequency Map

### Question

> Count frequency of each number.

```
freq = {}

for x in nums:
    freq[x] += 1
```

## Pattern: Duplicate Detection

### Question

> Does the array contain duplicates?

```
seen = set()

for x in nums:
    if x in seen:
        return true

    seen.add(x)

return false
```

### Complexity

```
Time:  O(n)
Space: O(n)
```

## Pattern: Two Sum

### Question

> Find two numbers whose sum equals target.

```
seen = {}

for i, x in enumerate(nums):

    needed = target - x

    if needed in seen:
        return [seen[needed], i]

    seen[x] = i
```

### Complexity

```
Time:  O(n)
Space: O(n)
```

---

# 3\. Two Pointers

## Recognition

Think **Two Pointers** when:

- Array is sorted
- Looking for a pair
- Comparing both ends
- Removing duplicates
- In-place modification
- Palindrome checking

## Example

> Find two numbers with sum = target in a sorted array.

```
left = 0
right = n - 1

while left < right:

    current = nums[left] + nums[right]

    if current == target:
        return [left, right]

    elif current < target:
        left += 1

    else:
        right -= 1
```

## Why?

If:

```
nums[left] + nums[right] < target
```

then we need a larger value.

Move:

```
left++
```

If sum is too large:

```
right--
```

## Common problems

- Two Sum II
- 3Sum
- Container With Most Water
- Valid Palindrome
- Remove Duplicates
- Move Zeroes

---

# 4\. Sliding Window

## Recognition

Think Sliding Window when you see:

- Longest substring
- Shortest substring
- Longest subarray
- Smallest subarray
- Maximum/minimum window
- "At most K"
- "Exactly K" in some variants
- Contiguous range

## Basic Template

```
left = 0

for right in range(n):

    add nums[right] to window

    while window is invalid:

        remove nums[left]
        left += 1

    update answer
```

## Example

> Longest substring without repeating characters.

```
left = 0
seen = set()
answer = 0

for right in range(len(s)):

    while s[right] in seen:
        seen.remove(s[left])
        left += 1

    seen.add(s[right])

    answer = max(answer, right - left + 1)
```

## Complexity

```
Time:  O(n)
Space: O(n)
```

## Common problems

- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Longest Repeating Character Replacement
- Minimum Size Subarray Sum
- Longest Subarray with At Most K Distinct Values

---

# 5\. Prefix Sum

## Recognition

Think Prefix Sum when:

- Asking about subarray sums
- Multiple range-sum queries
- Count subarrays satisfying a sum
- Need sum from `i` to `j`

## Basic Idea

```
prefix[i] = sum of elements from 0 to i
```

Then:

```
sum(i...j) = prefix[j] - prefix[i-1]
```

## Subarray Sum = K

This is a very important interview pattern.

```
prefix = 0
freq = {0: 1}
answer = 0

for x in nums:

    prefix += x

    if prefix - k in freq:
        answer += freq[prefix - k]

    freq[prefix] += 1
```

### Why?

We need:

```
prefix[j] - prefix[i] = k
```

Therefore:

```
prefix[i] = prefix[j] - k
```

So we store previous prefix sums in a HashMap.

### Complexity

```
Time:  O(n)
Space: O(n)
```

---

# 6\. Binary Search

## Recognition

Think Binary Search when:

- Array is sorted
- Search space is ordered
- You can eliminate half the possibilities
- There is a monotonic yes/no condition

## Basic Template

```
left = 0
right = n - 1

while left <= right:

    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid

    elif nums[mid] < target:
        left = mid + 1

    else:
        right = mid - 1

return -1
```

## Binary Search on Answer

This is extremely important.

### Recognition

Question asks:

> Minimum possible X such that condition is satisfied.

or:

> Maximum possible X such that condition is satisfied.

Usually you can define:

```
low = smallest possible answer
high = largest possible answer
```

Then create:

```
canDo(mid)
```

Example:

> Koko Eating Bananas

Search:

```
speed = minimum possible ... maximum possible
```

Then:

```
while low <= high:

    mid = (low + high) // 2

    if canFinish(mid):
        answer = mid
        high = mid - 1

    else:
        low = mid + 1
```

## Common problems

- Binary Search
- Search in Rotated Sorted Array
- Koko Eating Bananas
- Capacity to Ship Packages
- Allocate Books
- Aggressive Cows
- Split Array Largest Sum

---

# 7\. Linked List

## Pattern 1 — Reverse Linked List

Memorize this.

```
prev = null
curr = head

while curr:

    next = curr.next
    curr.next = prev

    prev = curr
    curr = next

return prev
```

## Pattern 2 — Dummy Node

Use when:

- Head may change
- Inserting/removing nodes
- Merging lists

```
dummy -> head
```

## Pattern 3 — Fast & Slow

Use for:

- Middle of linked list
- Cycle detection
- Cycle starting point
- Palindrome
- Kth node from end

---

# 8\. Stack

## Recognition

Think Stack when you see:

- Matching brackets
- Nested structures
- Undo
- Previous/next element
- Expression evaluation
- Parentheses
- "Nearest" element

## Valid Parentheses

```
stack = []

for ch in s:

    if ch is opening bracket:
        stack.push(ch)

    else:

        if stack is empty:
            return false

        if stack.top doesn't match ch:
            return false

        stack.pop()

return stack is empty
```

---

# 9\. Monotonic Stack

## Recognition

Immediate trigger words:

- Next greater
- Next smaller
- Previous greater
- Previous smaller
- Daily temperatures
- Stock span
- Largest rectangle

## Example

> Next Greater Element

```
stack = []
answer = [-1] * n

for i in range(n):

    while stack and nums[i] > nums[stack[-1]]:

        index = stack.pop()
        answer[index] = nums[i]

    stack.append(i)
```

### Complexity

```
Time: O(n)
```

Even though there is a `while` loop, each element is pushed and popped at most once.

---

# 10\. Intervals

## Recognition

Input looks like:

```
[start, end]
```

Question involves:

- Overlap
- Merge
- Scheduling
- Meeting rooms
- Non-overlapping intervals

## First Step

Usually:

```
sort intervals by start time
```

## Merge Intervals

```
intervals.sort()

answer = []

for interval in intervals:

    if answer is empty or interval.start > answer[-1].end:

        answer.append(interval)

    else:

        answer[-1].end = max(
            answer[-1].end,
            interval.end
        )
```

## Important Condition

Overlap exists when:

```
current.start <= previous.end
```

---

# 11\. Heap / Priority Queue

## Recognition

Think Heap when you see:

- Top K
- Kth largest
- Kth smallest
- Repeatedly get minimum
- Repeatedly get maximum
- Merge sorted lists
- Scheduling

## Top K Largest

Use a **min heap of size K**.

```
heap = []

for x in nums:

    push x into heap

    if len(heap) > k:
        pop smallest
```

Complexity:

```
Time:  O(n log k)
Space: O(k)
```

## Common problems

- Kth Largest Element
- Top K Frequent Elements
- K Closest Points
- Merge K Sorted Lists
- Find Median from Data Stream

---

# 12\. Trees

## First Question

Ask:

> What information do I need from the children to calculate the answer for the current node?

This often determines the traversal.

## DFS

Useful for:

- Height
- Diameter
- Balanced Tree
- Path Sum
- Subtree problems
- Lowest Common Ancestor

## BFS

Useful for:

- Level order
- Minimum depth
- Level-based problems
- Zigzag traversal

---

# 13\. Binary Search Tree

## Core Property

```
left subtree < root < right subtree
```

## Important Fact

Inorder traversal of a BST gives:

```
sorted order
```

## Search

```
if target == root:
    found

elif target < root:
    search left

else:
    search right
```

## Common problems

- Search BST
- Insert BST
- Validate BST
- Lowest Common Ancestor in BST
- Kth Smallest Element

---

# 14\. Graphs

## First classify the problem.

### Connectivity

Use:

```
DFS
BFS
DSU
```

### Shortest Path

```
Unweighted → BFS
Positive weights → Dijkstra
Negative weights → Bellman-Ford
DAG → Topological ordering + DP
```

### Dependencies

Use:

```
Topological Sort
```

### Minimum Spanning Tree

Use:

```
Kruskal
Prim
```

---

# 15\. BFS

## Recognition

Think BFS when:

- Minimum number of moves
- Shortest path in unweighted graph
- Level-by-level traversal
- Minimum steps
- Grid shortest path

## Template

```
queue = [start]
visited = {start}

while queue:

    node = queue.pop_front()

    for neighbor in neighbors(node):

        if neighbor not in visited:

            visited.add(neighbor)
            queue.push(neighbor)
```

## Important

For shortest distance, process by levels:

```
distance = 0

while queue:

    process current level

    distance += 1
```

---

# 16\. DFS

## Recognition

Think DFS for:

- Explore all connected nodes
- Connected components
- Islands
- Cycle detection
- Backtracking through graph
- Tree recursion

## Template

```
dfs(node):

    if node visited:
        return

    mark node visited

    for neighbor in neighbors(node):

        dfs(neighbor)
```

---

# 17\. Topological Sort

## Recognition

Keywords:

- Prerequisites
- Dependencies
- Course schedule
- Task ordering
- Build order
- Compilation dependencies

Example:

```
A → B
```

means:

```
A must happen before B
```

## Kahn's Algorithm

```
calculate indegree of every node

queue = all nodes with indegree 0

while queue:

    node = queue.pop()

    add node to answer

    for neighbor:

        indegree[neighbor] -= 1

        if indegree[neighbor] == 0:
            queue.push(neighbor)
```

## Cycle Detection

If:

```
number of processed nodes < total nodes
```

then there is a cycle.

---

# 18\. Union Find / DSU

## Recognition

Think DSU when:

- Groups merge
- Connectivity changes
- Connected components
- Redundant connection
- Network connectivity
- Kruskal's algorithm

## Operations

```
find(x)
union(a, b)
```

## Template

```
parent = [0, 1, 2, ..., n-1]

find(x):

    if parent[x] != x:
        parent[x] = find(parent[x])

    return parent[x]

union(a, b):

    rootA = find(a)
    rootB = find(b)

    if rootA != rootB:
        parent[rootA] = rootB
```

For optimal performance, use:

- Path compression
- Union by rank/size

---

# 19\. Backtracking

## Recognition

Think Backtracking when question asks for:

- All subsets
- All combinations
- All permutations
- All valid arrangements
- N-Queens
- Sudoku
- Word Search
- Generate Parentheses

## Core Pattern

```
choose
explore
undo
```

## Template

```
backtrack(path):

    if complete:
        answer.append(path)
        return

    for choice in choices:

        choose(choice)

        backtrack(path)

        undo(choice)
```

---

# 20\. Greedy

## Recognition

Think Greedy when:

> A locally optimal choice can be proven to lead to a globally optimal solution.

Common areas:

- Interval scheduling
- Jump Game
- Gas Station
- Activity Selection
- Minimum number of intervals
- Scheduling

## Important

Do **not** use greedy just because it looks intuitive.

Ask:

> Can I prove that choosing this option now can never hurt the optimal answer?

---

# 21\. Dynamic Programming

## Recognition

Think DP when:

- Same subproblem appears repeatedly
- There are overlapping subproblems
- You need maximum/minimum/count
- There are choices
- Current answer depends on previous answers

## Four Questions

### 1\. What is the state?

What variables uniquely describe a subproblem?

### 2\. What are the choices?

What can I do from this state?

### 3\. What is the transition?

How does current state depend on smaller states?

### 4\. What is the base case?

What is the smallest possible state?

---

# 22\. 1D Dynamic Programming

## Example — Climbing Stairs

To reach stair `n`:

```
dp[n] = dp[n-1] + dp[n-2]
```

because the last move can be:

```
1 step
OR
2 steps
```

## Template

```
dp[0] = base

for i in range(1, n):

    dp[i] = transition from previous states
```

## Common problems

- Climbing Stairs
- House Robber
- Coin Change
- Decode Ways
- Min Cost Climbing Stairs

---

# 23\. 2D Dynamic Programming

## Recognition

Two changing variables often mean 2D DP.

Examples:

- Grid problems
- LCS
- Edit Distance
- Knapsack

## Example — LCS

State:

```
dp[i][j]
```

means:

> LCS of first `i` characters of string A and first `j` characters of string B.

Transition:

```
if A[i-1] == B[j-1]:

    dp[i][j] = 1 + dp[i-1][j-1]

else:

    dp[i][j] = max(
        dp[i-1][j],
        dp[i][j-1]
    )
```

---

# 24\. Knapsack Pattern

## Recognition

Question gives:

- Items
- Weight/cost
- Value/profit
- Capacity
- Choose or don't choose

Think:

```
take
OR
don't take
```

## 0/1 Knapsack

State:

```
dp[i][capacity]
```

Transition:

```
dp[i][capacity] =
    max(
        don'tTake,
        take
    )
```

---

# 25\. Trie

## Recognition

Think Trie when questions involve:

- Prefix
- Dictionary
- Autocomplete
- Prefix search
- Many words
- Word insertion/search

## Structure

```
root
 ├── a
 │    ├── p
 │    └── n
 └── b
```

## Common problems

- Implement Trie
- Word Search II
- Replace Words
- Prefix Search
- Autocomplete

---

# 26\. Bit Manipulation

## Important identities

```
x ^ x = 0
x ^ 0 = x
```

Therefore:

> Every number occurs twice except one.

Solution:

```
answer = 0

for x in nums:
    answer ^= x

return answer
```

## Useful operations

### Check odd/even

```
x & 1
```

### Check power of two

```
x > 0 and (x & (x - 1)) == 0
```

### Remove lowest set bit

```
x = x & (x - 1)
```

---

# 27\. Fast & Slow Pointers

## Recognition

Especially useful for linked lists.

Use when:

- Find middle
- Detect cycle
- Find cycle start
- Find kth node from end
- Palindrome

## Find Middle

```
slow = head
fast = head

while fast and fast.next:

    slow = slow.next
    fast = fast.next.next

return slow
```

When fast reaches the end, slow is approximately at the middle.

---

# 28\. Matrix / Grid

Treat a grid as a graph.

Each cell can have up to four neighbors:

```
up
down
left
right
```

## Common patterns

### Number of Islands

Use:

```
DFS / BFS
```

### Shortest Path

Use:

```
BFS
```

### Flood Fill

Use:

```
DFS / BFS
```

### Grid DP

Use:

```
Dynamic Programming
```

Example:

```
dp[i][j] =
    best answer to reach cell (i,j)
```

---

# 29\. Advanced Graph Patterns

## Dijkstra

### Recognition

Shortest path + positive edge weights.

Use a:

```
min heap
```

Basic idea:

```
distance[start] = 0

while heap:

    distance, node = pop minimum

    for neighbor:

        newDistance = distance + edgeWeight

        if newDistance < distance[neighbor]:

            update distance
            push into heap
```

Complexity typically:

```
O((V + E) log V)
```

---

## Minimum Spanning Tree

### Kruskal

Think:

```
sort edges by weight
+
DSU
```

### Prim

Think:

```
min heap
+
grow tree
```

---

# 30\. Pattern Recognition Cheat Sheet

This is the section to memorize.

| If you see... | Think... |
| --- | --- |
| Pair sum | HashMap / Two Pointers |
| Sorted + pair | Two Pointers |
| Sorted + search | Binary Search |
| Longest substring | Sliding Window |
| Shortest substring | Sliding Window |
| Longest subarray | Sliding Window |
| Subarray sum K | Prefix Sum + HashMap |
| Range sum | Prefix Sum |
| Duplicate | HashSet |
| Frequency | HashMap |
| Anagram | Frequency Map |
| Group Anagrams | HashMap + Signature |
| Next Greater | Monotonic Stack |
| Previous Greater | Monotonic Stack |
| Next Smaller | Monotonic Stack |
| Top K | Heap |
| Kth Largest | Heap / Quickselect |
| Merge Intervals | Sort + Greedy |
| Meeting Rooms | Sort / Heap |
| Linked List cycle | Fast + Slow |
| Linked List middle | Fast + Slow |
| Reverse Linked List | Three pointers |
| Tree height | DFS |
| Tree level order | BFS |
| BST | Inorder / Binary Search |
| Number of Islands | DFS / BFS |
| Shortest unweighted path | BFS |
| Shortest weighted path | Dijkstra |
| Dependencies | Topological Sort |
| Connected components | DFS / BFS / DSU |
| Dynamic connectivity | DSU |
| All subsets | Backtracking |
| All permutations | Backtracking |
| All combinations | Backtracking |
| N-Queens | Backtracking |
| Optimization with repeated states | DP |
| Number of ways | DP |
| Prefix search | Trie |
| Unique using pairs | XOR |
| Minimum X satisfying condition | Binary Search on Answer |
| Maximum X satisfying condition | Binary Search on Answer |

---

# 31\. Interview Solving Framework

When the interviewer gives you a problem, follow this process.

## Step 1 — Understand the problem

Say:

> "Let me first make sure I understand the requirements."

Clarify:

- Input size
- Duplicates?
- Negative numbers?
- Sorted?
- Empty input?
- Expected output?
- Can we modify the input?

---

## Step 2 — Identify the brute force

Ask yourself:

> "What is the obvious solution?"

Example:

Find pair sum.

Brute force:

```
for i:
    for j:
        check nums[i] + nums[j]
```

Complexity:

```
O(n²)
```

---

## Step 3 — Find the bottleneck

Ask:

> "What are we repeatedly doing?"

For Two Sum:

```
Searching for target - nums[i]
```

Can HashMap make this `O(1)`?

Yes.

Therefore:

```
O(n²) → O(n)
```

---

## Step 4 — Identify the pattern

Ask:

> Which known pattern matches this?

Examples:

```
contiguous + longest
        ↓
Sliding Window
```

```
sorted + pair
        ↓
Two Pointers
```

```
minimum possible X
        ↓
Binary Search on Answer
```

---

## Step 5 — Explain before coding

A strong interview explanation:

> "I'll use a HashMap to store values I've already seen. For each number, I'll check whether `target - current` exists. This lets me find the required pair in O(1) average lookup time, giving O(n) total time."

Then code.

---

# 32\. Complexity Cheat Sheet

## Array operations

| Operation | Complexity |
| --- | --- |
| Access by index | O(1) |
| Search unsorted | O(n) |
| Search sorted | O(log n) |
| Insert at end | O(1) amortized |
| Insert at beginning | O(n) |

## HashMap

| Operation | Average |
| --- | --- |
| Insert | O(1) |
| Search | O(1) |
| Delete | O(1) |

Worst case can be O(n).

## Stack

```
push    O(1)
pop     O(1)
top     O(1)
```

## Queue

```
push    O(1)
pop     O(1)
```

## Heap

```
insert      O(log n)
delete      O(log n)
get min/max O(1)
```

## Binary Search

```
O(log n)
```

## BFS / DFS

For graph:

```
O(V + E)
```

## Sorting

Typical comparison sorting:

```
O(n log n)
```

## Dynamic Programming

Usually:

```
number of states × transitions per state
```

---

# 33\. The Big Pattern Decision Tree

Use this during practice.

```
START
  |
  v
What is the input?
  |
  +-- Array/String
  |      |
  |      +-- Sorted?
  |      |      |
  |      |      +-- Yes → Binary Search / Two Pointers
  |      |
  |      +-- Subarray/Substring?
  |      |      |
  |      |      +-- Longest/Shortest → Sliding Window
  |      |      +-- Sum → Prefix Sum
  |      |
  |      +-- Pair?
  |      |      |
  |      |      +-- HashMap / Two Pointers
  |      |
  |      +-- Top K?
  |             |
  |             +-- Heap
  |
  +-- Linked List
  |      |
  |      +-- Cycle/Middle → Fast/Slow
  |      +-- Reverse → Pointer manipulation
  |
  +-- Tree
  |      |
  |      +-- Level → BFS
  |      +-- Subtree information → DFS
  |      +-- BST → Inorder/Binary Search
  |
  +-- Graph
  |      |
  |      +-- Unweighted shortest path → BFS
  |      +-- Weighted shortest path → Dijkstra
  |      +-- Dependencies → Topological Sort
  |      +-- Connectivity → DFS/BFS/DSU
  |
  +-- "All possible..."
  |      |
  |      +-- Backtracking
  |
  +-- Optimization / Counting
         |
         +-- Repeated states?
                |
                +-- Yes → Dynamic Programming
```

---

# 34\. What You Should Memorize

Do **not** memorize 500 solutions.

Memorize these templates:

```
1. HashMap frequency
2. Two Pointers
3. Sliding Window
4. Prefix Sum
5. Binary Search
6. Binary Search on Answer
7. Reverse Linked List
8. Fast/Slow Pointers
9. Stack
10. Monotonic Stack
11. BFS
12. DFS
13. Tree DFS
14. Tree BFS
15. Heap
16. Backtracking
17. Topological Sort
18. DSU
19. 1D DP
20. 2D DP
21. Dijkstra
22. Trie
23. Bit Manipulation
```

Once these become automatic, many interview questions become variations of the same patterns.

---

# 35\. Final Mental Model

When you get a new problem, don't ask:

> "Have I seen this exact question?"

Ask:

> **"What pattern does this question resemble?"**

Then:

```
Question
   ↓
Identify data structure
   ↓
Identify operation
   ↓
Look for keywords
   ↓
Think brute force
   ↓
Find bottleneck
   ↓
Choose pattern
   ↓
Choose data structure
   ↓
Write invariant / state
   ↓
Code
   ↓
Test edge cases
   ↓
Analyze complexity
```

## The Most Important Recognition Rules

```
SORTED + PAIR
→ TWO POINTERS

SUBARRAY + LONGEST/SHORTEST
→ SLIDING WINDOW

SUBARRAY + SUM
→ PREFIX SUM

SUBARRAY SUM = K
→ PREFIX SUM + HASHMAP

NEXT/PREVIOUS GREATER/SMALLER
→ MONOTONIC STACK

TOP K / KTH
→ HEAP

OVERLAPPING INTERVALS
→ SORT + GREEDY

ALL POSSIBILITIES
→ BACKTRACKING

UNWEIGHTED SHORTEST PATH
→ BFS

WEIGHTED SHORTEST PATH
→ DIJKSTRA

DEPENDENCIES
→ TOPOLOGICAL SORT

CONNECTED COMPONENTS
→ DFS/BFS/DSU

REPEATED SUBPROBLEMS
→ DP

PREFIX SEARCH
→ TRIE

UNIQUE ELEMENT WITH PAIRS
→ XOR

MIN/MAX ANSWER WITH YES/NO CHECK
→ BINARY SEARCH ON ANSWER
```

---

# End Goal

You should eventually be able to see:

> **"Find the longest substring containing at most K distinct characters."**

and immediately think:

```
substring
    ↓
contiguous
    ↓
longest
    ↓
window
    ↓
Sliding Window + HashMap
```

Or:

> **"Find the minimum capacity needed to ship packages within D days."**

and think:

```
minimum answer
    ↓
define possible range
    ↓
can(mid)?
    ↓
monotonic
    ↓
Binary Search on Answer
```

That is the skill that matters most in DSA interviews. :::

You can save the block above directly as **`DSA_Interview_Patterns.md`** and open it in VS Code, GitHub, Obsidian, Typora, or any Markdown editor.