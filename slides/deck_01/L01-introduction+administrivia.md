---
marp: true
title: L01 Introduction and Administrivia
author: George Rudolph
paginate: true

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
  .two-column img {
    max-width: 100%;
    max-height: 50vh;
    width: auto;
    height: auto;
    object-fit: contain;
  }
  section img:not(.image-grid img):not(.triangle-grid img):not(.two-column img) {
    max-width: 100% !important;
    max-height: 60vh !important;
    width: auto !important;
    height: auto !important;
    object-fit: contain !important;
  }
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
  .checkbox {
    font-size: 14px !important;
    display: inline-block;
    margin-right: 4px;
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  .car-sequence img {
    opacity: 0;
    animation: fadeIn 0.5s ease-in forwards;
  }
  .car-sequence img:nth-child(1) { animation-delay: 0s; }
  .car-sequence img:nth-child(2) { animation-delay: 0.1s; }
  .car-sequence img:nth-child(3) { animation-delay: 0.2s; }
  .car-sequence img:nth-child(4) { animation-delay: 0.3s; }
  .car-sequence img:nth-child(5) { animation-delay: 0.4s; }
  .car-sequence img:nth-child(6) { animation-delay: 0.5s; }
  .car-sequence img:nth-child(7) { animation-delay: 0.6s; }
  .car-sequence img:nth-child(8) { animation-delay: 0.7s; }
  .car-sequence img:nth-child(9) { animation-delay: 0.8s; }
  .car-sequence img:nth-child(10) { animation-delay: 0.9s; }
  .car-sequence img:nth-child(11) { animation-delay: 1.0s; }
  .car-sequence img:nth-child(12) { animation-delay: 1.1s; }
  .car-sequence img:nth-child(13) { animation-delay: 1.2s; }
  .car-sequence img:nth-child(14) { animation-delay: 1.3s; }
  .car-sequence img:nth-child(15) { animation-delay: 1.4s; }
  .car-sequence img:nth-child(16) { animation-delay: 1.5s; }
  .car-sequence img:nth-child(17) { animation-delay: 1.6s; }
  .car-sequence img:nth-child(18) { animation-delay: 1.7s; }
  .car-sequence img:nth-child(19) { animation-delay: 1.8s; }
  .car-sequence img:nth-child(20) { animation-delay: 1.9s; }
  .image-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 2px;
    margin-top: 10px;
    max-height: 85vh;
    align-content: start;
  }
  .image-grid > img {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 220px;
  }
  .image-pair {
    display: flex !important;
    flex-direction: row !important;
    gap: 2px;
    width: 100%;
    align-items: center;
    justify-content: center;
  }
  .image-pair img {
    flex: 1 1 50% !important;
    max-height: 220px !important;
    width: auto !important;
    height: auto !important;
    object-fit: contain !important;
    display: block !important;
  }
  .triangle-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 2px;
    margin-top: 20px;
    max-width: 90%;
    margin-left: auto;
    margin-right: auto;
  }
  .triangle-grid img:first-child {
    grid-column: 1 / -1;
    justify-self: center;
    max-width: 70%;
    max-height: 450px;
  }
  .triangle-grid img:not(:first-child) {
    max-height: 400px;
    width: 100%;
    height: auto;
    object-fit: contain;
  }

---

# CS 6460: Artificial Intelligence

# Introduction

![](assets/images_00.png)

Instructor: George Rudolph

Utah Valley University Spring 2026

\(slides adapted from Dan Klein\, <span style="color:#000000"> </span> Pieter Abbeel\, Anca Dragan\, et al\)


---
<!-- slide 2 -->

# Sci-Fi AI?

<div class="image-grid">

![](assets/images_01.png)

![](assets/images_02.png)

![](assets/image_04.png)

</div>

---

<!-- slide 3 -->

<div class="triangle-grid">

![](assets/images_08.png)

![](assets/images_09.png)

![](assets/images_10.png)

</div>

---

# Learning Outcomes

<div class="two-column">

<div>

1. What is artificial intelligence?

2. What can AI do?

3. What is this course?

</div>

<div>

![](assets/images_11.png)

</div>

</div>

---

# What is AI?

<div class="two-column">

<div>

The science of making machines that:
- Think like people
- Think rationally

</div>

<div>

![](assets/images_12.png)

</div>

</div>

---

# Rational Decisions

