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


num_tracks = None
track_length = 20


def createTracks(n, length, goal_blocks):
	''' Creates n number of tracks/obstacles with minecarts for the agent to get through'''
	drawTracks = ""
	for i in range(n):
		goal = goal_blocks[i]
		trackPos = (i*3)+1
		if i == 0:
			trackPos = i+1
		safePos = trackPos+1
		emptyPos = safePos+1
		goal_block = "emerald_block"
		if i == n-1:
			goal_block = "diamond_block"
		currTrack = '''	    
							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)-1) + '''" y2="4" z2="''' + str(trackPos) + '''" type="redstone_block"/>
							<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(0-(length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
							<DrawCuboid x1="''' + str((length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
							<DrawLine x1="''' + str(0-(length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="golden_rail"/>

							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str((length//2)-1) + '''" y2="4" z2="''' + str(safePos) + '''" type="netherrack"/>
							<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(safePos) + '''" x2="''' + str(goal-1) + '''" y2="5" z2="''' + str(safePos) + '''" type="fire"/>
							<DrawCuboid x1="''' + str(goal+1) + '''" y1="5" z1="''' + str(safePos) + '''" x2="''' + str(length//2) + '''" y2="5" z2="''' + str(safePos) + '''" type="fire"/>
							<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + str(safePos) + '''" type="''' + goal_block + '''"/>
					'''
		drawTracks += currTrack
		if i % 2 == 0:
			drawTracks += '''<DrawEntity x="''' + str(0-(length//2)) + '''" y="5" z="''' + str(trackPos+0.5) + '''" type="MinecartRideable"/>'''
		else:
			drawTracks += '''<DrawEntity x="''' + str((length//2)-1) + '''" y="5" z="''' + str(trackPos+0.5) + '''" type="MinecartRideable"/>'''
	return '''<DrawingDecorator>
						''' + drawTracks + '''
			  </DrawingDecorator>'''


def GetMissionXML(n_tracks, length, goal_blocks):
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
				  ''' + createTracks(n_tracks, length, goal_blocks) + '''
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>

			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="0.5" y="5" z="0.5" yaw="0.5" pitch="-6"/>
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
						<max x="0" y="0" z="0"/>
					  </Grid>
					</ObservationFromGrid>
					<AbsoluteMovementCommands/>
					<MissionQuitCommands/>
					<ChatCommands/>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''

q_table = {}
epsilon = 0.04

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

def get_current_travel_direction(host):
	entities = []
	while len(entities) == 0:
		try:
			entities.extend(get_observation(host, "entity"))
		except:
			time.sleep(0.1)
	for e in entities:
		if e.get('name') == 'MinecartRideable':	
			if e.get('motionX') > 0:
				return "left"
			else:
				return "right"

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

def get_block_under(host):
	block_under = []
	while len(block_under) == 0:
		try:
			block_under.extend(get_observation(host, "under"))
			if block_under[0] == "air":
				block_under.clear()
		except:
			time.sleep(0.1)
	return block_under[0]


def get_possible_actions():
	return ["crouch", "nothing"]

def choose_action(curr_state, possible_actions, eps):
	print("CHOOSE_ACTION STATE: ", curr_state)
	sol_found = False
	for v in q_table.values():
		if v.get('crouch') >= 10:
			sol_found = True

	if curr_state not in q_table:
		q_table[curr_state] = {}
	for action in possible_actions:
		if action not in q_table[curr_state]:
			q_table[curr_state][action] = 0

	q_value = q_table[curr_state]['crouch']

	if q_value == 10:
		return "crouch"
	elif q_value == 0:
		if sol_found:
			return "nothing"
		else:
			return "crouch"
	elif q_value < 0:		# Takes care of case where a state might work even if previously failed
		percentage = epsilon - (0.02*abs((q_value+10)))		# -5% per -1 past -10
		rnd = random.random()
		print("random #: ", rnd)


		if rnd <= percentage:
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
			if get_block_under(host) == "emerald_block":
				q_table[curr_state][action] += 10
				return 10
			else:
				if q_table[curr_state][action] == 0:
					q_table[curr_state][action] -= 10
					return -10
				else:
					q_table[curr_state][action] -= 1
					return -1
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
		a0 = choose_action(s0, get_possible_actions(), epsilon)
		S.append(s0)
		A.append(a0)
		R.append(0)

		current_r = act(host, curr_state, a0)
		R.append(current_r)

		if current_r != 0:
			return True
		else:
			return False

		done_updating = True

def get_on_minecart(host):
	on_minecart = False
	# Move forward until in position to get on minecart
	host.sendCommand("move 1")
	#print(get_current_z_state(host))
	while int(get_current_z_state(host)) % 3 != 0:
		print("in loop: ", str(get_current_z_state(host)))		
		continue
	host.sendCommand("move 0")
	# Get on minecart
	while not on_minecart:
		host.sendCommand("use 1")
		time.sleep(0.1)
		host.sendCommand("use 0")
		if get_current_z_state(host) % 3 == 1.500:  # > 1
			on_minecart = True
	time.sleep(0.1)
	return on_minecart




if __name__ == '__main__':
	# Prompt user to provide track numbers
	print("\nCrossyCart is a Minecraft AI that gets on minecarts and gets off at destination blocks in order to cross the road.")
	while type(num_tracks) != int:
		try:
			num_tracks = int(input("Before it begins, enter the number of tracks the AI will have to cross: "))
		except:
			print("Please enter an integer\n")
			continue

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

	# Create randomized goal blocks
	goal_blocks = []
	for n in range(num_tracks):
		goal_blocks.append(random.randint((-track_length//2+1), (track_length//2)-2))

	mission_complete = False
	restarting = True
	i = 0	# Trial number
	tracks_completed = 0
	while not mission_complete:
		# Only restarts the whole mission if agent dies (after initial start)
		if restarting:
			my_mission = MalmoPython.MissionSpec(GetMissionXML(num_tracks, track_length, goal_blocks), True)      #my_mission = MalmoPython.MissionSpec(GetMissionXML(random.randint(1,10), 20), True)
			my_mission_record = MalmoPython.MissionRecordSpec()
			my_mission.requestVideo(800, 500)
			my_mission.setViewpoint(1)

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

			restarting = False
			tracks_completed = 0

		# Get on minecart
		on_minecart = get_on_minecart(agent_host)

		print("goal_block: ", goal_blocks[tracks_completed])

		# Choose action on minecart
		if on_minecart:
			off_minecart = False
			while not off_minecart:
				distance_from_goal = 0
				current_x = get_current_x_state(agent_host)
				# If curr_x is right of goal block, set its distance away as negative, otherwise set distance as positive
				print("curr_x: ",current_x)
				if goal_blocks[tracks_completed] > current_x:
					distance_from_goal = -(abs(goal_blocks[tracks_completed]-current_x))
				elif goal_blocks[tracks_completed] < current_x:
					distance_from_goal = abs(goal_blocks[tracks_completed] - current_x)
				#print("curr_x: ",get_current_x_state(agent_host))
				print(distance_from_goal)
				off_minecart = run(agent_host, (distance_from_goal, get_current_travel_direction(agent_host)))
				print(q_table)
				time.sleep(0.1)

		if get_block_under(agent_host) == "diamond_block":		# Completed all tracks
			mission_complete = True
		elif get_block_under(agent_host) == "emerald_block":	# Completed current track
			tracks_completed += 1
		else:													# Agent died and has to restart
			restarting = True
			print("TRIAL ", i, " FAILED")
			i += 1
			agent_host.sendCommand("quit")

	print("Mission Successful")
