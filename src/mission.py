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

def GetMissionXML():
	return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
			<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

			  <About>
				<Summary>CrossyCarts - Minecraft recreation of Frogger/CrossyRoad</Summary>
			  </About>

			<ServerSection>
			  <ServerInitialConditions>
				<Time>
					<StartTime>1000</StartTime>
					<AllowPassageOfTime>false</AllowPassageOfTime>
				</Time>
				<Weather>clear</Weather>
			  </ServerInitialConditions>

			  <ServerHandlers>
				  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;35;village"/>
				  <DrawingDecorator>
                    <DrawCuboid x1="-10" y1="226" z1="-1" x2="11" y2="226" z2="20" type="air"/>
				  </DrawingDecorator>

				  <ServerQuitFromTimeUp timeLimitMs="10000"/>
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>

			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="0.5" y="56.0" z="0.5" yaw="0"/>
				</AgentStart>
				<AgentHandlers>
					<DiscreteMovementCommands/>
					<AgentQuitFromTouchingBlockType>
						<Block type="redstone_block"/>
					</AgentQuitFromTouchingBlockType>
					<ObservationFromGrid>
					  <Grid name="floorAll">
						<min x="-10" y="-1" z="-10"/>
						<max x="10" y="-1" z="10"/>
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
		my_mission = MalmoPython.MissionSpec(GetMissionXML(), True)
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