---
marp: true
title: L02 Uninformed Search
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

# Search

<div class = "text-small">

<img src="assets/L02_Uninformed_Search_0.png" alt="robot entering a maze with walls" width="600">

Instructor: George Rudolph

Utah Valley University Spring 2026

</div>

<div class="text-tiny">

slides adapted from Dan Klein and Pieter Abbeel of UC Berkley
see also ai.berkley.edu

</div>

</center>

---

# Learning Outcomes

<div class = "two-column">

<div>

1. Define Agents that Plan Ahead
1. Frame Problems as Search Problems
1. Implement Uninformed Search Algorithms
  * Depth\-First Search
  * Breadth\-First Search
  * Uniform\-Cost Search
1. Analyze Uninformed Search Algorithms using Big\-O complexity

</div>

<div>

<img src="assets/L02_Uninformed_Search_1.png" alt="Robot thinking about maximizing chances of getting apple from tree" width="400">

</div>

</div>

---

# Agents that Plan

<center>

<img src="assets/L02_Uninformed_Search_2.png" alt="robot with a thought bubble" width="400">

</center>


---


# Reflex Agents

<div class = "two-column">

<div>

* Reflex agents:
  * Choose action based on current percept \(and maybe memory\)
  * May have memory or a model of the world’s current state
  * Do not consider the future consequences of their actions
  * <span style="color:#ff0000">Consider how the world IS</span>


* Can a reflex agent be rational?

</div>

<div>

<img src="assets/L02_Uninformed_Search_3.png" alt="Robot jumping over a ravine to grab apple from tree" width="400">

</div>

</div>

---


# Planning Agents

<div class="two-column">

<div>

* Planning agents:
  * Ask “what if”
  * Decisions based on \(hypothesized\) consequences of actions
  * Must have a model of how the world evolves in response to actions
  * Must formulate a goal \(test\)
  * <span style="color:#ff0000">Consider how the world WOULD BE</span>
* Optimal vs\. complete planning
* Planning vs\. replanning

</div>

<div>

<img src="assets/L02_Uninformed_Search_4.png" alt="Robot using a long pole grabber to get apple from tree" width="400">

</div>

</div>

---


# Move to nearest dot and eat it

<center>

<img src="assets/example_plan.png" alt="example plan for eating dots" width="800">

</center>

---
# Precompute optimal plan, execute it

<center>

<img src="assets/example_plan.png" alt="example plan for eating dots" width="800">

</center>

---

<center>

# Search Problems

<img src="assets/L02_Uninformed_Search_5.png" alt="robot scanning horizon" width="800">

</center>

---

# Framing of Search Problem

<center>

<img src="assets/search_problem_definition.png" alt="robot scanning horizon" width="800">

</center>

---


# Search Problems Are Models

<center>

<img src="assets/L02_Uninformed_Search_16.png" alt="Uninformed Search 16" width="800">

</center>

---


# Example: Traveling in Romania

<div class="two-column">

<div>

<img src="assets/L02_Uninformed_Search_17.png" alt="graph of cities and roads in Romania" width="600">

</div>

<div>

* State space:
  * Cities
* Successor function:
  * Roads: Go to adjacent city with cost = distance
* Start state:
  * Arad
* Goal test:
  * Is state == Bucharest?
* Solution?

</div>

</div>

---


# What's in a State Space?

The <span style="color:#ff0000">world state</span> includes every detail of the environment

<center>

<img src="assets/L02_Uninformed_Search_18.png" alt="Pac-Man game screenshot showing world state" width="500">

</center>

A <span style="color:#ff0000">search state</span> keeps only the details needed for planning \(abstraction\)

<div class="two-column">

<div>

<span style="color: #185c33;">Problem: Path Planning</span>
  * States: \(x\, y\) location
  * Actions: <span style="color:#ff0000">NSEW</span>
  * Successor: update location only
  * Goal test: is \(x\,y\)=END

</div>

<div>