* We’ll use the term  __rational__  in a very specific\, technical way:
  * Rational: maximally achieving pre\-defined goals
  * __Rationality__ only concerns what decisions are made
      - not the thought process behind them
  * Goals are expressed in terms of the  __utility__  of outcomes
  * <span style="color:#1212d2"> Being rational means </span>  <span style="color:#1212d2"> __maximizing your expected utility__ </span>


A better title for  <span style="color:#00b050">this course </span>  <span style="color:#ff0000">might</span>  be:

<center>
<span style="color:#1212d2">Computational Rationality</span> or 
<span style="color:#1212d2">Rational Agents </span>
</center>

---

# <span style="color:#00b050">Maximize</span> Your <span style="color:#ff0000">Expected Utility</span>

![](assets/images_13.png)

---

# Expected Utility

Consequences of an action, context, other actors expressed as a weighted average of the utilities of all possible outcomes.

Goal: **Maximize** expected utility as a convex optimization problem

---

# Related to

- Utilitarianism (Consequntialism) – Jeremy Bentham

- Utility rather than values, could be Virtue Ethics – Aristotle

- Deontology (Duty based ethics)

---

# Self-interest

- What is an agent that is good about acting for itself? Humans! 

- Replicating the brain would be an AI, right?

---

# What About the Brain?

<div class="two-column">

<div>

![](assets/images_18.png)

</div>

<div>

![](assets/images_19.png)

</div>

</div>

<div class="small-text">

_Brains \(human minds\) are very good at making rational decisions\, but not perfect_

_Brains aren't as modular as software\, so hard to reverse engineer\!_

_"Brains are to intelligence as wings are to flight"_

_Lessons learned from the brain: memory \(data\) and simulation \(computation\) are key to decision making_

</div>

---
# Course Topics 

<div class = "two-column">

<div>

* Part I: Making Decisions
  * Fast search / planning
  * Heuristic and Adversarial search
* Part II: Reasoning under Uncertainty
  * Bayesian Networks
  * Markov Decision Processes
  * Reinforcement Learning

</div>

<div>

* Part III
  * Independent Study
* Throughout: Applications
  * Natural language\, vision\, robotics\, games\, …

</div>

---

# What's Novel in Modern AI?

* Deep Learning (CNNs, Transformers) has revolutionized many AI applications
* Historically feature engineering was done by hand
* Even today for most projects 80% of effort is in data preparation
* Generative AI has transformed AI capabilities
  * Generative Adversarial Networks (GANs) for realistic image generation
  * Diffusion models (DALL-E, Stable Diffusion) for high-quality image synthesis
  * Large Language Models (LLMs) for text generation and understanding
  * Foundation models trained on massive data can be adapted to many tasks
* An AI may learn the utility function along with the data
  * Function to optimize may not be known beforehand

---

# Logistics

![](assets/images_22.png)

---

# Canvas

* Syllabus
* Course schedule
* Slides and notes
* Homework
* Exams
* Grades

---

# GitHub

* Copy starting Code for Projects from zip file in Canvas
* Put in own private GitHub Repository
  * Must be private\, NOT public
* Add your instructor as a collaborator on your copy
  * Clone the repo to your local machine
* Create a new branch in your copy for each project (search, multiagent, reinforcement, tracking, <independent study>)
* Commit changes for your solution in the respective branch
  * Push to your remote repository
* Don't ask me to use pull requests on branches--it's an extra step I don't need

---

# Communicate

* Email or Teams messages
* Teams video conference with instructor
* Canvas Discussion posts related to topics
  * Post as\-needed
  * Burning question that you want answers to
  * Muddiest Point that you want clarification on
  * Can come from readings\, slides\, projects\, other sources

* Topic Hour: Propose 4pm Tuesday; join if available

---

# Grading Projects

* Find project descriptions and starting code from GitHub
* Submit Sumit a link to your repo/branch in Canvas
* 4 projects have an autograding script  <span style="color:#ff0000">autograder\.py</span>
  * Objective standard
  * Incremental development of projects
  * You know how you’re doing
  * Faster feedback cycle
* Independent Study project is manually graded
  * cannot submit after last day of class
---

# Class Instruction

* This course is independent study on AI
* Well\-defined
  * Schedule
  * Set of readings
  * Homework
  * Exams
  * Programming projects to complete
* Very limited instruction and faculty supervision
* Requires individual initiative and responsibility
* Is not self\-paced
  * Assignments have expected due dates

---

# Helpful Prerequisites

* Admitted to a graduate program \(you are\)
* Some basic Python programming experience
* Familiar with
  * Basic data structures and algorithms like searching and sorting
  * Basic probability and statistics
  * Some calculus is helpful but not required

