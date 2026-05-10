"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Priyesh Patel
Student ID:   131613518

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq

# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return '''Why a single shortest-path run from S is not enough:**
                A shortest path is not enough because we need to go too all relic chambers at least once before reaching the exit.
            What decision remains after all inter-location costs are known:**
                Which ordering of relic chambers minimizes the torch cost.
            Why this requires a search over orders (one sentence):**
                This requires a search over orders so that we can find the best path to minimize the torch fuel cost.
            '''



# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    return list(set([spawn] + relics))


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    #create dict
    dist = {}
    #set all nodes to unreachable
    for node in graph:
        dist[node] = float('inf')
    #set distance to start to 0
    dist[source] = 0

    pq = [(0,source)]


    while pq:
        curDist, curNode = heapq.heappop(pq)

        if(curDist > dist[curNode]):
            continue

        for neighbor, cost in graph[curNode]:
            newDist = dist[curNode] + cost

            if(newDist < dist[neighbor]):
                dist[neighbor] = newDist
                heapq.heappush(pq, (newDist, neighbor))
    return dist





def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    sources = select_sources(spawn, relics, exit_node)
    dist = {}
    for source in sources:
        distance = run_dijkstra(graph,source)
        dist[source] = distance
    return dist



# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return '''## Part 3: Algorithm Correctness
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
'''


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.


    """
    return '''## Part 4: Search Design

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

    '''


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    best = [float('inf'), []]
    relics_remaining = set(relics)
    _explore(dist_table, spawn, relics_remaining,[],0, exit_node,best)
    return best[0], best[1]



def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Up1dates best in place.

    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    #Because all routes are nonnegative, adding to the route cannot make the cost lower.
    #This means this route cannot beat the best cost so far.
    if cost_so_far >= best[0]:
        return
    if not relics_remaining:
        exit_cost = dist_table[current_loc][exit_node]
        if exit_cost == float('inf'):
            return
        total_cost = cost_so_far + exit_cost
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = relics_visited_order.copy()
        return

    for relic in list(relics_remaining):
        cost = dist_table[current_loc][relic]
        if cost == float('inf'):
            continue
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + cost, exit_node, best)
        relics_visited_order.pop()
        relics_remaining.add(relic)




# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist = precompute_distances(graph,spawn,relics,exit_node)
    return find_optimal_route(dist,spawn,relics,exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
