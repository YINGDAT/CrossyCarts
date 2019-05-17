"""
Minecraft recreation of Frogger/CrossyRoad game 

For CS 175 - Project in AI
Author: Suzanna Chen, Yingda Tao, and Nidhi Srinivas Vellanki
"""

import MalmoPython
import os
import sys
import time
import json
import random
import math

def GetMissionXML(goal):
	return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
			<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

			  <About>
				<Summary>CrossyCarts - Minecraft recreation of Frogger/CrossyRoad</Summary>
			  </About>

			<ServerSection>
			  <ServerInitialConditions>
				<Time>
					<StartTime>0</StartTime>
					<AllowPassageOfTime>false</AllowPassageOfTime>
				</Time>
				<Weather>clear</Weather>
			  </ServerInitialConditions>

			  <ServerHandlers>
				  <FlatWorldGenerator generatorString="biome_1" />
				  <DrawingDecorator>
	                  		<DrawCuboid x1="-11" y1="4" z1="-3" x2="31" y2="40" z2="-3" type="stone_slab"/>
	                  		<DrawCuboid x1="-11" y1="4" z1="-2" x2="-11" y2="40" z2="10" type="stone_slab"/>
	                  		<DrawCuboid x1="31" y1="4" z1="-2" x2="31" y2="40" z2="10" type="stone_slab"/>
	                  		
	                  		<DrawCuboid x1="-10" y1="4" z1="1" x2="30" y2="4" z2="1" type="redstone_block"/>
	                  		<DrawCuboid x1="-11" y1="5" z1="1" x2="-11" y2="5" z2="1" type="obsidian"/>
	                  		<DrawCuboid x1="31" y1="5" z1="1" x2="31" y2="5" z2="1" type="obsidian"/>
	                  		<DrawCuboid x1="-10" y1="6" z1="1" x2="30" y2="6" z2="1" type="fence"/>
	                  		<DrawLine x1="-10" y1="5" z1="1" x2="30" y2="5" z2="1" type="golden_rail"/>
	                  		<DrawEntity x="-10" y="5" z="1" type="MinecartRideable"/>

	                  		<DrawCuboid x1="-10" y1="4" z1="2" x2="30" y2="4" z2="2" type="quartz_block"/>
	                  		<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="2" x2="''' + str(goal) + '''" y2="4" z2="2" type="emerald_block"/>

	                  		<DrawCuboid x1="-10" y1="4" z1="4" x2="30" y2="4" z2="4" type="redstone_block"/>
	                  		<DrawLine x1="-10" y1="5" z1="4" x2="30" y2="5" z2="4" type="golden_rail"/>

				  </DrawingDecorator>

				  <ServerQuitFromTimeUp timeLimitMs="10000"/>
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>

			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="0" y="5" z="0"/>
				</AgentStart>
				<AgentHandlers>
					<DiscreteMovementCommands/>
					<AgentQuitFromTouchingBlockType>
						<Block type="redstone_block"/>
					</AgentQuitFromTouchingBlockType>
					<ObservationFromGrid>
					  <Grid name="floorAll">
						<min x="0" y="0" z="0"/>
						<max x="0" y="0" z="0"/>
					  </Grid>
				  </ObservationFromGrid>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''



if __name__ == '__main__':
	agent_host = MalmoPython.AgentHost()
	try:
		agent_host.parse( sys.argv )
	except RuntimeError as e:
		print('ERROR:',e)
		print(agent_host.getUsage())
		exit(1)
	if agent_host.receivedArgument("help"):
		print(agent_host.getUsage())
		exit(0)

	num_reps = 1
	for i in range(num_reps):
		#rnd = random.random()
		random.seed(time.time())
		goal_block = random.randint(-10, 30)

		my_mission = MalmoPython.MissionSpec(GetMissionXML(goal_block), True)
		my_mission_record = MalmoPython.MissionRecordSpec()
		my_mission.requestVideo(800, 500)
		my_mission.setViewpoint(1)

		# Attempt to start a mission:
		max_retries = 3
		my_clients = MalmoPython.ClientPool()
		my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

		for retry in range(max_retries):
			try:
				agent_host.startMission( my_mission, my_clients, my_mission_record, 0, "%s-%d" % ('Moshe', i) )
				break
			except RuntimeError as e:
				if retry == max_retries - 1:
					print("Error starting mission", (i+1), ":",e)
					exit(1)
				else:
					time.sleep(2)

		# Loop until mission starts:
		print("Waiting for the mission", (i+1), "to start ",)
		world_state = agent_host.getWorldState()
		while not world_state.has_mission_begun:
			#sys.stdout.write(".")
			time.sleep(0.1)
			world_state = agent_host.getWorldState()
			for error in world_state.errors:
				print("Error:",error.text)

		print()
		print("Mission", (i+1), "running.")