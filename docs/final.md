---
layout: default
title:  Final
---

## Video

---

## Project Summary
CrossyCart is an Minecraft adaptation of the games Crossy Road™ and Frogger™.

In this version, the player must get on minecarts and get off of them at the right time in order to safely cross the tracks. Minecarts move back and forth along a 20 block minecart track with randomized safe drop-off points. If the player gets off at the wrong time they will be engulfed by flames and die.


<p align="center">

<strong>Figure 1: Example of gameplay</strong>

</p>

<p align="center">

<img src="img/track_showcase.gif" width="391" height="181" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_failure.gif" width="391" height="181" />

</p>


The player’s current position and velocity in the minecart are factors to consider when determining when to get off. Since the player in the minecart will always be moving even when it decides to get off the minecart, it should decide to get off a couple blocks away from the goal because by the time their action is executed their position would have changed (hopefully to where the safe block is).

Minecarts typically have a predefined speed of 8 m/s. In our CrossyCart game, however, minecart speeds are variable throughout the track since minecarts collide at both ends of the 20 block track in order to move back and forth. The collision briefly brings the minecart to a stop before accelerating it again which makes it more difficult to determine the right time to get off the minecart. Getting off 3 blocks away at a velocity of 1.5, for example, may land the player on the goal block, but if the velocity is 0.6 the block distance may be less. Because of this variability, it is necessary to use machine learning algorithms to create an AI that can reliably complete the track.

---

## Approaches

In our previous report we created an AI that was able to eventually complete 1 track with a predetermined goal block which served as our baseline. Since then, we have randomized the position of the goal block and changed our states and rewards in order to create an AI that is able to complete multiple tracks with different goal blocks.

Our AI automatically gets into position to get on the minecart and gets on the minecart. The main problem lies in when it decides to get off of the minecart. We chose to use q-tabular reinforcement learning because there is a moderate number of states with only two actions to choose from: get off (crouch) or nothing. Since q-learning is model free, we are also able to see the agent learn to complete the track and handle stochastic transitions (ex. changes in speed while riding).

**Track Set-up**

After running the program, the user is prompted to enter a number of tracks that the agent will have to cross. This inputted number is used to create n number of 20-block tracks each with its own randomized goal block. The x-coordinate of the randomized goal blocks for each track is stored in an array to create our states later.

**Q-Tabular Learning**

<u>States:</u>

Our states are stored as a tuple of (distance_from_goal, current_velocity).

&nbsp;&nbsp; distance_from_goal
* The distance_from_goal only focuses on the x-coordinate difference (left ↔ right) because that is the only factor that plays into when the agent should get off the minecart. Movement in Minecraft is continuous, not block-by-block, so x-position values provided by Malmo are float values. Obviously, using this would create too many states for our q-table, so we rounded states to the nearest integer value:

<p align="center">

<img src="img/round_int.png"/>

</p>

* Distance is negative if it is on the right side of the goal (from the agent's perspective) and positive if it is on the left. Using the agent's current position, we calculated this by doing:

<p align="center">

<img src="img/distance_away.png" width="259" height="108" />

</p>

&nbsp;&nbsp; current_velocity
* Like the x-coordinate values, the velocity of the minecart also varied by many decimal places. In order to reduce the number of states we rounded again, this time to the nearest tenth decimal place. 


<u>Rewards:</u>

* **=10**: landed on goal block
* **-10**: landed on fire
* **-1**: landed on fire when previously landing on either goal or fire from this state (q-value not 0)

We will elaborate on these rewards when we explain our choose_action function below.



---

## Evaluation

Pictured below is a table which shows an example of the agent on a track and how the q-table would get updated based on which block it gets off at. 
* Green = goal block
* Red = fire block (agent hasn’t tried block yet)
* Orange = fire block (agent previously tried this block)
* A = agent

<img src="img/example_table.png" width="800" height="60" />

Our program is able to successfully find a path for the agent across multiple tracks. As previously stated, our baseline for success was testing whether the agent could make it across one track. 

<p align="center">

<strong>Figure 1: Examples of successful (left) and unsuccessful (right) gameplay</strong>

</p>

<p align="center">

<img src="img/example_failure.gif" width="391" height="181" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_success.gif" width="391" height="181" />

</p>

The two images above were taken from the same run. The example on the left shows the agent failing to solve the problem while the example on the right shows how it learned and solved the problem. 

After successfully solving the baseline, we moved on to testing our program with multiple tracks. 

<p align="center">

<strong>Figure 1: Examples of successful gameplay across 3 tracks</strong>

</p>

<p align="center">

<img src="img/3_track_success.gif" width="391" height="181" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_success.gif" width="391" height="181" />

</p>

For our prototype build we only used the agent's current rounded x-position for our states. In our final version we realized we needed to make changes in order to be able to cross multiple tracks. By using the distance away from the goal block and velocities as states our agent is able to apply what it learned from successfully crossing the first track onto crossing subsequent tracks. After making these changes we recognized the disadvantages of using q-learning for this problem since many things had to be rounded in order to efficiently use a q-table.

---

## References