<span style="color: #185c33;">Problem: Eat\-All\-Dots</span>
  * States: \{\(x\,y\)\, dot <span style="color:#ff0000">booleans</span>\}
  * Actions: <span style="color:#ff0000">NSEW</span>
  * Successor: update location and possibly a dot boolean
  * Goal test: dots all false

</div>

</div>

---

# State Space Sizes?

<div class = "two-column">

<div>

* World state:
  * Agent positions: <span style="color: #ff0000;">120</span>
  * Food count: <span style="color: #ff0000;">30</span>
  * Ghost positions: <span style="color: #ff0000;">12</span>
  * Agent facing: <span style="color: #ff0000;">NSE</span>
* How many
  * World states?
  * $120 \times 2^{30} \times 12^{2} \times 4$
  * States for pathing?
  * $120$
  * States for eat\-all\-dots?
  * $120 \times 2^{30}$

</div>

<div>

<img src="assets/L02_Uninformed_Search_19.png" alt="Uninformed Search 19" width="400">

</div>

---


# Quiz: Safe Passage

<img src="assets/L02_Uninformed_Search_20.png" alt="Uninformed Search 20" width="100%">

<span style="color:rgb(224, 22, 83);">Problem: eat all dots while keeping the ghosts perma\-scared </span>  
<span style="color:rgb(224, 22, 83);">What does the state space have to specify?</span>   
  * agent position, dot booleans, power pellet booleans, remaining scared time

---




# State Space Graphs and Search Trees

<div class="two-column">

<div>

- Each branch is a possible choice

- Each node is a possible state

- Same state may occur in several branches

</div>

<div>

<img src="assets/L02_Uninformed_Search_21.png" alt="Uninformed Search 21" width="400">

</div>

</div>

---

# State Space Graphs

<div class="two-column">

<div>

* <span style="color:#ff0000">State space graph</span>: A mathematical representation of a search problem
  * <span style="color:#ff0000">Nodes</span> are \(abstracted\) world configurations
  * <span style="color:#ff0000">Arcs</span> represent successors \(action results\)
  * The <span style="color:#ff0000">goal test</span> is a set of goal nodes \(maybe only one\)
* In a state space graph\, each state occurs only once\!

<span style="color:#ff0000">We can rarely build this full graph in memory \(it’s too big\)\, but it’s a useful idea</span>

</div>

<div>

<img src="assets/state_space_graph.png" alt="Uninformed Search 21" width="400">

</div>

</div>

---
# An Abstract Example

<div class="two-column">

<div>

* <span style="color:#ff0000">State space graph</span>: A mathematical representation of a search problem
  * <span style="color:#ff0000">Nodes</span> are \(abstracted\) world configurations
  * <span style="color:#ff0000">Arcs</span> represent successors \(action results\)
  * The <span style="color:#ff0000">goal test</span> is a set of goal nodes \(maybe only one\)
* In a state space graph\, each state occurs only once\!

We can rarely build this full graph in memory \(it’s too big\)\, but it’s <span style="color:#ff0000">a useful idea</span>

</div>

<div>

<img src="assets/tiny_state_space_graph.png" alt="an example graph as state space" width="600">

*Tiny state space graph for a tiny search problem*
</div>

</div>

---

# Search Trees

<img src="assets/search_trees_01.png" alt="example search tree with a root and " width="80%">

<div class="small-text">

* A search tree:
  * A <span style="color:#ff00dd">“what if”</span> tree of plans and their outcomes
  * The <span style="color:#cc0000">start state</span> is the <span style="color:#cc0000">root</span> node
  * Children correspond to successors
  * <span style="color:#cc0000">Nodes</span> show <span style="color:#cc0000">states</span>, but correspond to <span style="color:#cc0000">PLANS</span> that achieve those states
  
  </div>

  <span style="color:#cc0000">For most problems\, we can never actually build the whole tree</span>

---

# State Space Graphs vs. Search Trees

<div class="two-column">

<div>

<img src="assets/tiny_graph_in_bubble.png" alt="tiny state graph" width="400px">

</div>

<div>

<img src="assets/tiny_graph_search_tree.png" alt="example search tree with a root and " width="400px">

</div>

</div>

