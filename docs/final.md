---
layout: default
title:  Final
---
## Video

## Project Summary
CrossyCart is an Minecraft adaptation of the games Crossy Road™ and Frogger™.

In this version, the player must get on minecarts and get off of them at the right time in order to safely cross the tracks. Minecarts move back and forth along a 20 block minecart track with randomized safe drop-off points. If the player gets off at the wrong time they will be engulfed by flames and die.


<p align="center">

**Figure 1: Examples of successful (left) and unsuccessful (right) gameplay**

</p>

<p align="center">

<img src="img/example_success.gif" width="391" height="181" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_failure.gif" width="391" height="181" />

</p>


The player’s current position and velocity in the minecart are factors to consider when determining when to get off. Since the player in the minecart will always be moving even when it decides to get off the minecart, it should decide to get off a couple blocks away from the goal because by the time their action is executed their position would have changed (hopefully to where the safe block is).

Minecarts typically have a predefined speed of 8 m/s. In our CrossyCart game, however, minecart speeds are variable throughout the track since minecarts collide at both ends of the 20 block track in order to move back and forth. The collision briefly brings the minecart to a stop before accelerating it again which makes it more difficult to determine the right time to get off the minecart. Getting off 3 blocks away at a velocity of 1.5, for example, may land the player on the goal block, but if the velocity is 0.6 the block distance may be less. Because of this variability, it is necessary to use machine learning algorithms to create an AI that can reliably complete the track.

## Approaches

In our previous report we created an AI that was able to eventually complete 1 track with a predetermined goal block which served as our baseline. Since then, we have randomized the position of the goal block and changed our states and rewards in order to create an AI that is able to complete multiple tracks with different goal blocks.

Our AI automatically gets into position to get on the minecart and gets on the minecart. The main problem lies in when it decides to get off of the minecart. We chose to use q-tabular reinforcement learning because there is a moderate number of states with only two actions to choose from: get off (crouch) or nothing. Since q-learning is model free, we are also able to see the agent learn to complete the track and handle stochastic transitions (ex. changes in speed while riding).

**Track Set-up**

After running the program, the user is prompted to enter a number of tracks that the agent will have to cross. This inputted number is used to create n number of 20-block tracks each with its own randomized goal block. The x-coordinate of the randomized goal blocks for each track is stored in an array to create our states later.

**Q-Tabular Learning**

-States
    *Our
* Rewards


## Evaluation

## References
