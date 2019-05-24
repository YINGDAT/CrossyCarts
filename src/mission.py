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

'''
Notes:
- z = (i*3)+1 = on goal platforms 
'''


def createTracks(n, length):
	''' Creates n number of tracks/obstacles with minecarts for the agent to get through'''
	drawTracks = ""
	goal_loc = [(length//2)//2, (0-(length//2))//2]		# only 2 non-random goal blocks for status report
	for i in range(n):
		# random goal reserved for final report
		goal = goal_loc[i]										#goal = random.randint((-length//2), (length//2))
		trackPos = (i*3)+1
		if i == 0:
			trackPos = i+1
		safePos = trackPos+1
		emptyPos = safePos+1
		goal_block = "emerald_block"
		if i == n-1:
			goal_block = "diamond_block"
		currTrack = '''	    
							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(trackPos) + '''" x2="''' + str(length//2) + '''" y2="4" z2="''' + str(trackPos) + '''" type="redstone_block"/>
	                  		<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(0-(length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
	                  		<DrawCuboid x1="''' + str((length//2)+1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)+1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
	                  		<DrawLine x1="''' + str(0-(length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(length//2) + '''" y2="5" z2="''' + str(trackPos) + '''" type="golden_rail"/>
	                  		<DrawEntity x="''' + str(0-(length//2)) + '''" y="5" z="''' + str(trackPos) + '''" type="MinecartRideable"/>

	                  		<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(length//2) + '''" y2="4" z2="''' + str(safePos) + '''" type="quartz_block"/>
	                  		<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + str(safePos) + '''" type="''' + goal_block + '''"/>

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
					<Placement x="0.4" y="5" z="0.65" yaw="0.5" pitch="-6"/>
				</AgentStart>
				<AgentHandlers>
					<ContinuousMovementCommands turnSpeedDegs="180"/>
    	            <ObservationFromNearbyEntities>
        	            <Range name="entities" xrange="20" yrange="2" zrange="2"/>
            	    </ObservationFromNearbyEntities>
					<ObservationFromGrid>
					  <Grid name="floorAhead">
						<min x="-4" y="0" z="1"/>
						<max x="4" y="0" z="1"/>
					  </Grid>
					  <Grid name="floorUnder">
						<min x="0" y="-1" z="0"/>
						<max x="0" y="-1" z="0"/>
					  </Grid>
				  </ObservationFromGrid>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''

class CrossyAI:
	def __init__(self, alpha=0.3, gamma=1, n=1, ai_host=None):
		"""Constructing an RL agent.
		Args
			alpha:  <float>  learning rate      (default = 0.3)
			gamma:  <float>  value decay rate   (default = 1)
			n:      <int>    number of back steps to update (default = 1)
		"""
		self.epsilon = 0.2  # chance of taking a random action instead of the best
		self.q_table = {}
		self.n, self.alpha, self.gamma = n, alpha, gamma

		self.agent_host = ai_host

	def get_observation(self, kind):
		'''Get different world observations'''
		currState = self.agent_host.getWorldState()
		if len(currState.observations) > 0:
			msg = currState.observations[0].text
			observations = json.loads(msg)
			if kind == "ahead":
				return observations.get(u'floorAhead', 0)
			elif kind == "under":
				return observations.get(u'floorUnder', 0)
			elif kind == "entity":
				return observations.get(u'entities', 0)

	def get_curr_state(self):
		'''Creates a unique identifier for a state (defined as the current
		   position of the agent, or position of the minecart if agent is supposed
		   to get on)
				returns [x,y,z] coordinates rounded to ensure states are confined
								to individual blocks
				x: rounded to nearest integer
				y: rounded to 4.7 for on cart
				z: floor
		'''
		x = -1
		y = -1
		z = -1
		entities = self.get_observation("entity")
		if entities == None:
			return #"World still rendering"
		for e in entities:
			if e.get('name') == 'CrossyCartsBot':
				x = e.get('x')
				y = e.get('y')
				z = int(e.get('z'))
				if int(z) == 0 and y > 4:
					return #"Agent still falling"
				if x >= 0:
					x += 0.5
				else:
					x -= 0.5
				x = int(x)
				if y > 4.7 and y < 4.9:
					y = 4.7
				elif y != 4.0 and y != 5.0:
					return #"Agent in air"
			else:
				if z % 3 == 0:
					x = e.get('x')
					if x >= 0:
						x += 0.5
					else:
						x -= 0.5
					x = int(x)
		return [x,y,z]
				
	def get_possible_actions(self):
		return ["use", "crouch", "move"]

		'''
	def get_possible_action(self, grid_entity):
		if grid_entity[0][0] == "redstone_block":
			return "use"
		else if grid_entity[0][0] == "air":
			return "move"
		else:
			return "use"
			'''

	#def act(self, action):
	#	action = get_possible_action()
	#	if action == "move":
	#def run(self):

		



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
	AI = CrossyAI(ai_host=agent_host)
	for i in range(num_reps):

		my_mission = MalmoPython.MissionSpec(GetMissionXML(2, 20), True)      #my_mission = MalmoPython.MissionSpec(GetMissionXML(random.randint(1,10), 20), True)
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


		#AI.get_possible_action

		
		# Testing if agent can get into cart
		print("USE")
		for i in range(30):
			agent_host.sendCommand("use 1")
			agent_host.sendCommand("use 0")
			print(AI.get_curr_state())
			time.sleep(0.1)

		print("\n\n\nCROUCH")
		for i in range(5):
			agent_host.sendCommand("crouch 1")
			agent_host.sendCommand("crouch 0")
			print(AI.get_curr_state())
			time.sleep(0.1)

		print("\n\n\nMOVE")
		for i in range(20):
			agent_host.sendCommand("move 1")
			time.sleep(0.1)
			print(AI.get_curr_state())

			#AI.getObservations()