- Each NODE in in the search tree is an entire PATH in the state space graph.
- We construct graph and search on demand, and we construct as little as possible
   - lazy construction \(could use generator...\)

---
 
# State Graph Size vs Search Space Size
<div class="two-column">


<div>

## Consider this 4\-state graph.

<img src="assets/four_state_graph.svg" alt="4-state graph with nodes s, a, b, G" width="100%">

</div>

<div>

## How big is its search tree \(from S\)?

<center>

<img src="assets/L02_Uninformed_Search_38.png" alt="search size is infinite" width="100px">

</center>

</div>

</div>

---

# Repeated Structure in Search Tree

<style scoped>
.three-column {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  align-items: center;
}
</style>

<div class="three-column">

<div>

## Consider this 4\-state graph.

<img src="assets/four_state_graph.svg" alt="4-state graph with nodes s, a, b, G" width="100%">

</div>

<div>

## First 4 levels of search tree

<img src="assets/four_state_search_tree.svg" alt="First 4 levels of search tree from state s" width="100%">

</div>

<div>

## How big is its search tree \(from S\)?

<center>

<img src="assets/L02_Uninformed_Search_38.png" alt="search size is infinite" width="100px">

</center>

</div>

</div>

---

<center>

# Tree Search

<img src="assets/L02_Uninformed_Search_39.png" alt="Uninformed Search 39" width="400">

</center>

---


# Search Example: Navigate Romania

<center>

<img src="assets/L02_Uninformed_Search_40.png" alt="a map of some cities with distances in Romania" width="900px">

</center>

---


# Searching with a Search Tree

<div class="two-column">

<div>

<img src="assets/L02_Uninformed_Search_41.png" alt="Uninformed Search 41" width="600">

</div>

<div>

<img src="assets/L02_Uninformed_Search_42.png" alt="Uninformed Search 42" width="600">

</div>

</div>

<img src="assets/L02_Uninformed_Search_43.png" alt="Uninformed Search 43" width="600">


---

# Search Algorithm 

1. Expand out potential plans \(tree nodes\)
1. Maintain a  <span style="color:#cc0000">fringe </span> of partial plans under consideration
1. Try to  <span style="color:#ff0000">expand</span>  as  <span style="color:#ff0000">few</span>  tree nodes as possible

---

# General Tree Search

<img src="assets/L02_Uninformed_Search_44.png" alt="Uninformed Search 44" width="80%">



* Important ideas:
  * Fringe
  * Expansion
  * Exploration strategy
* Main question:  <span style="color:#ff0000">which</span>  fringe nodes to explore?

---

# Example: Tree Search

<center>

<img src="assets/tree_search_example.svg" alt="Search tree example showing paths from s to G" width="300px">

</center>


---

<center>

# Depth-First Search

<img src="assets/L02_Uninformed_Search_45.png" alt="Uninformed Search 45" width="400">

</center>

---

# DFS 

**Idea:** Full speed ahead in one direction until you can't go further

**Strategy:** expand a deepest node first

**Implementation:** Fringe is a LIFO stack

---

# Try It: DFS Water Maze Simulation

<div class="small-text">

**Run the DFS simulation:**

**Linux/Mac:**
```bash
cd code
./run_dfs_simulation.sh
```

**Windows:**
```cmd
cd code
run_dfs_simulation.bat
```

**Or manually:**
```bash
cd code/dfs_water
python3 dfs_water_maze.py
```

**Requirements:** Python 3.13+ with numpy and matplotlib

Watch water spread through the maze using DFS - it goes deep first!

</div>

---

# Search Algorithm Properties

<img src="assets/L02_Uninformed_Search_46.png" alt="Uninformed Search 46" width="400">

---

# Properties 

* Complete: Guaranteed to find a solution if one exists?
* Optimal: Guaranteed to find the least cost path?
* Time complexity?
* Space complexity?

<div class = "two-column">

<div>

* Cartoon of search tree:
  * b is the branching factor
  * m is the maximum depth
  * solutions at various depths s
* Number of nodes in entire tree?
  * $1 + b + b^2 + … + b^m = O(b^m)$

</div>

<div>

