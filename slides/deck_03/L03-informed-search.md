---
marp: true
title: CS 6460: Artificial Intelligence — Informed Search
author: George Rudolph
paginate: true
allowLocalFiles: true
math: katex

# Global default background (applies to all slides unless overridden)
backgroundImage: url('https://marp.app/assets/hero-background.svg')
backgroundColor: #ffffff

style: |
  :root { --uvu-green: #004b23; --uvu-green-2: #2d6a4f; --uvu-accent: #40916c; --text: #1a1a1a; }
  section { color: var(--text); }
  h1, h2, h3 { color: var(--uvu-green); }
  h1 { font-weight: 800; }
  h2 { font-weight: 700; text-align: center !important; }
  h3 { font-weight: 600; }
  p, li { font-size: 28px; line-height: 1.35; }
  table { font-size: 22px; border-collapse: collapse; }
  th { background: #e8f2ea; color: var(--uvu-green); font-weight: 700; }
  td, th { padding: 12px 16px; border-bottom: 1px solid #e5e5e5; }
  footer { 
    color: #e8e8e8; 
    background: linear-gradient(to bottom, 
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.15) 15%,
      rgba(255, 255, 255, 0.5) 50%,
      rgba(255, 255, 255, 0.5) 50%,
      rgba(255, 255, 255, 0.15) 85%,
      rgba(255, 255, 255, 0) 100%);
    padding: 12px 15px;
    backdrop-filter: blur(2px);
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
  }
  section::after { position: absolute; bottom: 20px; right: 30px; color: var(--text); font-size: 24px; }
  .two-column { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: center; }
  .two-column[style*="align-items: start"] { align-items: start; align-content: start; }
  .two-column[style*="align-items: start"] > div:first-child { padding-top: 0 !important; margin-top: 0 !important; align-self: start; }
  .two-column[style*="align-items: start"] > div:last-child { align-self: start; }
  .two-column p, .two-column li { font-size: 24px; line-height: 1.3; }
  .two-column strong { font-size: 25px; }
  .text-red { color: #d32f2f !important; }
  .text-green { color: #2d6a4f !important; }
  span.text-red { color: #d32f2f !important; }
  span.text-green { color: #2d6a4f !important; }
  .small-text {
    font-size: 20px !important;
    line-height: 1.3 !important;
  }
  .small-text li, .small-text p {
    font-size: 20px !important;
    line-height: 1.3 !important;
    margin-bottom: 6px;
  }
  .text-tiny {
    font-size: 14px !important;
    line-height: 1.2 !important;
    color: #666 !important;
  }
  .text-tiny p, .text-tiny li {
    font-size: 14px !important;
    line-height: 1.2 !important;
    margin-bottom: 4px;
  }
  .tiny-text {
    font-size: 14px !important;
    line-height: 1.2 !important;
    color: #666 !important;
  }
  .tiny-text p, .tiny-text li {
    font-size: 14px !important;
    line-height: 1.2 !important;
    margin-bottom: 4px;
  }
  .smaller-text {
    font-size: 16px !important;
    line-height: 1.25 !important;
  }
  .smaller-text p, .smaller-text li {
    font-size: 16px !important;
    line-height: 1.25 !important;
    margin-bottom: 5px;
  }
  .checkbox {
    font-size: 14px !important;
    display: inline-block;
    margin-right: 4px;
  }
  
---
<style scoped>
section {
  padding-top: 20px;
  padding-bottom: 10px;
}
h1 {
  margin-top: 8px;
  margin-bottom: 5px;
  line-height: 1.1;
}
h1:first-of-type {
  margin-top: 0;
}
.text-small {
  font-size: 18px !important;
  line-height: 1.2 !important;
  margin-top: 10px;
  margin-bottom: 8px;
}
.text-small p {
  font-size: 18px !important;
  line-height: 1.2 !important;
  margin: 4px 0;
}
img {
  margin: 8px 0;
}
</style>


<center>

# CS 6460: Artificial Intelligence
## Informed Search

<img src="assets/slide01_img01.png" alt="CS_6460_Artificial_Intelligence" width="600">

Instructor: George Rudolph
Utah Valley University Spring 2025

<div class = "tiny-text">

[These slides adapted from Dan Klein and Pieter Abbeel at UC Berkley]

</div>

</center>

---
# Learning Outcomes

<div class= "two-column">

<div>

1. Solve Problems using Informed Searches
- Heuristics
- Greedy Search
- A* Search
2. Model Problems as Graph Search

</div>

<div>

![Learning_Outcomes](assets/slide02_img01.png)

</div>

</div>

---

# Search and Models

<div class = "two-column">

<div>

- Search operates over models of the world
- The agent doesn’t actually try all the plans out in the real world!
- Planning is all <span style="color: #d32f2f;">in simulation</span>
- Your search is only as good as your models…

</div>

<div>

![Search_and_Models](assets/slide03_img01.png)

</div>

</div>

---

<center>

# Informed Search


<img src="assets/slide04_img01.png" alt="Informed_Search" width="700">

</center>

---
# Search Heuristics

<div class = "two-column">

<div>

A heuristic is:
- A function that <span style="color: #008000; font-weight: bold;">estimates</span> how close a state is to a goal
- Designed for a <span style="color: #d32f2f; font-weight: bold;">particular</span> search problem
- Examples: Manhattan distance, Euclidean distance

<img src="assets/slide05_img01.png" alt="Search_Heuristics" width="600px">

</div>

<div>

<img src="assets/slide05_img02.png" alt="Search_Heuristics" width="350">
<img src="assets/slide05_img03.png" alt="Search_Heuristics" width="350">

</div>

</div>

---

# Example: Heuristic Function

<center>

<img src="assets/slide06_img01.png" alt="Example_Heuristic_Function" width="800">

</center>

---

<center>

# Greedy Search

<img src="assets/slide07_img01.png" alt="Greedy_Search" width="700">

</center>

---
# Example: Greedy Heuristic Function

<center>

<img src="assets/slide06_img01.png" alt="Example_Heuristic_Function" width="800">

</center>

---
# Greedy Search

<div class = "two-column">

<div>

- Expand the node that seems closest…
- What can go wrong?

<img src="assets/slide09_img02.png" alt="Example_Heuristic_Function" width="100%">

</div>

<div>

<center>
<img src="assets/slide09_img03.png" alt="Example_Heuristic_Function" width="280">

</center>

<img src="assets/slide09_img05.png" alt="Example_Heuristic_Function" width="450">

</div>

</div>

---

# Greedy Search

<div class = "two-column" >

<div>

- Strategy: expand a node that you think is closest to a goal state
   - Heuristic: estimate of distance to nearest goal for each state

A common case
- Best-first takes you straight to the (wrong) goal


Worst-case  
- behaves like a badly-guided DFS

</div>

<div style="text-align: right;">

<img src="assets/slide10_img01.png" alt="Greedy_Search" width="350">

</div>

</div>

---
# Video of Demo Contours Greedy (Empty)
---
# Video of Demo Contours Greedy (Pacman Small Maze)
---

<center>

# A* Search

<img src="assets/slide13_img01.png" alt="A Star Section Image" width="800">

</center>

---

# A* Search

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; align-items: center;">

<div style="text-align: center;">
<strong>UCS</strong><br>
<img src="assets/slide14_img01.png" alt="A_Search" width="250">
</div>

<div style="text-align: center;">
<strong>Greedy</strong><br>
<img src="assets/slide14_img02.png" alt="A_Search" width="250">
</div>

<div style="text-align: center;">
<strong>A*</strong><br>
<img src="assets/slide14_img03.png" alt="A_Search" width="250">
</div>

</div>

---
# Combining UCS and Greedy
- Uniform-cost orders by path cost, or backward cost  g(n)
- Greedy orders by goal proximity, or forward cost  h(n)
- A* Search orders by the sum: f(n) = g(n) + h(n)
- S
- a
- d
- b
- G
- h=5
- h=6
- h=2
- 1
- 8
- 1
- 1
- 2
- h=6
- h=0
- c
- h=7
- 3
- e
- h=1
- 1
- Example: Teg Grenager
- S
- a
- b
- c
- e
- d
- d
- G
- G
- g = 0 h=6
- g = 1 h=5
- g = 2 h=6
- g = 3 h=7
- g = 4 h=2
- g = 6 h=0
- g = 9 h=1
- g = 10 h=2
- g = 12 h=0
![Combining_UCS_and_Greedy](assets/slide15_converted01.png)
![Combining_UCS_and_Greedy](assets/slide15_converted02.png)
![Combining_UCS_and_Greedy](assets/slide15_converted03.png)
![Combining_UCS_and_Greedy](assets/slide15_converted04.png)
![Combining_UCS_and_Greedy](assets/slide15_converted05.png)
![Combining_UCS_and_Greedy](assets/slide15_converted06.png)
![Combining_UCS_and_Greedy](assets/slide15_converted07.png)
![Combining_UCS_and_Greedy](assets/slide15_converted08.png)
![Combining_UCS_and_Greedy](assets/slide15_converted09.png)
![Combining_UCS_and_Greedy](assets/slide15_converted10.png)
![Combining_UCS_and_Greedy](assets/slide15_converted11.png)
![Combining_UCS_and_Greedy](assets/slide15_converted12.png)
![Combining_UCS_and_Greedy](assets/slide15_converted13.png)
![Combining_UCS_and_Greedy](assets/slide15_converted14.png)
![Combining_UCS_and_Greedy](assets/slide15_converted15.png)
![Combining_UCS_and_Greedy](assets/slide15_converted16.png)
![Combining_UCS_and_Greedy](assets/slide15_converted17.png)
![Combining_UCS_and_Greedy](assets/slide15_converted18.png)
![Combining_UCS_and_Greedy](assets/slide15_converted19.png)
![Combining_UCS_and_Greedy](assets/slide15_converted20.png)
![Combining_UCS_and_Greedy](assets/slide15_converted21.png)
![Combining_UCS_and_Greedy](assets/slide15_converted22.png)
![Combining_UCS_and_Greedy](assets/slide15_converted23.png)
![Combining_UCS_and_Greedy](assets/slide15_converted24.png)
![Combining_UCS_and_Greedy](assets/slide15_converted25.png)
![Combining_UCS_and_Greedy](assets/slide15_converted26.png)
![Combining_UCS_and_Greedy](assets/slide15_converted27.png)
![Combining_UCS_and_Greedy](assets/slide15_converted28.png)
![Combining_UCS_and_Greedy](assets/slide15_converted29.png)
![Combining_UCS_and_Greedy](assets/slide15_converted30.png)
![Combining_UCS_and_Greedy](assets/slide15_converted31.png)
![Combining_UCS_and_Greedy](assets/slide15_converted32.png)
![Combining_UCS_and_Greedy](assets/slide15_converted33.png)
![Combining_UCS_and_Greedy](assets/slide15_converted34.png)
![Combining_UCS_and_Greedy](assets/slide15_converted35.png)
![Combining_UCS_and_Greedy](assets/slide15_converted36.png)
![Combining_UCS_and_Greedy](assets/slide15_converted37.png)
![Combining_UCS_and_Greedy](assets/slide15_converted38.png)
![Combining_UCS_and_Greedy](assets/slide15_converted39.png)
![Combining_UCS_and_Greedy](assets/slide15_converted40.png)
![Combining_UCS_and_Greedy](assets/slide15_converted41.png)
![Combining_UCS_and_Greedy](assets/slide15_converted42.png)
![Combining_UCS_and_Greedy](assets/slide15_converted43.png)
---
# When should A* terminate?
- Should we stop when we put a goal in the fringe?
- No: only stop when we pull a goal off the fringe
- S
- B
- A
- G
- 2
- 3
- 2
- 2
- h = 1
- h = 2
- h = 0
- h = 3
![When_should_A_terminate_](assets/slide16_converted01.png)
![When_should_A_terminate_](assets/slide16_converted02.png)
![When_should_A_terminate_](assets/slide16_converted03.png)
![When_should_A_terminate_](assets/slide16_converted04.png)
![When_should_A_terminate_](assets/slide16_converted05.png)
![When_should_A_terminate_](assets/slide16_converted06.png)
![When_should_A_terminate_](assets/slide16_converted07.png)
![When_should_A_terminate_](assets/slide16_converted08.png)
![When_should_A_terminate_](assets/slide16_converted09.png)
![When_should_A_terminate_](assets/slide16_converted10.png)
![When_should_A_terminate_](assets/slide16_converted11.png)
![When_should_A_terminate_](assets/slide16_converted12.png)
---
# Is A* Optimal?
- What is wrong?
- Actual bad goal cost < estimated good goal cost
- We need estimates to be less than actual costs!
- A
- G
- S
- 1
- 3
- h = 6
- h = 0
- 5
- h = 7
![Is_A_Optimal_](assets/slide17_converted01.png)
![Is_A_Optimal_](assets/slide17_converted02.png)
![Is_A_Optimal_](assets/slide17_converted03.png)
![Is_A_Optimal_](assets/slide17_converted04.png)
![Is_A_Optimal_](assets/slide17_converted05.png)
![Is_A_Optimal_](assets/slide17_converted06.png)
![Is_A_Optimal_](assets/slide17_converted07.png)
![Is_A_Optimal_](assets/slide17_converted08.png)
![Is_A_Optimal_](assets/slide17_converted09.png)
---
# Admissible Heuristics
![Admissible_Heuristics](assets/slide18_img01.png)
---
# Idea: Admissibility
- Inadmissible (pessimistic) heuristics break optimality by trapping good plans on the fringe
- Admissible (optimistic) heuristics slow down bad plans but never outweigh true costs
![Idea_Admissibility](assets/slide19_img01.png)
![Idea_Admissibility](assets/slide19_img02.png)
![Idea_Admissibility](assets/slide19_converted01.png)
![Idea_Admissibility](assets/slide19_converted02.png)
---
# Admissible Heuristics
- A heuristic h is admissible (optimistic) if:
- where               is the true cost to a nearest goal
- Examples:
- Defining admissible heuristics is the biggest effort in using A* in practice
![Admissible_Heuristics](assets/slide20_img01.png)
![Admissible_Heuristics](assets/slide20_img02.png)
![Admissible_Heuristics](assets/slide20_converted01.png)
![Admissible_Heuristics](assets/slide20_converted02.png)
---
# Optimality of A* Tree Search
![Optimality_of_A_Tree_Search](assets/slide21_img01.png)
---
# Optimality of A* Tree Search
- Assume:
- A is an optimal goal node
- B is a suboptimal goal node
- h is admissible
- Claim:
- A will exit the fringe before B
- …
![Optimality_of_A_Tree_Search](assets/slide22_converted01.png)
![Optimality_of_A_Tree_Search](assets/slide22_img01.png)
![Optimality_of_A_Tree_Search](assets/slide22_img02.png)
---
# Optimality of A* Tree Search: Blocking
- Proof:
- Imagine B is on the fringe
- Some ancestor n of A is on the fringe, too (maybe A!)
- Claim: n will be expanded before B
- f(n) is less or equal to f(A)
- Definition of f-cost
- Admissibility of h
- …
- h = 0 at a goal
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_converted01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img02.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_converted02.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_converted03.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img03.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img04.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img05.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_converted04.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide23_img06.png)
---
# Optimality of A* Tree Search: Blocking
- Proof:
- Imagine B is on the fringe
- Some ancestor n of A is on the fringe, too (maybe A!)
- Claim: n will be expanded before B
- f(n) is less or equal to f(A)
- f(A) is less than f(B)
- B is suboptimal
- h = 0 at a goal
- …
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_img01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_img02.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_converted01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_converted02.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_converted03.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_img03.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_img04.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide24_img05.png)
---
# Optimality of A* Tree Search: Blocking
- Proof:
- Imagine B is on the fringe
- Some ancestor n of A is on the fringe, too (maybe A!)
- Claim: n will be expanded before B
- f(n) is less or equal to f(A)
- f(A) is less than f(B)
- n expands before B
- All ancestors of A expand before B
- A expands before B
- A* search is optimal
- …
![Optimality_of_A_Tree_Search_Blocking](assets/slide25_img01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide25_converted01.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide25_img02.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide25_img03.png)
![Optimality_of_A_Tree_Search_Blocking](assets/slide25_img04.png)
---
# Properties of A*
---
# Properties of A*
- …
- b
- …
- b
- Uniform-Cost
- A*
![Properties_of_A_](assets/slide27_converted01.png)
![Properties_of_A_](assets/slide27_converted02.png)
![Properties_of_A_](assets/slide27_converted03.png)
![Properties_of_A_](assets/slide27_converted04.png)
![Properties_of_A_](assets/slide27_converted05.png)
![Properties_of_A_](assets/slide27_converted06.png)
---
# UCS vs A* Contours
- Uniform-cost expands equally in all “directions”
- A* expands mainly toward the goal, but does hedge its bets to ensure optimality
- Start
- Goal
- Start
- Goal
![UCS_vs_A_Contours](assets/slide28_converted01.png)
![UCS_vs_A_Contours](assets/slide28_converted02.png)
![UCS_vs_A_Contours](assets/slide28_converted03.png)
![UCS_vs_A_Contours](assets/slide28_converted04.png)
---
# Video of Demo Contours (Empty) -- UCS
---
# Video of Demo Contours (Empty) -- Greedy
---
# Video of Demo Contours (Empty) – A*
---
# Video of Demo Contours (Pacman Small Maze) – A*
---
# Comparison
- Greedy
- Uniform Cost
- A*
![Comparison](assets/slide33_img01.jpg)
![Comparison](assets/slide33_img02.jpg)
![Comparison](assets/slide33_img03.jpg)
![Comparison](assets/slide33_converted01.png)
![Comparison](assets/slide33_converted02.png)
![Comparison](assets/slide33_converted03.png)
---
# A* Applications
![A_Applications](assets/slide34_img01.png)
---
# A* Applications
- Video games
- Path / routing problems
- Resource planning problems
- Robot motion planning
- Language analysis
- …
![A_Applications](assets/slide35_img01.png)
---
# Video of Demo Pacman (Tiny Maze) – UCS / A*
---
# Video of Demo Empty Water Shallow/Deep – Guess Algorithm
---
# Creating Heuristics
![Creating_Heuristics](assets/slide38_img01.png)
---
# Creating Admissible Heuristics
- Most of the work in solving hard search problems optimally is in coming up with admissible heuristics
- Often, admissible heuristics are solutions to relaxed problems, where new actions are available
- Inadmissible heuristics are often useful too
- 366
![Creating_Admissible_Heuristics](assets/slide39_converted01.png)
![Creating_Admissible_Heuristics](assets/slide39_converted02.png)
![Creating_Admissible_Heuristics](assets/slide39_converted03.png)
---
# Example: 8 Puzzle
- What are the states?
- How many states?
- What are the actions?
- How many successors from the start state?
- What should the costs be?
- Start State
- Goal State
- Actions
![Example_8_Puzzle](assets/slide40_converted01.png)
![Example_8_Puzzle](assets/slide40_img01.png)
![Example_8_Puzzle](assets/slide40_converted02.png)
![Example_8_Puzzle](assets/slide40_converted03.png)
![Example_8_Puzzle](assets/slide40_img02.png)
![Example_8_Puzzle](assets/slide40_converted04.png)
---
# 8 Puzzle I
- Heuristic: Number of tiles misplaced
- Why is it admissible?
- h(start) =
- This is a relaxed-problem heuristic
- 8
- Statistics from Andrew Moore
![8_Puzzle_I](assets/slide41_converted01.png)
![8_Puzzle_I](assets/slide41_img01.png)
![8_Puzzle_I](assets/slide41_converted02.png)
![8_Puzzle_I](assets/slide41_converted03.png)
---
# 8 Puzzle II
- What if we had an easier 8-puzzle where any tile could slide any direction at any time, ignoring other tiles?
- Total Manhattan distance
- Why is it admissible?
- h(start) =
- 3 + 1 + 2 + … = 18
![8_Puzzle_II](assets/slide42_converted01.png)
![8_Puzzle_II](assets/slide42_converted02.png)
---
# 8 Puzzle III
- How about using the actual cost as a heuristic?
- Would it be admissible?
- Would we save on nodes expanded?
- What’s wrong with it?
- With A*: a trade-off between quality of estimate and work per node
- As heuristics get closer to the true cost, you will expand fewer nodes but usually do more work per node to compute the heuristic itself
![8_Puzzle_III](assets/slide43_img01.png)
---
# Semi-Lattice of Heuristics
---
# Trivial Heuristics, Dominance
- Dominance: ha ≥ hc if
- Heuristics form a semi-lattice:
- Max of admissible heuristics is admissible
- Trivial heuristics
- Bottom of lattice is the zero heuristic (what does this give us?)
- Top of lattice is the exact heuristic
![Trivial_Heuristics_Dominance](assets/slide45_img01.png)
![Trivial_Heuristics_Dominance](assets/slide45_img02.png)
![Trivial_Heuristics_Dominance](assets/slide45_converted01.png)
---
# Graph Search
![Graph_Search](assets/slide46_img01.png)
---
# Tree Search: Extra Work!
- Failure to detect repeated states can cause exponentially more work.
- Search Tree
- State Graph
![Tree_Search_Extra_Work_](assets/slide47_converted01.png)
![Tree_Search_Extra_Work_](assets/slide47_converted02.png)
![Tree_Search_Extra_Work_](assets/slide47_img01.wmf)
![Tree_Search_Extra_Work_](assets/slide47_img02.wmf)
---
# BFS Graph Search Example
- we shouldn’t bother expanding the circled nodes: WHY?
![BFS_Graph_Search_Example](assets/slide48_converted01.png)
---
# Graph Search
- Idea: never expand a state twice
- How to implement:
- Tree search + set of expanded states (“closed set”)
- Expand the search tree node-by-node, but…
- Before expanding a node, check to make sure its state has never been expanded before
- If not new, skip it, if new add to closed set
- Important: store the closed set as a set, not a list
- Can graph search wreck completeness?  Why/why not?
- How about optimality?
---
# A* Graph Search Gone Wrong?
- S
- A
- B
- C
- G
- 1
- 1
- 1
- 2
- 3
- S (0+2)
- State space graph
- Search tree
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted01.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted02.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted03.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted04.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted05.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted06.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted07.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted08.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted09.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted10.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted11.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted12.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted13.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted14.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted15.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted16.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted17.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted18.png)
![A_Graph_Search_Gone_Wrong_](assets/slide50_converted19.png)
---
# Consistency of Heuristics
- Main idea: estimated heuristic costs ≤ actual costs
- Admissibility: heuristic cost ≤ actual cost to goal
- h(A) ≤ actual cost from A to G
- Consistency: heuristic “arc” cost ≤ actual cost for each arc
- h(A) – h(C) ≤ cost(A to C)
- Consequences of consistency:
- The f value along a path never decreases
- h(A) ≤ cost(A to C) + h(C)
- A* graph search is optimal
- 3
- A
- C
- G
- h=4
- h=1
- 1
- h=2
![Consistency_of_Heuristics](assets/slide51_converted01.png)
![Consistency_of_Heuristics](assets/slide51_converted02.png)
![Consistency_of_Heuristics](assets/slide51_converted03.png)
![Consistency_of_Heuristics](assets/slide51_converted04.png)
![Consistency_of_Heuristics](assets/slide51_converted05.png)
![Consistency_of_Heuristics](assets/slide51_converted06.png)
![Consistency_of_Heuristics](assets/slide51_converted07.png)
![Consistency_of_Heuristics](assets/slide51_converted08.png)
---
# Optimality
- Tree search:
- A* is optimal if heuristic is admissible
- UCS is a special case (h = 0)
- Graph search:
- A* optimal if heuristic is consistent
- UCS optimal (h = 0 is consistent)
- Consistency implies admissibility
- In general, most natural admissible heuristics tend to be consistent, especially if from relaxed problems
![Optimality](assets/slide52_img01.png)
---
# A*: Summary
- A* uses both backward costs and (estimates of) forward costs
- A* is optimal with admissible / consistent heuristics
- Heuristic design is key: often use relaxed problems
![A_Summary](assets/slide53_img01.png)
---
# Tree Search Pseudo-Code
![Tree_Search_Pseudo-Code](assets/slide54_img01.png)
---
# Graph Search Pseudo-Code
![Graph_Search_Pseudo-Code](assets/slide55_img01.png)
---
# Search Problem Example 1
![Search_Problem_Example_1](assets/slide56_img01.png)
![Search_Problem_Example_1](assets/slide56_img02.png)
---
# Search Problem Example 1 (solution)
![Search_Problem_Example_1_solution_](assets/slide57_img01.png)
![Search_Problem_Example_1_solution_](assets/slide57_img02.png)
