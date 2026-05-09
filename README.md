# The Torchbearer

**Student Name:** Priyesh Patel
**Student ID:** 131613518  
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis
- **Why a single shortest-path run from S is not enough:**
  A shortest path is not enough because we need to go too all relic chambers at least once before reaching the exit.

- **What decision remains after all inter-location costs are known:**
  Which ordering of relic chambers minimizes the torch cost.

- **Why this requires a search over orders (one sentence):**
  This requires a search over orders so that we can find the best path to minimize the torch fuel cost.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source                                                  |
|----------------|---------------------------------------------------------------------|
| _spawn node_   | This is where we start from to get to a relic                       |
| relic chamber  | after a relic chamber we can either go to another relic or the exit |

### Part 2b: Distance Storage

| Property | Your answer                                     |
|---|-------------------------------------------------|
| Data structure name | dictionary                                      |
| What the keys represent | nodes                                           |
| What the values represent | torch cost to get to the key                    |
| Lookup time complexity | O(1)                                            |
| Why O(1) lookup is possible | dictionary uses hashtable which has O(1) look up |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1
- **Cost per run:** mlogn
- **Total complexity:** O(mlogn)
- **Justification (one line):** we run once from the start and then from every relic chamber. This is O(mlogn)

---

## Part 3: Algorithm Correctness
### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  dist[x] where x is a node then dist[x] holds the actual shortest distance from a source s.

- **For nodes not yet finalized (not in S):**
  dist[x] where x is a node then dist[x] is the shortest distance proven so far from a source s.

### Part 3b: Why Each Phase Holds
- **Initialization : why the invariant holds before iteration 1:**
  Before the first iteration S is empty so none of the nodes are finalized, so we set them to inf,
because no path has been found so far.

- **Maintenance : why finalizing the min-dist node is always correct:**
  We can finalize the minimum dist node because there are no better paths because choosing a alternative path 
will always increase the cost since there are no negative edges.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the algorithm ends all nodes have been finalized and we have gone through all of Dijkstra's
this means we have the actual shortest distances. And any nodes that are still inf are unreachable.

### Part 3c: Why This Matters for the Route Planner
Having the correct shortest distance from the important locations is important
because we use it to create the best route between the intrest points to minimize cost.


## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:**  The greedy algorithm chooses to go the cheapest relic from the current point
but this local choice could cause more expensive choices later
- **Counter-example setup:** Starting from S, having relics A,B and exit T. Lets use costs: S->A=1,S->B = 2, 
A->B=100, B->A=1, A->T=1, B->T=1
- **What greedy picks:** Greedy picks S->A for 1, Then it has to choose A->B for 100 to reach every relic chamber
- and then B->T for one, this total cost  is 102
- **What optimal picks:** The optimal route is S->B->A->T = 4
- **Why greedy loses:** The greedy loses because the cheapest first step does not lead to the overall 
best path. 

### What the Algorithm Must Explore

- The algorithm must explore all possible orders of the relic chambers to the finished,
to find the lowest cost path.

---

## Part 5: State and Search Space

### Part 5a: State Representation
| Component | Variable name in code | Data type | Description                          |
|---|-----------------------|-----------|--------------------------------------|
| Current location | current_loc                | node      | where the the current route ends     |
| Relics already collected | relics_visited_order                | list      | The relics collected so far in order |
| Fuel cost so far | cost_so_far               | float     | The total fuel cost so fara          |

### Part 5b: Data Structure for Visited Relics
| Property | Your answer                                  |
|---|----------------------------------------------|
| Data structure chosen | set                                          |
| Operation: check if relic already collected | Time complexity:O(1)                         |
| Operation: mark a relic as collected | Time complexity:O(1)                         |
| Operation: unmark a relic (backtrack) | Time complexity:O(1)                         |
| Why this structure fits | a set is fast when adding or removing relics |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** There are k orders for the first and k-1 for the next ... to 1 this is a factorial

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The lowest route cost so far with the corresponding relic order
- **When it is used:** Before adding to the route it is checked and updated after all relic have been reached and going to the exit
- 
- **What it allows the algorithm to skip:** The algorithm can skip any route that has a cost at least the cur cost so far

### Part 6b: Lower Bound Estimation
- **What information is available at the current state:** we know the current location, remaining relics, our current relic order, and the
current cost
- **What the lower bound accounts for:** The fuel already spend
- **Why it never overestimates:** Its given that all routes are non negative, so we know 
adding a route wont decrease the cost.

### Part 6c: Pruning Correctness
- if the lower bound is has a higher cost than the best route so far it doesnt beat it
- Since all routes are non negative we can get rid of this branch because it cant contain the optimal solution

---

## References
- Lecture notes
- https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
