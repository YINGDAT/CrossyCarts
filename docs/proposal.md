---
layout: default
title: Proposal
---


## {{ page.title }}

### Summary of the Project 
Our project is a Space Invaders game simulation in Minecraft. The goal of the game is to kill all of the aliens before they cross an “invasion line”. As the player progresses, the aliens move forward faster and shoot at the player more rapidly. The goal of our project is for the AI to learn how to kill the aliens without getting killed and before they “invade”. The input is the space invaders locations, how many are left to kill, the distance between the player, the closest aliens to the invasion line, and where the aliens will shoot back. The output is where the agent will shoot and the location it will move to. The job of the AI is to determine which alien is the best one to kill and how to move to the position without getting shot. It should consider the cost of moving to each position before it decides which one to go to.

### AI/ML Algorithms
We will be using reinforcement learning with Q-learning.

### Evaluation Plan
The metrics we will use to evaluate our model will be level completion time, lives taken, shot accuracy, and number of levels completed. Our baseline for failure is getting killed without killing any aliens at level 1, and our baseline for success is killing all of the aliens and clearing all of the levels. Some example evaluations are: +1 per second of survival, +1 per alien killed, +100 for level advancing, -100 for losing a life, and -500 for getting “invaded”. Since we are using reinforcement learning/Q-learning, our data will be continuously updated as the AI plays.

We will verify that the AI works based on whether it is able to clear levels or not. Some examples of basic sanity cases we will use are whether or not the AI can avoid getting shot and if the AI can pick the best alien to kill. Our moonshot case is if the AI can clear levels which have the aliens moving and shooting too fast for a human to play against. 

### Appointment with the Instructor 
Wednesday, April 24, 3:00pm