---

# Direct Instruction

* No direct instruction
* Office Hours \(on Teams\, or  in\-person\)
  * Posted
* Project Parties??? \(next slide\)

---

# Project Parties???

* Collaborate with another student on projects 1\-4 if you want
  * But you must write your own code\, not copy each other’s code
* Independent Study project can be a group of 2 project
  * Single submission for the whole group
  * Individual grading
  * 30% peer grading \(from the group\) \+ 70% instructor grade
  * Must get instructor approval of topic from instructor
* Get together online or in person before each deadline
* Can get guidance from the instructor

---

# Homework

* 4 Homeworks
* Individual work
* Engage with material differently than coding projects
* Preparation for mid\-term and final exams

---

# Projects

![](assets/images_24.png)

* See Canvas for Due Dates
* See zip file for starting code to put in your repo
* Python 3\.13 or compatible
* Autograded
* <span style="color:#ff0000"> __Projects give you hands\-on experience with the algorithms__ </span>
* <span style="color:#ff0000"> __Not just theory__ </span>

---

# Late Policy

* Late penalty is 10% per day up to 5 business days
  * No submission after 5 business days
* Exams and independent study project may not be submitted late
* Instructor may grant exceptions or extensions
  * Case\-by\-case basis
    * Ask ASAP if you feel you need one
  * Example: health or medical reasons or an emergency
* Sometimes you figure something out on a later project that builds on an earlier project
  * you may be allowed to resubmit the earlier project for improved score
  * Check with your instructor if this happens

---

# Assessments

- Midterm Exam

- Final Exam

## Exams

In Canvas \(see for dates\)

Multiple Choice, Some short answer

Not Necessarily Easy

Available for 2\-3 days each

Open Book? Harder Questions

Already stressed about the exams? Prepare good notes

---

# Instruction vs. Assessment

__Assessment__

Measure knowledge\, skill

Each student on their ownMay not successfully complete

__Instruction__

Grow knowledge

Collaborate\, work until success

* These  two goals don’t mix
* Lecture material/ Videos / Discussion / Projects are instruction
  * Usually collaborative\, work until success \(but please no spoilers\)
* Exams are assessment
  * on your own \(harder\)

---

# Grade Breakdown

Homework \(20%\)

Projects \(50%\)

Midterm \+ Final \(30%\)

---

# Student Wellness

* UVU CS courses are rigorous and mentally demanding
* Overwhelmed by the course? Contact your instructor or Student Support Services\.
* If you need professional help\, contact Student Health Services

---

# Academic Honesty

* No consultation or collaborators for Exams
  * Including the Internet\, Gen AI
* Acknowledge all collaborators and sources on projects
* Copying  <span style="color:#ff0000">someone else’s code </span> and submitting it as your own is
  * asking for a grade you did not earn and
  * claiming mastery of skills of which you have not demonstrated mastery
  * Gen AI can be used as an aid\, but not a crutch or a replacement

---

# Required Textbook

Russell & Norvig\, AI: A Modern Approach\, 4th Ed\.

![](assets/images_26.png)

---


# A (Short) History of AI

<div class = "two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.1; margin-bottom: 0; font-size: 18px !important;">

**1940s—1950s: Foundations**
* 1943: McCulloch & Pitts
* 1950: Turing
* 1956: Dartmouth

**1960s—1980s**
* Game programs
* Expert systems → Winter

**1990s—2011**
* ML, probabilistic
* Bayesian methods

</div>

<div class="small-text" style="line-height: 1.1; margin-bottom: 0; font-size: 18px !important;">

**2012—2024: Deep Learning & Gen AI**
* **2012**: ImageNet
* **2014**: GANs
* **2016**: AlphaGo
* **2017**: Transformers
* **2018**: BERT
* **2019**: GPT-2
* **2020**: GPT-3
* **2021**: DALL-E
* **2022**: ChatGPT
* **2023**: GPT-4
* **2024**: Agentic AI

</div>

</div>

---


# What Can AI Do Today?

<div class = "two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.2; font-size: 18px !important;">

**Quiz: Which can be done? (2024)**

