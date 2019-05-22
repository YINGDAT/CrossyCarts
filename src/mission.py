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

def createTracks(n, length):
	''' Creates n number of tracks/obstacles with minecarts for the agent to get through'''
	drawTracks = ""
	for i in range(n):
		#random.seed(time.time())
		goal = random.randint((-length//2), (length//2))
		trackPos = (i*3)+1
		if i == 0:
			trackPos = i+1
		safePos = trackPos+1
		emptyPos = safePos+1
		currTrack = '''	    
							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(trackPos) + '''" x2="''' + str(length//2) + '''" y2="4" z2="''' + str(trackPos) + '''" type="redstone_block"/>
	                  		<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(0-(length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
	                  		<DrawCuboid x1="''' + str((length//2)+1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)+1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
	                  		<DrawLine x1="''' + str(0-(length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(length//2) + '''" y2="5" z2="''' + str(trackPos) + '''" type="golden_rail"/>
	                  		<DrawEntity x="''' + str(0-(length//2)) + '''" y="5" z="''' + str(trackPos) + '''" type="MinecartRideable"/>

	                  		<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(length//2) + '''" y2="4" z2="''' + str(safePos) + '''" type="quartz_block"/>
	                  		<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + str(safePos) + '''" type="emerald_block"/>

	                '''
		drawTracks += currTrack
	return '''<DrawingDecorator>
    					''' + drawTracks + '''
    		  </DrawingDecorator>'''


def GetMissionXML(n, length):
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
				  ''' + createTracks(n,length) + '''

				  <ServerQuitFromTimeUp timeLimitMs="10000"/>
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>

			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="0.4" y="7" z="0.65" yaw="0.5" pitch="-6"/>
				</AgentStart>
				<AgentHandlers>
					<ContinuousMovementCommands turnSpeedDegs="180"/>
    	            <ObservationFromNearbyEntities>
        	            <Range name="entities" xrange="20" yrange="2" zrange="2"/>
            	    </ObservationFromNearbyEntities>
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

		my_mission = MalmoPython.MissionSpec(GetMissionXML(random.randint(1,10), 20), True)
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

		# Testing if agent can get into cart
		for i in range(40):
			print("use")
			agent_host.sendCommand("use 1")
			agent_host.sendCommand("use 0")
			time.sleep(0.1)

		#agent_host.sendCommand("pitch 0.1")

		#command = input("Send a command: ")
		#agent_host.sendCommand(command)
		
		for i in range(100):
			print("c")
			agent_host.sendCommand("crouch 1")
			agent_host.sendCommand("crouch 0")
			#agent_host.sendCommand("jump 1")
			#agent_host.sendCommand("jump 0")


			time.sleep(0.1)
		