# Development Log – The Torchbearer

**Student Name:** Priyesh Patel
**Student ID:** 131613518

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 05/07/26: Initial Plan


I will start by implementing in the order of the parts given in the assignment markdown
file this means I will implement select sources first. 
I think that getting the correct optimal route will be the most difficult.
I will test using the already given test cases as I go. 


---

## Entry 2 – 05/07/26: Fixing Dijkstras implentation

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

When writing the Dijkstra's implementation I first made a mistake when creating the pq for the while loop using heapq
. When I first wrote the pq I forgot to add the source node with distance 0
so the wile loop wouldnt have ran at all. I made sure to add source 0 before the while loop
starts to make sure it starts.

---

## Entry 3 – 05/08/26: Figuring out why greedy fails

When figuring out the greedy algorithm I at first tried to just say the 
greedy alogithm would always choose the cheapest path to the end, but this doesnt work
because it would reach all the relic chambers, I then made it so that it first goes to a relic chambers
. Even with this greedy still doesnt work, but it does make more sense. 

---


## Entry 4 – 05/09/26: Finishing explore recursion

when writing the explore function for part 6, the hardest part was making sure
to keep track of how the recursion changes what we need to search
without changing the other branches. I had to make sure that
when I choose a relic I have to remove it from the remaining relics list and add it to the 
relics visited list. But after the recursion I need to undo this.

---
## Entry 5 – 05/10/24: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

If given more time I would probably add more pruning if possible, and add checks for edge cases like
unreachable relics or multiple paths with the same costs. 

---

## Final Entry – 05/10/24: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|-----------------|
| Part 1: Problem Analysis | 1               |
| Part 2: Precomputation Design | 2               |
| Part 3: Algorithm Correctness | 1               |
| Part 4: Search Design | 1               |
| Part 5: State and Search Space | 1               |
| Part 6: Pruning | 1               |
| Part 7: Implementation | 1               |
| README and DEVLOG writing | 1               |
| **Total** | 9               |