* <span class="checkbox">✅</span> Play Jeopardy?
* <span class="checkbox">✅</span> Win chess vs. humans?
* <span class="checkbox">✅</span> Win Go vs. best?
* <span class="checkbox">✅</span> Play table tennis?
* <span class="checkbox">⚠️</span> Grab cup, put on shelf?
* <span class="checkbox">❌</span> Unload dishwasher?
* <span class="checkbox">⚠️</span> Drive on highway?
* <span class="checkbox">❌</span> Drive city streets?
* <span class="checkbox">✅</span> Buy groceries online?
* <span class="checkbox">⚠️</span> Buy groceries in store?
* <span class="checkbox">✅</span> Prove math theorem?
* <span class="checkbox">⚠️</span> Perform surgery?
* <span class="checkbox">⚠️</span> Unload dishwasher (with person)?
* <span class="checkbox">✅</span> Translate (real-time)?
* <span class="checkbox">✅</span> Write funny story?

</div>

<div style="max-height: 60vh;">

![](assets/images_30.png)

</div>

</div>

---


# AI Story Generation: Then and Now

<div class="two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.2;">

**1984: Tale-Spin**
* "Joe Bear ate beehive" — wrong
* "Gravity drowned" — error
* Missing context

![](assets/images_31.png)

</div>

<div class="small-text" style="line-height: 1.2;">

**2024: Modern LLMs**
* <span class="checkbox">✅</span> Coherent narratives
* <span class="checkbox">✅</span> Context awareness
* <span class="checkbox">⚠️</span> Factual errors
* <span class="checkbox">⚠️</span> Hallucinations
* <span class="checkbox">⚠️</span> Consistency issues

**Key:** Improved but reasoning challenges remain

</div>

</div>



---


# Natural Language & Large Language Models

<div class="two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.1; font-size: 18px !important;">

* **Speech Technologies**
  * Voice assistants (Siri, Alexa)
  * Real-time transcription
  * Natural text-to-speech

* **LLMs (2024)**
  * GPT-4, Claude 3, Gemini
  * Code generation (Copilot)
  * Translation, Q&A
  * Multimodal capabilities

* **Applications**
  * Content creation
  * Code assistance
  * Chatbots
  * Research synthesis

* **Challenges:** Hallucinations, bias, deepfakes, privacy

</div>

<div style="max-height: 55vh;">

![](assets/images_32.png)

</div>

</div>


---


# Computer Vision (2024)

<div class="two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.0; font-size: 17px !important; margin-bottom: 0;">

* **Capabilities**
  * Object detection (YOLO, DETR)
  * Segmentation (SAM)
  * Image generation (DALL-E 3, Midjourney)
  * Medical imaging, AV perception

* **Multimodal AI**
  * Vision-language (GPT-4V)
  * Image-text conversion
  * Video understanding

* **Applications**
  * Medical diagnosis, Manufacturing QC
  * Security, AR/VR

</div>

<div style="max-height: 55vh;">

![](assets/images_36.png)

</div>

</div>


---


# Game Agents & AI in Games

<div class="two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.2;">

* **Milestones**
  * 1997: Deep Blue (Chess)
  * 2016: AlphaGo (Go)
  * 2017: AlphaZero
  * 2019: MuZero

* **Current (2024)**
  * Game NPCs/opponents
  * Strategy game AI
  * General game-playing

* **Key Insight**
  * Specialized → general
  * Self-learning
  * Transfer learning

</div>

<div style="max-height: 45vh;">

![](assets/images_37.png)

</div>

</div>


---


<div class="two-column" style="align-items: center;">

<div>

![](assets/images_39.png)

</div>

<div class="small-text">

**AlphaGo vs. Lee Sedol (2016)**

Historic moment: AI defeated world Go champion

**Key:** Specialized → general-purpose learning

</div>

</div>

---

# Reinforcement Learning Game Agents

Pixels as the perception! Way harder. Way more games, but fun
What can using pixels in the real world (cameras) give us?


---


# Robotics (2024)

<div class="two-column" style="align-items: start">

<div class="small-text" style="line-height: 1.0; font-size: 17px !important; margin-bottom: 0;">

* **Applications**
  * Warehouse, manufacturing
  * Service (hospitals, hotels)
  * Agricultural, delivery

* **Advanced**
  * Boston Dynamics (Atlas, Spot)
  * Humanoid (Tesla Optimus, Figure AI)
  * Surgical (da Vinci), Drones

* **Challenges**
  * Real-world vs. simulation
  * Safety, reliability, cost
  * Human-robot collaboration

* **In this class:** AI planning/control, not mechanical

</div>

<div style="max-height: 20vh;">

![](assets/images_40.png)

</div>

</div>

---

# Robot Learning (2024)

<div class="two-column">

<div>

* **Current Research Focus**
  * End-to-end learning from demonstration
  * Sim-to-real transfer learning
  * Multi-task learning for robots
  * Foundation models for robotics

