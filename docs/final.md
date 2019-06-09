---
layout: default
title:  Final
---
## Video

## Project Summary
CrossyCart is an Minecraft adaptation of the games Crossy Road™ and Frogger™.

In this version, the player must get on minecarts and get off of them at the right time in order to safely cross the tracks. Minecarts move back and forth along a 20 block minecart track with randomized safe drop-off points. If the player gets off at the wrong time they will be engulfed by flames and die.


&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_success.gif" width="391" height="181" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="img/example_failure.gif" width="391" height="181" />


The player’s current position and velocity in the minecart are factors to consider when determining when to get off. Since the player in the minecart will always be moving even when it decides to get off the minecart, it should decide to get off a couple blocks away from the goal because by the time their action is executed their position would have changed (hopefully to where the safe block is).

Minecarts typically have a predefined speed of 8 m/s. In our CrossyCart game, however, minecart speeds are variable throughout the track since minecarts collide at both ends of the 20 block track in order to move back and forth. The collision briefly brings the minecart to a stop before accelerating it again which makes it more difficult to determine the right time to get off the minecart. Getting off 3 blocks away at a velocity of 1.5, for example, may land the player on the goal block, but if the velocity is 0.6 the block distance may be less. Because of this variability, it is necessary to use machine learning algorithms to create an AI that can reliably complete the track.

## Approaches

## Evaluation

## References
