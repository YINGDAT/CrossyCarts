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
from collections import defaultdict, deque
from copy import deepcopy


def createTracks(n, length):
	''' Creates n number of tracks/obstacles with minecarts for the agent to get through'''
	drawTracks = ""
	goal = -6 			# Set goal block
	for i in range(n):
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
							<DrawEntity x="''' + str(0-(length//2)) + '''" y="5" z="''' + str(trackPos+0.5) + '''" type="MinecartRideable"/>

							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(length//2) + '''" y2="4" z2="''' + str(safePos) + '''" type="quartz_block"/>
							<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + str(safePos) + '''" type="''' + goal_block + '''"/>

					'''
		drawTracks += currTrack
	return '''<DrawingDecorator>
						''' + drawTracks + '''
			  </DrawingDecorator>'''


def GetMissionXML(n, length, agent_x):
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
				  <FlatWorldGenerator generatorString="biome_1" forceReset="true" />
				  ''' + createTracks(n, length) + '''
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>

			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="'''+ str(agent_x) +'''" y="5" z="0.5" yaw="0.5" pitch="-6"/>
				</AgentStart>
				<AgentHandlers>
					<ContinuousMovementCommands turnSpeedDegs="480"/>
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
					<AbsoluteMovementCommands/>
					<MissionQuitCommands/>
					<ChatCommands/>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''

q_table = {}
epsilon = 0.35

def get_observation(host, kind):
	'''Get different world observations'''
	current_state = host.getWorldState()
	if len(current_state.observations) > 0:
		msg = current_state.observations[0].text
		observations = json.loads(msg)
		if kind == "ahead":
			return observations.get(u'floorAhead', 0)
		elif kind == "under":
			block_under = observations.get(u'floorUnder', 0)
			return block_under
		elif kind == "entity":
			return observations.get(u'entities', 0)

def get_current_x_state(host):
	entities = []
	while len(entities) == 0:
		try:
			entities.extend(get_observation(host, "entity"))
		except:
			time.sleep(0.1)
	for e in entities:
		if e.get('name') == 'CrossyCartsBot':	
			x = e.get('x')
			if x >= 0:
				return int(x+0.5)
			else:
				return int(x-0.5)

def get_current_z_state(host):
	entities = []
	while len(entities) == 0:
		try:
			entities.extend(get_observation(host, "entity"))
		except:
			time.sleep(0.1)
	for e in entities:
		if e.get('name') == 'CrossyCartsBot':
			return e.get('z')

def get_possible_actions():
	return ["crouch", "nothing"]

def choose_action(curr_state, possible_actions, eps):
	if curr_state not in q_table:
		q_table[curr_state] = {}
	for action in possible_actions:
		if action not in q_table[curr_state]:
			q_table[curr_state][action] = 0
	if q_table[curr_state]['crouch'] == 0:
		return "crouch"
	elif curr_state in range(-1, -9) and q_table[curr_state]['crouch'] == -10:		# Takes care of case where a state might work even if previously failed
		 rnd = random.random()
		 print("random #: ", rnd)
		 if rnd <= epsilon:
		 	return "crouch"
	else:
		return "nothing"


def crouch(host, curr_state, action):
	command_executed = False
	while not command_executed:
		host.sendCommand("crouch 1")
		time.sleep(0.2)
		host.sendCommand("crouch 0")

		if get_current_z_state(host) > 2:
			if get_current_x_state(host) == -5:
				q_table[curr_state][action] = 10
				return 10
			else:
				q_table[curr_state][action] = -10
				return -10
			command_executed = True

def act(host, curr_state, action):
	if action == "nothing":
		q_table[curr_state][action] = 0
		return 0
	else:
		return crouch(host, curr_state, action)

def run(host, curr_state):
	S, A, R = deque(), deque(), deque()
	done_updating = False
	while not done_updating:
		s0 = curr_state
		a0 = choose_action(s0, get_possible_actions() ,epsilon)
		S.append(s0)
		A.append(a0)
		R.append(0)

		current_r = act(host, curr_state, a0)
		R.append(current_r)

		if current_r == -10 or current_r == 10:
			return True
		else:
			return False

		done_updating = True






if __name__ == '__main__':

	agent_host = MalmoPython.AgentHost()
	try:
		agent_host.parse(sys.argv)
	except RuntimeError as e:
		print('ERROR:',e)
		print(agent_host.getUsage())
		exit(1)
	if agent_host.receivedArgument("help"):
		print(agent_host.getUsage())
		exit(0)

	solution_found = False
	i = 0
	while not solution_found:
		time.sleep(1)

		my_mission = MalmoPython.MissionSpec(GetMissionXML(1, 20,random.randint(-7,7)), True)      #my_mission = MalmoPython.MissionSpec(GetMissionXML(random.randint(1,10), 20), True)
		my_mission_record = MalmoPython.MissionRecordSpec()
		my_mission.requestVideo(800, 500)
		my_mission.setViewpoint(1)
		if i > 0:
			agent_host.sendCommand("tp 0.5 " + str(4+(i*15)) + " 0.5")

		# Attempt to start a mission:

		my_client_pool = MalmoPython.ClientPool()
		my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
		max_retries = 3
		for retry in range(max_retries):
			try:
				agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "CrossyAI")
				break
			except RuntimeError as e:
				if retry == max_retries - 1:
					print("Error starting trial", (i+1), ":",e)
					exit(1)
				else:
					time.sleep(2)
		time.sleep(0.1)
		# Loop until mission starts:
		print("Waiting for trial", (i+1), "to start ",)
		world_state = agent_host.getWorldState()
		while not world_state.has_mission_begun:
			#sys.stdout.write(".")
			time.sleep(0.1)
			world_state = agent_host.getWorldState()
			for error in world_state.errors:
				print("Error:",error.text)

		print()
		print("Trial", (i+1), "running.")

		# Get on minecart
		on_minecart = False
		while not on_minecart:
			agent_host.sendCommand("use 1")
			time.sleep(0.1)
			agent_host.sendCommand("use 0")
			if get_current_z_state(agent_host) > 1:
				on_minecart = True
		time.sleep(0.1)

		if on_minecart:
			off_minecart = False
			while not off_minecart:
				off_minecart = run(agent_host, get_current_x_state(agent_host))
				print(q_table)
				time.sleep(0.1)
		if get_current_x_state(agent_host) == -6:
			break

		i += 1
		print("TRIAL FAILED: -10")
		agent_host.sendCommand("quit")

	print("Mission Successful")