<img src="assets/dfs_properties.png" alt="cartoon of DFS search" width="400">
</div>

</div>

---

# Even More DFS Properties

<div class = "two-column">

<div class = "small-text">

- What nodes does DFS expand?
   - Some left prefix of the tree
   - Could process whole tree
   - If $m$ is finite, takes $O(b^m)$ time
- How much space does fringe take?
   - only has siblings on path to root
   - $O(bm)$

- Is it complete?
   - $m$ could be infinite... 
   - only if we prevent cycles

- Is it optimal?
   - No
   - Finds leftmost solution
   - Does not consider cost or depth

</div>

<div>

<img src="assets/dfs_search_pattern.png" alt="Uninformed Search 46" width="10000">

</div>

</div>

---

# Breadth-First Search (BFS)

<div class = "two-column">

<div>

<img src="assets/L02_Uninformed_Search_47.png" alt="Uninformed Search 47" width="600">

**Strategy:** expand a <span style="color:#ff0000">shallowest node</span> <span style="color: dark green">first</span>

**Implementation:** Fringe is a FIFO queue
</div>

<div>

<img src="assets/bfs_tiers.png" alt="Uninformed Search 47" width="800">

</div>

</div>

---

# Try It: BFS Water Maze Simulation

<div class="small-text">

**Run the BFS simulation:**

**Linux/Mac:**
```bash
cd code
./run_bfs_simulation.sh
```

**Windows:**
```cmd
cd code
run_bfs_simulation.bat
```

**Or manually:**
```bash
cd code/bfs_water
python3 bfs_water_maze.py
```

**Requirements:** Python 3.13+ with numpy and matplotlib

Watch water spread level by level using BFS - notice the difference from DFS!

</div>

---

# BFS Properties

<div class="two-column">

<div class= "small-text">

- What nodes does BFS expand?
   - processes all nodes above the shallowest solution $s$
   - search time is $O(b^s)$

- How much space does fringe take?
  - $O(b^s)$

- Is it complete?
   - If solution exists, $s$ must be finite
   - So yes

- Is it optimal?
   - only if all costs are 1 (or equal)

</div>

<div>

<img src="assets/bfs_search_pattern.png" alt="a drawing of bfs search pattern" width="800">

</div>

</div>

---

# DFS vs BFS

<img src="assets/L02_Uninformed_Search_48.png" alt="Uninformed Search 48" width="1000">

---

# Quiz: DFS vs BFS

1. When will BFS outperform DFS?

1. When will DFS outperform BFS?

---


# Example: Maze Water with BFS


- BFS spreads out in concentric circles from root.
- Explores a lot of the state space

---

# Example: Maze Water with DFS

- Explores less but finds a terrible solution.
- It is checking for repeated states
   - Otherwise it would never complete


---


# Iterative Deepening

<div class="two-column">

<div>

* Idea: get DFS’s space advantage with BFS’s time / shallow\-solution advantages
  * Run a DFS with depth limit 1\.  If no solution…
  * Run a DFS with depth limit 2\.  If no solution…
  * Run a DFS with depth limit 3\.  …\.\.
* Isn’t that wastefully redundant?
  * Generally most work happens in the lowest level searched\, so not so bad\!

</div>

<div>

<img src="assets/iterative_deepening.png" alt="Uninformed Search 48" width="400">

</div>

---

# Cost-Sensitive Search

<center>
<img src="assets/cost_sensitive_header.svg" alt="a graph showing smany nodes, each with varying weights" width="60%">
</center>

BFS finds the shortest path in terms of number of actions.

It does not find the least\-cost path\.  We will now cover

a similar algorithm which does find the least\-cost path\.

---

<center>

# Uniform Cost Search (UCS)

<img src="assets/ucs_mound.png" alt="decorative picture of a mound" width="800">

</center>

---
# UCS Profile

<img src="assets/cost_sensitive_header.svg" alt="a graph showing many nodes, each with varying weights" width="70%">

Strategy: expand a cheapest node first

Fringe is a priority queue \(priority: cumulative cost\)

---

# Example Cost profile 

