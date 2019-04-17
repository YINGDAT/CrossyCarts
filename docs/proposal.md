---
layout: default
title: Proposal
---


## {{ page.title }}

### Summary of the Project 
Our project is an adaptation of Space Invaders for Minecraft. The AI will be in an enclosed area with an x number of Ghasts. Ghasts are enemies in minecraft that fly around and shoot fireballs at the player. At each level, the number of Ghasts in the room will increase. The goal of our project is for the AI to learn how to kill the Ghasts without getting killed. The input is the Ghasts’ locations, how many are left to kill, the distance between the player and the Ghast, and where the Ghasts will shoot back. The output is where the agent will shoot and the location it will move to. The job of the AI is to determine which Ghast is the best one to kill and how to move to the position without getting shot. It should consider the cost of moving to each position before it decides which one to go to.  

### AI/ML Algorithms
We will be using reinforcement learning with Q-learning.

### Evaluation Plan
The metrics we will use to evaluate our model will be level completion time, lives taken, shot accuracy, and number of levels completed. Our baseline for failure is getting killed without killing any Ghasts at level 1, and our baseline for success is killing all of the Ghasts and clearing all of the levels. Some example evaluations are: +10 for killing a Ghast with a bow, +5 for making a Ghast kill another Ghast, +5 for deflecting the fireball, -5 for missing a shot, and -15 for getting hit. Since we are using reinforcement learning/Q-learning, our data will be continuously updated as the AI plays.

We will verify that the AI works based on whether it is able to clear levels or not. Some examples of basic sanity cases we will use are whether or not the AI can avoid getting shot and if the AI can pick the best Ghast to kill. Our moonshot case is if the AI can clear levels which have the Ghasts moving and shooting too fast for a human to play against. 


### Appointment with the Instructor 
Wednesday, April 24, 3:00pm