* **Key Advances**
  * Visual learning for manipulation
  * Imitation learning and reinforcement learning
  * Human-robot collaboration
  * General-purpose robot manipulation

</div>

<div>

* **Challenges**
  * Real-world deployment reliability
  * Safety in human environments
  * Generalization across tasks

</div>

</div>

---

# Autonomous Vehicles (2024)

![](assets/images_44.png)

---

# Current State of Self-Driving Cars

<div class="two-column">

<div class = "text-small">

* **Deployed (Limited)**
  * Waymo: Phoenix, San Francisco (fully autonomous)
  * Cruise: San Francisco (suspended 2024)
  * Tesla: Full Self-Driving (supervised, Level 2)

* **Why It's So Hard:**
  * Continuous decision-making
  * Multi-agent environment
  * Partially observable (can't see everything)
  * Safety-critical (zero tolerance for errors)
  * Edge cases and rare scenarios

</div>

<div>

* **Key Challenges:**
  * Weather conditions
  * Unpredictable human behavior
  * Regulatory and liability issues
  * Public trust and acceptance

</div>
</div>

---


# Why Autonomous Driving is Challenging

<div class="two-column">

<div class="small-text" style="line-height: 1.2;">

**The Problem: Static vs. Dynamic**

* **Snapshot view:** Car appears to have space
* **Reality:** Everything is moving
* **When car accelerates:** Space disappears quickly
* **Need:** Predict future states, not just current

**Key Challenges:**

* **Temporal reasoning:** What will happen next?
* **Multi-agent:** Other cars, pedestrians moving
* **Uncertainty:** Can't predict all behaviors
* **Safety-critical:** Must be right 100% of time

</div>

<div style="max-height: 60vh;">

![](assets/images_48.png)

**Example:** Static view shows space, but dynamic reality requires predicting movement

</div>

</div>


---


# Autonomous Driving: Complex Scenarios

<div class="two-column">

<div class="small-text" style="line-height: 1.2;">

**Real-World Complexity:**

* **Highway:** Relatively easier
* **City streets:** Much harder
  * Multiple agents at intersections
  * Pedestrians, cyclists
  * Construction, weather
  * Edge cases (emergency vehicles, animals)

* **Requires:**
  * Agility and awareness
  * Real-time decision making
  * Handling uncertainty
  * Safety guarantees

</div>

<div style="max-height: 60vh;">

![](assets/images_52.png)

![](assets/images_65.png)

</div>

</div>


---


**Progress in Autonomous Vehicles (2024):**

* Waymo: millions of autonomous miles
* Tesla FSD Beta: hundreds of thousands of users
* Robotaxis in select cities

**Key Question: What is the utility function of a self-driving car?**

---

# Utility Functions in AI

<div class = "two-column">

<div>

## Clear Utility Function

**Games:**
* Win the game
* Maximize score
* Clear, measurable objectives

</div>

<div>

## Complex Utility Function

**Real-World Applications:**
* Safety vs. efficiency trade-offs
* Ethical dilemmas (trolley problem)
* Multiple stakeholders' interests
* Long-term vs. short-term goals

</div>

</div>

---

# Challenges with Utility Functions

* Even in games, clear utility doesn't always give desired behavior
* In robotics, optimizing single metrics can lead to unintended consequences
  * Example: Quadrotor optimizing flight time → rockets straight up
  * Need to consider safety, smoothness, energy efficiency
* Real-world applications require multi-objective optimization

---

# Designing Rational Agents

![](assets/images_82.png)



* An  __agent__  is an entity that  _perceives_  and  _acts_ \.
* A  __rational agent__  _ _ selects actions that maximize its \(expected\)  __utility__ \.
* Characteristics of the  __percepts\, environment\,__  and  __action space __ dictate techniques for selecting rational actions
* <span style="color:#333399"> __This course __ </span>  <span style="color:#333399">is about:</span>
  * General AI techniques for a variety of problem types
  * Learning to recognize when and how a new problem can be solved with an existing technique
---

Quick recap: what will we do in this class?

---

# Pac-Man as an Agent

![](assets/images_83.png)

Pac\-Man is a registered trademark of Namco\-Bandai Games\, used here for educational purposes

---

# Pac man! 

- How many of you have played this game? 
- It’s surprisingly hard, but you’ll solve it in this class!

---

# Maximize  <span style="color:#ff0000">Your</span> Expected Utility

![](assets/images_84.png)