<img src="assets/cost_sensitive_search_tree.svg" alt="a graph showing the cost profile of traversing paths in the tree" width="50%">

---

# Uniform Cost Search (UCS) Properties

<div class="two-column">

<div>

* What nodes does UCS expand?
  * All nodes with cost less than cheapest solution
  * Let solution cost = $C^*$
  * Let arcs cost $\geq \varepsilon$
  * “effective depth” $\approx C^*/\varepsilon$
  * Takes time $O(b^{C^*/\varepsilon})$
* How much space does the fringe take?
  * $O(b^{C^*/\varepsilon})$
* Is it complete?
  *Yes if: best solution has a finite cost and minimum arc cost is positive
* Is it optimal?
  * Yes\!  Proof via $A^*$
</div>

<div>

<img src="assets/ucs_properties.png" alt="a graph showing the cost profile of traversing paths in the tree" width="100%">
</div>

</div>

---

# Uniform Cost Issues

<div class = "two-column">

<div>

* UCS explores increasing cost contours
* The good: UCS is complete and optimal\!
* The bad:
  * Explores options in every “direction”
  * No information about goal location

We’ll fix the bad soon\!

</div>

<div>

<img src="assets/ucs_issues.png" alt="a graph showing the cost profile of traversing paths in the tree" width="350px">
</div>

</div>

---

# Guess Which One --- BFS or UCS?

<div class="small-text">

**Run the simulation:**

**Linux/Mac:**
```bash
cd code
./run_guess_simulation.sh
```

**Windows:**
```cmd
cd code
run_guess_simulation.bat
```

**Or manually:**
```bash
cd code/guess_bfs_ucs
python3 guess_bfs_water_maze.py
```

**Requirements:** Python 3.13+ with numpy and matplotlib

**The maze has:**
- Shallow water (cost 1) - light blue background
- Deep water (cost 2) - dark blue background

</div>

---

# Guess Which of the Three --- DFS, BFS, UCS

<div class="small-text">

**Run the simulation:**

**Linux/Mac:**
```bash
cd code
./run_guess_ucs_simulation.sh
```

**Windows:**
```cmd
cd code
run_guess_ucs_simulation.bat
```

**Or manually:**
```bash
cd code/guess_bfs_ucs
python3 guess_ucs_water_maze.py
```

**Requirements:** Python 3.13+ with numpy and matplotlib

**The maze has:**
- Shallow water (cost 1) - light blue background
- Deep water (cost 2) - dark blue background

</div>

---


# The One Queue

<div class = "two-column">

<div>

* All search algorithms same except different fringe strategies
* All fringes are priority queues: collections of nodes with attached priorities
* For DFS and BFS, you can avoid the $log(n)$ overhead from an actual priority queue by using stack or queue

* Can create one implementation that takes a variable queuing object (Stack is a LIFO Queue...)
* but don't do that for this class

 </div> 

<div>

<img src="assets/L02_Uninformed_Search_52.png" alt="Uninformed Search 52" width="600">

</div>

</div>

---

# Search and Models

<div class = "two-column">


<div>

* Search operates over models of the world
* The agent doesn’t actually try all the plans out in the real world\!
* Planning is all "in simulation"
* Your search is only as good as your models…

</div>

<div>

<img src="assets/L02_Uninformed_Search_53.png" alt="Uninformed Search 53" width="400">

</div>

</div>

---


# State Space Example

<img src="assets/L02_Uninformed_Search_54.png" alt="Uninformed Search 54" width="650">


---


# State Space Example (Solution)

<img src="assets/L02_Uninformed_Search_55.png" alt="Uninformed Search 55" width="580">


---


# Search Problem Example

<img src="assets/L02_Uninformed_Search_56.png" alt="Uninformed Search 56" width="450">


---


# Search Problem Example (solution)

<div class = "two-column">

<div>

<img src="assets/L02_Uninformed_Search_57.png" alt="Uninformed Search 57" width="600">

</div>

<div>

<img src="assets/L02_Uninformed_Search_58.png" alt="Uninformed Search 58" width="100%">

</div>

</div>

